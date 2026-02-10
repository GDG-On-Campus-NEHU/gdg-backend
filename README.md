# Backend API

This project is a Django REST API for **Google Developer's Group, NEHU** (GDG NEHU) with blogs, projects, roadmaps, events, and team members.

## Setup

```powershell
# from project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # Create admin account
python manage.py runserver
```

## 📚 Complete API Reference

### Blog Posts `/api/blog/`
- `GET /api/blog/` - List all blog posts
- `POST /api/blog/` - Create blog post (multipart)
- `GET /api/blog/{id}/` - Get single blog post
- `PUT/PATCH /api/blog/{id}/` - Update blog post
- `DELETE /api/blog/{id}/` - Delete blog post

**Fields:** `title`, `summary`, `content` (HTML), `image`, `author_name`, `published_date`, `tag_ids`, `tags`

### Projects `/api/projects/`
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create project (multipart)
- `GET /api/projects/{id}/` - Get single project
- `PUT/PATCH /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

**Fields:** `title`, `description`, `content` (HTML), `image`, `author_name`, `published_date`, `tag_ids`, `tags`

### Roadmaps `/api/roadmaps/`
- `GET /api/roadmaps/` - List all roadmaps
- `POST /api/roadmaps/` - Create roadmap (multipart)
- `GET /api/roadmaps/{id}/` - Get single roadmap
- `PUT/PATCH /api/roadmaps/{id}/` - Update roadmap
- `DELETE /api/roadmaps/{id}/` - Delete roadmap

**Fields:** `icon_name`, `title`, `description`, `content` (HTML), `author_name`, `published_date`

> Roadmaps are text-first and do not include images.

### Events `/api/events/`
- `GET /api/events/` - List all events
- `POST /api/events/` - Create event (multipart)
- `GET /api/events/{id}/` - Get single event
- `PUT/PATCH /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event

**Fields:** `title`, `summary`, `content` (HTML), `image`, `author_name`, `event_date`

### Team Members `/api/team/`
- `GET /api/team/` - List all team members (read-only)
- `GET /api/team/{id}/` - Get single team member

**Fields:** `name`, `role`, `photo`, `bio`, `skills`, `skills_list` (array), `position_rank`, `github_url`, `linkedin_url`, `instagram_url`, `twitter_url`, `website_url`

### Tags `/api/tags/`
- `GET /api/tags/` - List all tags (read-only)

## 🖼️ Working with Images

Use **multipart/form-data** for uploads:

```javascript
const formData = new FormData();
formData.append('title', 'My Post');
formData.append('content', '<p>Content</p>');
formData.append('author_name', 'John Doe');
formData.append('image', imageFile);  // From <input type="file">

fetch('http://127.0.0.1:8000/api/blog/', {
  method: 'POST',
  body: formData
});
```

## 📖 Documentation Files

- **`COMPLETE_FRONTEND_API_GUIDE.md`** - Complete React examples for all endpoints
- **`API_GUIDE.md`** - Detailed API usage with examples
- **`FRONTEND_INTEGRATION_GUIDE.md`** - How to connect your frontend
- **`test_api.html`** - Live test page (open in browser after starting server)

## 🧪 Testing the API

1. Start the server: `python manage.py runserver`
2. Open `test_api.html` in your browser
3. Or use the Django browsable API: http://127.0.0.1:8000/api/

## 🔑 Admin Panel

Access at: `http://127.0.0.1:8000/admin/`

Use this to:
- Add/edit blog posts, projects, roadmaps, events
- Manage team members (with skills and social links)
- Create tags
- Rich text editing for content

## 🌐 CORS Configuration

Frontend allowed origins (in `settings.py`):
- `http://localhost:5173`
- `http://127.0.0.1:5173`

Add more origins if needed.

## ✨ Key Features

✅ Rich text content (CKEditor)
✅ Image uploads (stored in `/media/`)
✅ Author name and dates on all content
✅ Tags for categorization
✅ Team member skills and social links
✅ Full CRUD for blogs, projects, roadmaps, events
✅ Automatic timestamp handling

## 🧹 Maintenance Notes

- Update `SITE_NAME` in `backend_core/settings.py` if branding changes.
- Keep API examples in `COMPLETE_FRONTEND_API_GUIDE.md` up to date when fields change.
- Avoid editing files under `venv/` or `.idea/` — those are environment-specific.
