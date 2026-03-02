from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .management.commands.normalize_richtext_html import normalize_html
from .models import Tag, BlogPost, Project, ProjectContributor, Event, Roadmap, TeamMember


class BlogPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='Robotics')
        self.admin_user = get_user_model().objects.create_user(
            username='admin-user',
            password='secret123',
            is_staff=True,
        )

    def test_create_blog_post_with_rich_text(self):
        self.client.force_authenticate(user=self.admin_user)
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

    def test_anonymous_blog_post_create_is_denied(self):
        payload = {
            'title': 'First Post',
            'summary': 'Short summary',
            'content': '<p><strong>Hello</strong> world</p>',
        }
        response = self.client.post('/api/blog/', payload, format='json')
        self.assertIn(response.status_code, {401, 403})

    def test_blog_post_list_excludes_content(self):
        post = BlogPost.objects.create(
            title='Post',
            summary='Summary',
            content='<p>Body</p>',
        )
        post.tags.add(self.tag)
        response = self.client.get('/api/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('content', response.data[0])

    def test_blog_post_detail_includes_content(self):
        post = BlogPost.objects.create(
            title='Post',
            summary='Summary',
            content='<p>Body</p>',
        )
        response = self.client.get(f'/api/blog/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('content', response.data)

    def test_numeric_id_detail_route_fallback(self):
        post = BlogPost.objects.create(
            title='Legacy Post',
            summary='Summary',
            content='<p>Body</p>',
        )
        response = self.client.get(f'/api/blog/{post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], post.id)
        self.assertEqual(response.data['slug'], post.slug)


class ProjectEventApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='AI')
        self.admin_user = get_user_model().objects.create_user(
            username='project-admin-user',
            password='secret123',
            is_staff=True,
        )

    def test_create_project_with_author_and_date(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            'title': 'Project Alpha',
            'description': 'Short description',
            'content': '<p>Long content</p>',
            'author_name': 'Alex Doe',
            'tag_ids': [self.tag.id],
            'is_open_source': True,
            'status': 'in_progress',
            'repo_url': 'https://github.com/example/project-alpha',
            'demo_url': 'https://alpha.example.com',
            'contributors': [
                {
                    'name': 'Deobrat',
                    'role_type': 'Backend',
                    'photo_url': 'https://imgur.com/a.png',
                    'github_url': 'https://github.com/deobrat',
                    'linkedin_url': 'https://linkedin.com/in/deobrat',
                    'website_url': 'https://deobrat.dev',
                    'order': 2,
                },
                {
                    'name': 'Aarav',
                    'role_type': 'Design',
                    'order': 1,
                },
            ],
        }
        response = self.client.post('/api/projects/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        project = Project.objects.first()
        self.assertEqual(project.author_name, 'Alex Doe')
        self.assertEqual(project.content, '<p>Long content</p>')
        self.assertTrue(project.is_open_source)
        self.assertEqual(project.status, 'in_progress')
        self.assertEqual(project.contributors.count(), 2)
        self.assertEqual(project.contributors.first().name, 'Aarav')
        self.assertEqual(project.contributors.last().role_type, 'Backend')

    def test_create_event_with_author_and_date(self):
        self.client.force_authenticate(user=self.admin_user)
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

    def test_anonymous_project_and_event_creates_are_denied(self):
        project_payload = {
            'title': 'Project Alpha',
            'description': 'Short description',
            'content': '<p>Long content</p>',
        }
        event_payload = {
            'title': 'Workshop',
            'summary': 'Intro session',
            'content': '<p>Details</p>',
        }
        project_response = self.client.post('/api/projects/', project_payload, format='json')
        event_response = self.client.post('/api/events/', event_payload, format='json')
        self.assertIn(project_response.status_code, {401, 403})
        self.assertIn(event_response.status_code, {401, 403})

    def test_project_event_list_excludes_content(self):
        Project.objects.create(title='P', description='D', content='<p>Project body</p>')
        Event.objects.create(title='E', summary='S', content='<p>Event body</p>')

        project_response = self.client.get('/api/projects/')
        event_response = self.client.get('/api/events/')

        self.assertEqual(project_response.status_code, 200)
        self.assertEqual(event_response.status_code, 200)
        self.assertNotIn('content', project_response.data[0])
        self.assertNotIn('content', event_response.data[0])

    def test_project_event_detail_include_content(self):
        project = Project.objects.create(title='P', description='D', content='<p>Project body</p>')
        event = Event.objects.create(title='E', summary='S', content='<p>Event body</p>')

        project_response = self.client.get(f'/api/projects/{project.slug}/')
        event_response = self.client.get(f'/api/events/{event.slug}/')

        self.assertEqual(project_response.status_code, 200)
        self.assertEqual(event_response.status_code, 200)
        self.assertIn('content', project_response.data)
        self.assertIn('content', event_response.data)

    def test_project_detail_contains_contributors(self):
        project = Project.objects.create(title='P', description='D', content='<p>Project body</p>')
        ProjectContributor.objects.create(project=project, name='Mia', role_type='ML', order=1)
        response = self.client.get(f'/api/projects/{project.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['contributors'][0]['name'], 'Mia')


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

    def test_bootstrap_and_search_use_summary_payloads(self):
        bootstrap_response = self.client.get('/api/bootstrap/')
        self.assertEqual(bootstrap_response.status_code, 200)
        self.assertTrue(bootstrap_response.data['events'])
        self.assertNotIn('content', bootstrap_response.data['events'][0])

        search_response = self.client.get('/api/search/?q=pi')
        self.assertEqual(search_response.status_code, 200)
        self.assertTrue(search_response.data['events'])
        self.assertNotIn('content', search_response.data['events'][0])
        if search_response.data['blogs']:
            self.assertNotIn('content', search_response.data['blogs'][0])
        if search_response.data['projects']:
            self.assertNotIn('content', search_response.data['projects'][0])
        if search_response.data['roadmaps']:
            self.assertNotIn('content', search_response.data['roadmaps'][0])


class RichTextNormalizationTests(TestCase):
    def test_normalize_html_converts_legacy_patterns(self):
        legacy = (
            '<p style="text-align:center">Hello</p>'
            '<figure class="image image_left"><img src="x.jpg"></figure>'
            '<iframe src="https://www.youtube.com/embed/abc123"></iframe>'
            'https://youtu.be/xyz789'
        )

        normalized = normalize_html(legacy)

        self.assertIn('text-align: center', normalized)
        self.assertIn('image-style-align-left', normalized)
        self.assertIn('<oembed url="https://www.youtube.com/watch?v=abc123"></oembed>', normalized)
        self.assertIn('https://www.youtube.com/watch?v=xyz789', normalized)
