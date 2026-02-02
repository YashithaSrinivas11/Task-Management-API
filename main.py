from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import uuid

app = FastAPI(title="Task Management API")
tasks_db = []

class Task(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str = "pending"
    created_at: Optional[datetime] = None

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    task.id = str(uuid.uuid4())
    task.created_at = datetime.now()
    tasks_db.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.put("/tasks/{task_id}")
def update_task(task_id: str, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_task.id = task_id
            updated_task.created_at = task.created_at
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")