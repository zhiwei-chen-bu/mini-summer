from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
from itertools import count

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Todo(BaseModel):
    id: int
    task: str
    done: bool = False

todos: List[Todo] = []
id_counter = count(1)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    todo = Todo(id=next(id_counter), task=item)
    todos.append(todo)
    return RedirectResponse("/", status_code=303)

@app.get("/todos/all")
def get_all_todo():
    return todos

@app.put("/todos/{id}/complete")
def update_todo(id: int, todo: Todo):
    for t in todos:
        if t.id == id:
            t.done = True
            return {"message": "Todo marked as complete"}
    return {"error": "Todo not found"}

@app.get("/todos/pending")
def pending_todo():
    return [t for t in todos if not t.done]

@app.delete("/todos/{id}")
def delete_todo(id: int):
    global todos
    todos = [t for t in todos if t.id != id]
    return {"message": "Todo deleted"}
