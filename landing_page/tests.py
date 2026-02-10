from django.test import TestCase
from rest_framework.test import APIClient
from .models import Tag, BlogPost, Project, Event

class BlogPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='Robotics')

    def test_create_blog_post_with_rich_text(self):
        payload = {
            'title': 'First Post',
            'summary': 'Short summary',
            'content': '<p><strong>Hello</strong> world</p>',
        }
        response = self.client.post('/api/blog/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog = BlogPost.objects.first()
        self.assertEqual(blog.content, payload['content'])

    def test_blog_post_list_includes_content(self):
        post = BlogPost.objects.create(
            title='Post',
            summary='Summary',
            content='<p>Body</p>',
        )
        post.tags.add(self.tag)
        response = self.client.get('/api/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('content', response.data[0])

class ProjectEventApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='AI')

    def test_create_project_with_author_and_date(self):
        payload = {
            'title': 'Project Alpha',
            'description': 'Short description',
            'content': '<p>Long content</p>',
            'author_name': 'Alex Doe',
            'tag_ids': [self.tag.id],
        }
        response = self.client.post('/api/projects/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        project = Project.objects.first()
        self.assertEqual(project.author_name, 'Alex Doe')
        self.assertEqual(project.content, '<p>Long content</p>')

    def test_create_event_with_author_and_date(self):
        payload = {
            'title': 'Workshop',
            'summary': 'Intro session',
            'content': '<p>Details</p>',
            'author_name': 'Events Team',
        }
        response = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        event = Event.objects.first()
        self.assertEqual(event.author_name, 'Events Team')
        self.assertEqual(event.content, '<p>Details</p>')
