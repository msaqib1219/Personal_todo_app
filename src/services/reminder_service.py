"""ReminderService: background polling for due-time reminders."""

import threading
from datetime import datetime

from sqlmodel import Session, select

from src.config import logger
from src.models.task import DEFAULT_REMINDER_MINUTES, Task


class ReminderService:
    """Polls for tasks approaching their due time and dispatches notifications."""

    def __init__(self, engine, app_callback):
        self._engine = engine
        self._app_callback = app_callback
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self):
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def _poll_loop(self):
        while not self._stop_event.is_set():
            try:
                self._check_reminders()
            except Exception:
                logger.exception("Reminder check failed")
            self._stop_event.wait(30)

    def _check_reminders(self):
        with Session(self._engine) as session:
            statement = select(Task).where(
                Task.is_completed == False,  # noqa: E712
                Task.reminder_sent == False,  # noqa: E712
                Task.due_date.is_not(None),  # type: ignore[union-attr]
                Task.due_time.is_not(None),  # type: ignore[union-attr]
            )
            tasks = list(session.exec(statement).all())
            now = datetime.now()
            for task in tasks:
                reminder_min = task.reminder_minutes or DEFAULT_REMINDER_MINUTES
                try:
                    hour, minute = map(int, task.due_time.split(":"))
                    due_dt = datetime.combine(task.due_date, datetime.min.time().replace(
                        hour=hour, minute=minute,
                    ))
                except (ValueError, AttributeError):
                    continue
                from datetime import timedelta
                trigger_at = due_dt - timedelta(minutes=reminder_min)
                if trigger_at <= now:
                    task.reminder_sent = True
                    session.add(task)
                    session.commit()
                    self._dispatch(task.id, task.title, due_dt)

    def _dispatch(self, task_id: int, title: str, due_dt: datetime):
        # Desktop notification
        try:
            from plyer import notification
            notification.notify(
                title="Todo Reminder",
                message=f"{title}\nDue: {due_dt.strftime('%Y-%m-%d %H:%M')}",
                timeout=10,
            )
        except Exception:
            logger.exception("Desktop notification failed")
        # In-app callback (must be scheduled on main thread)
        try:
            self._app_callback(task_id, title, due_dt)
        except Exception:
            logger.exception("App callback failed")
