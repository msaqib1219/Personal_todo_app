"""Unit tests for ReminderService."""

from datetime import date, datetime, timedelta

from sqlmodel import Session, SQLModel, create_engine

from src.models.task import Task
from src.services.reminder_service import ReminderService


def _setup():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


class TestCheckReminders:
    def test_triggers_callback_for_due_task(self):
        engine = _setup()
        now = datetime.now()
        with Session(engine) as session:
            task = Task(
                title="Due soon",
                due_date=now.date(),
                due_time=now.strftime("%H:%M"),
                reminder_minutes=30,
                reminder_sent=False,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            task_id = task.id

        called = []
        svc = ReminderService(engine, lambda tid, title, dt: called.append((tid, title)))
        svc._check_reminders()

        assert len(called) == 1
        assert called[0][0] == task_id

        # Verify reminder_sent is now True
        with Session(engine) as session:
            t = session.get(Task, task_id)
            assert t.reminder_sent is True

    def test_skips_already_sent(self):
        engine = _setup()
        now = datetime.now()
        with Session(engine) as session:
            task = Task(
                title="Already sent",
                due_date=now.date(),
                due_time=now.strftime("%H:%M"),
                reminder_minutes=30,
                reminder_sent=True,
            )
            session.add(task)
            session.commit()

        called = []
        svc = ReminderService(engine, lambda tid, title, dt: called.append(1))
        svc._check_reminders()
        assert len(called) == 0

    def test_skips_tasks_without_due_time(self):
        engine = _setup()
        with Session(engine) as session:
            task = Task(
                title="No time",
                due_date=date.today(),
                due_time=None,
                reminder_minutes=15,
                reminder_sent=False,
            )
            session.add(task)
            session.commit()

        called = []
        svc = ReminderService(engine, lambda tid, title, dt: called.append(1))
        svc._check_reminders()
        assert len(called) == 0

    def test_skips_future_task(self):
        engine = _setup()
        future = datetime.now() + timedelta(hours=2)
        with Session(engine) as session:
            task = Task(
                title="Future task",
                due_date=future.date(),
                due_time=future.strftime("%H:%M"),
                reminder_minutes=5,
                reminder_sent=False,
            )
            session.add(task)
            session.commit()

        called = []
        svc = ReminderService(engine, lambda tid, title, dt: called.append(1))
        svc._check_reminders()
        assert len(called) == 0
