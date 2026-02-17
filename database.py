import select
from sqlmodel import Session


from sqlmodel import Field, SQLModel, create_engine, Session, select


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: str


db_url = "sqlite:///task_db.db"

engine = create_engine(db_url, echo=True)


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


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
