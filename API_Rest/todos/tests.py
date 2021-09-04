from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo

class TestListCreateTodos(APITestCase):

    def authenticate(self):
        sample_user_register = {"username":"UsernameTest", "email":"usertest@gmail.com", "password":"password01"}
        self.client.post(reverse('register'), sample_user_register)

        sample_user_login = {"username":"UsernameTest", "password":"password01"}
        response = self.client.post(reverse('login'), sample_user_login)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    
    def test_should_not_create_todo_with_no_auth(self):
        sample_todo = {'title': "title new", 'description': "description new"}
        response = self.client.post(reverse('todos'), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_should_create_todo(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate()
        sample_todo = {'title': "title new", 'description': "description new"}
        response = self.client.post(reverse('todos'), sample_todo)
        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "title new")
        self.assertEqual(response.data['description'], "description new")
        
   
    def test_retrieve_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        sample_todo = {'title': "title new", 'description': "description new"}
        self.client.post(reverse('todos'), sample_todo)
        
        response = self.client.get(reverse('todos'))
        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)






 