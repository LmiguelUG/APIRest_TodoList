from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo

class TestTodosAPIView(APITestCase):

    def create_todo(self):
        sample_todo = {'title': "title new", 'description': "description new"}
        response = self.client.post(reverse('todos'), sample_todo)
        return response

    def authenticate(self):
        sample_user_register = {"username":"UsernameTest", "email":"usertest@gmail.com", "password":"password01"}
        self.client.post(reverse('register'), sample_user_register)
        sample_user_login = {"username":"UsernameTest", "password":"password01"}
        response = self.client.post(reverse('login'), sample_user_login)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


class TestListCreateTodos(TestTodosAPIView):

    def authenticate(self):
        sample_user_register = {"username":"UsernameTest", "email":"usertest@gmail.com", "password":"password01"}
        self.client.post(reverse('register'), sample_user_register)

        sample_user_login = {"username":"UsernameTest", "password":"password01"}
        response = self.client.post(reverse('login'), sample_user_login)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    
    def test_should_not_create_todo_with_no_auth(self):
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_should_create_todo(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate()
        response = self.create_todo()
        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "title new")
        self.assertEqual(response.data['description'], "description new")
        
   
    def test_retrieve_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        self.create_todo()
        response = self.client.get(reverse('todos'))
        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)


class TestTodoDetail(TestTodosAPIView):

    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()
        response_2 = self.client.get(reverse('todo', kwargs = {'id': response.data['id']}))
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id = response.data['id'])
        self.assertEqual(todo.title, response_2.data['title'])

    def test_update_one_item(self):
        self.authenticate()
        response = self.create_todo()
        response_2 = self.client.patch(reverse('todo', kwargs = {'id': response.data['id']}), {'title': "title new update", 'is_complete': True})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id = response.data['id'])
        self.assertIsInstance(response.data['is_complete'], bool)
        self.assertEqual(todo.title, "title new update")
        self.assertEqual(todo.is_complete, True)

    def test_delete_one_item(self):
        self.authenticate()
        response = self.create_todo()
        previous_db_count = Todo.objects.all().count()
        self.assertGreater(previous_db_count, 0)
        self.assertEqual(previous_db_count, 1)
        response = self.client.delete(reverse('todo', kwargs = {'id': response.data['id']}))
        previous_db_count = Todo.objects.all().count()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)