from sqlmodel import Session, select
from database import engine, Tasks


def get_all_tasks():
    with Session(engine) as session:
        all_tasks = session.exec(select(Tasks)).all()
    return all_tasks if all_tasks else None


def add_task(provided_task):
    task = Tasks(task=provided_task.task)
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
    return task


def delete_task(id):
    with Session(engine) as session:
        task = session.get(Tasks, id)
        if not task:
            return None
        session.delete(task)
        session.commit()
    return task


def update_task(id, provided_task):
    with Session(engine) as session:
        task = session.exec(select(Tasks).where(Tasks.id == id)).one_or_none()
        if not task:
            return None

        task.id = id
        task.task = provided_task.task
        session.add(task)
        session.commit()
    return task
