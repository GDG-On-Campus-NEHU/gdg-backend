from django.test import TestCase
from rest_framework.test import APIClient

from .models import Tag, BlogPost, Project, Event, Roadmap, TeamMember


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


class TagAndItemsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='Raspberry Pi')

        blog = BlogPost.objects.create(title='Intro to ROS', summary='ROS basics', content='x')
        blog.tags.add(self.tag)

        project = Project.objects.create(title='Robot Arm', description='Build arm', content='x')
        project.tags.add(self.tag)

        roadmap = Roadmap.objects.create(icon_name='🤖', title='Robotics Path', description='path', content='x')
        roadmap.tags.add(self.tag)

        event = Event.objects.create(title='Pi Workshop', summary='Hands-on', content='x')
        event.tags.add(self.tag)

        team = TeamMember.objects.create(name='Sam', role='Lead', bio='Robotics mentor')
        team.tags.add(self.tag)

    def test_tags_list_with_counts(self):
        response = self.client.get('/api/tags/?include_counts=true&type=all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tags'][0]['slug'], 'raspberry-pi')
        self.assertEqual(response.data['tags'][0]['count'], 5)

    def test_items_filter_by_tag_slug(self):
        response = self.client.get('/api/items/?tag=raspberry-pi&type=all')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['pagination']['total'], 5)
        self.assertTrue(all(item['type'] in {'blogs', 'projects', 'events', 'roadmaps', 'team'} for item in response.data['items']))

    def test_tag_detail_returns_metadata_and_items(self):
        response = self.client.get('/api/tags/raspberry-pi/?type=projects&page=1&per_page=20&sort=recent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['tag']['name'], 'Raspberry Pi')
        self.assertEqual(response.data['pagination']['total'], 1)
