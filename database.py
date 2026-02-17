from sqlmodel import Field, SQLModel, create_engine


class Tasks(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: str


db_url = "sqlite:///task_db.db"

engine = create_engine(db_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
