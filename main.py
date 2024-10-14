from fasthtml.common import *
import re


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A("Toggle   ", hx_get=f"/toggle/{todo.id}", target_id=tid)
    delete = A("Delete  ", hx_delete=f"/{todo.id}", hx_swap="outerHTML", target_id=tid)

    title_element = todo.title
    # Verificar si el título es una URL
    if re.match(r"^https?://", todo.web):
        web_element = A(todo.web, href=todo.web, target="_blank")
    else:
        web_element = todo.web

    return Li(toggle, delete,title_element, web_element + ("✅" if todo.done else ""), id=tid)


app, rt, todos, Todo = fast_app(
    "todos.db", live=False, render=render, id=int, title=str,web=str, done=bool, pk="id"
)


def mk_input():
    return Input(placeholder="Add a New Todo title", id="title", hx_swap_oob="true"),Input(placeholder="Add a New URL", id="web", hx_swap_oob="true")


@rt("/")
def get():
    frm = Form(
        Group(mk_input(), Button("Add")),
        hx_post="/",
        target_id="todo-list",
        hx_swap="beforeend",
    )
    return Titled("Developer Todos", Card(Ul(*todos(), id="todo-list"), header=frm))


@rt("/{tid}")
def post(todo: Todo):
    web = todo.web.strip()
    title =todo.title
    

    # Verificar si el título es una URL
    if re.match(r"^https?://", web):
        # Aquí puedes agregar la lógica para procesar la URL
        # Por ejemplo, puedes crear un nuevo Todo con la URL como título
        new_todo = Todo(id=None, web=web,title=title, done=False)
        return todos.insert(new_todo)
    else:
        # Si no es una URL, simplemente inserta el Todo normalmente
        return todos.insert(todo)


@rt("/{tid}")
def delete(tid: int):
    todos.delete(tid)


@rt("/toggle/{tid}")
def get(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    return todos.update(todo)


serve()
