"""Entry point: initialize DB, launch GUI."""

from src.config import logger
from src.gui.app import TodoApp
from src.repository.database import create_db_and_tables, create_engine_with_fallback, get_session
from src.repository.task_repo import TaskRepository
from src.services.reminder_service import ReminderService
from src.services.task_service import TaskService


def main():
    logger.info("Application starting")

    engine = create_engine_with_fallback()
    create_db_and_tables(engine)

    session = get_session(engine)
    repo = TaskRepository(session)
    service = TaskService(repo)

    app = TodoApp(service)

    reminder = ReminderService(engine, app._show_reminder_popup)
    reminder.start()

    app.mainloop()

    reminder.stop()
    session.close()
    logger.info("Application shutdown")


if __name__ == "__main__":
    main()
