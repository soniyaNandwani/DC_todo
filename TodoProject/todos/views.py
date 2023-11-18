from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Todo

# Create your views here.

servers = {
    'Server A': 0,
    'Server B': 0,
    'Server C': 0
}

def list_todo_items(request):
    context = {'todo_list' : Todo.objects.all()}
    return render(request, 'todos/todo_list.html',context)


def insert_todo_item(request: HttpRequest):
    todo = Todo(content=request.POST['content'])
    todo.save()
    
    # Find server with the least connections
    selected_server = min(servers, key=servers.get)

    # Increment the connections count for the selected server
    servers[selected_server] += 1
    
    print(f"Task added, assigned to {selected_server}, Connections: {servers[selected_server]}")
    
    return redirect('/todos/list/')

def delete_todo_item(request,todo_id):
    todo_to_delete = Todo.objects.get(id=todo_id)
    todo_to_delete.delete()
    
    # Find server with the least connections
    selected_server = min(servers, key=servers.get)

    # Decrement the connections count for the selected server
    servers[selected_server] -= 1
    
    print(f"Task deleted, assigned to {selected_server}, Connections: {servers[selected_server]}")
    
    return redirect('/todos/list/')
