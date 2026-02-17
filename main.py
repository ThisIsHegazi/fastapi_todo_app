from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import get_all_tasks, add_task, delete_task, update_task

app = FastAPI()


class Task(BaseModel):
    id: int | None = None
    task: str


@app.get("/")
def home():
    return {"data": "hello,world"}


@app.get("/tasks")
def get_tasks():
    tasks = get_all_tasks()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="You have No Tasks"
        )
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    created_task = add_task(task)
    if not created_task:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return created_task


@app.put("/tasks/{id}")
def update_spec_task(id: int, task: Task):
    updated_task = update_task(id, task)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No tasks found with id {id}"
        )

    return updated_task


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spec_task(id: int):
    task = delete_task(id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No tasks found with id {id}"
        )
    return task
