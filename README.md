# Backend API

This project is a Django REST API for **Google Developer's Group, NEHU** (GDG NEHU) with blogs, projects, roadmaps, events, and team members.

## 🎯 Key Features

- **External Image Hosting**: Uses Imgur/Cloudinary for images (zero server storage costs!)
- **Rich Text Editing**: CKEditor integration for blog posts, projects, events, and roadmaps
- **RESTful API**: Full CRUD operations for all content types
- **Tag System**: Organize content with reusable tags
- **Team Management**: Team member profiles with skills and social links

## 🚀 Setup

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
- `POST /api/blog/` - Create blog post
- `GET /api/blog/{id}/` - Get single blog post
- `PUT/PATCH /api/blog/{id}/` - Update blog post
- `DELETE /api/blog/{id}/` - Delete blog post

**Fields:** `title`, `summary`, `content` (HTML), `image_url`, `author_name`, `published_date`, `tag_ids`, `tags`

### Projects `/api/projects/`
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get single project
- `PUT/PATCH /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

**Fields:** `title`, `description`, `content` (HTML), `image_url`, `author_name`, `published_date`, `tag_ids`, `tags`

### Roadmaps `/api/roadmaps/`
- `GET /api/roadmaps/` - List all roadmaps
- `POST /api/roadmaps/` - Create roadmap
- `GET /api/roadmaps/{id}/` - Get single roadmap
- `PUT/PATCH /api/roadmaps/{id}/` - Update roadmap
- `DELETE /api/roadmaps/{id}/` - Delete roadmap

**Fields:** `icon_name`, `title`, `description`, `content` (HTML), `author_name`, `published_date`

> Roadmaps are text-first and do not include images.

### Events `/api/events/`
- `GET /api/events/` - List all events
- `POST /api/events/` - Create event
- `GET /api/events/{id}/` - Get single event
- `PUT/PATCH /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event

**Fields:** `title`, `summary`, `content` (HTML), `image_url`, `author_name`, `event_date`

### Team Members `/api/team/`
- `GET /api/team/` - List all team members (sorted by position_rank)
- `GET /api/team/{id}/` - Get single team member

**Fields:** `name`, `role`, `photo_url`, `bio`, `skills`, `skills_list` (array), `position_rank`, `github_url`, `linkedin_url`, `instagram_url`, `twitter_url`, `website_url`

### Tags `/api/tags/`
- `GET /api/tags/` - List all tags (read-only)

## 🖼️ Working with Images

**This backend uses external image hosting (Imgur, Cloudinary, etc.) to minimize storage costs.**

### For Admins
1. Upload images to Imgur: https://imgur.com/upload
2. Copy the direct image URL (right-click → Copy Image Address)
3. Paste the URL in the Django admin panel

### For Frontend Developers
All image fields return direct URLs - use them directly:

```javascript
// Create a blog post with an image
fetch('http://127.0.0.1:8000/api/blog/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'My Post',
    summary: 'Short summary',
    content: '<p>Rich text content</p>',
    image_url: 'https://i.imgur.com/example.jpg',
    author_name: 'John Doe',
    tag_ids: [1, 2]
  })
});

// Display the image
<img src={blog.image_url} alt={blog.title} />
```

**See `IMAGE_HOSTING_GUIDE.md` for detailed instructions on image hosting.**

## 📖 Documentation Files

- **`IMAGE_HOSTING_GUIDE.md`** - Complete guide to external image hosting
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
- Add/edit blog posts, projects, roadmaps, events, team members
- Manage tags
- Add image URLs from external hosting services

## 💡 Why External Image Hosting?

✅ **Zero storage costs** on free-tier deployments  
✅ **No bandwidth charges** - images served from CDN  
✅ **Better performance** - global CDN delivery  
✅ **Easier deployment** - no media file management  
✅ **Smaller backups** - database-only backups
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
