# from todos.views import CreateTodoAPIView, TodoListAPIView
from todos.views import TodosAPIView
from django.urls import path

urlpatterns = [
    # path('create', CreateTodoAPIView.as_view(), name = "create_todo"),
    # path('list', TodoListAPIView.as_view(), name = "list_todos"),
    path('', TodosAPIView.as_view(), name = "todos"),
]

