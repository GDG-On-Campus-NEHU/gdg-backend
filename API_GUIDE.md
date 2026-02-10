# API Response Examples & Image Upload Guide

## How Author Name and Date Are Sent to Frontend

The serializers automatically include `author_name` and date fields in API responses. Here's what the frontend receives:

### Example: GET /api/blog/

**Request:**
```bash
GET http://127.0.0.1:8000/api/blog/
```

**Response (JSON):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Robotics",
    "summary": "A beginner's guide to robotics",
    "content": "<p><strong>Learn</strong> about robots!</p>",
    "image": "http://127.0.0.1:8000/media/blog_images/robot.jpg",
    "tags": [
      {"name": "Robotics"},
      {"name": "AI"}
    ],
    "author_name": "GDG NEHU Team",
    "published_date": "2026-02-10T14:30:00Z"
  }
]
```

### Example: GET /api/projects/

**Response:**
```json
[
  {
    "id": 1,
    "title": "Smart Home System",
    "description": "IoT project",
    "content": "<p>Details about the project...</p>",
    "image": "http://127.0.0.1:8000/media/project_images/smart_home.jpg",
    "tags": [{"name": "IoT"}],
    "author_name": "GDG NEHU Projects Team",
    "published_date": "2026-02-09T10:00:00Z"
  }
]
```

### Example: GET /api/events/

**Response:**
```json
[
  {
    "id": 1,
    "title": "Workshop on Machine Learning",
    "summary": "Hands-on ML workshop",
    "content": "<p>Workshop details...</p>",
    "image": "http://127.0.0.1:8000/media/event_images/workshop.jpg",
    "author_name": "GDG NEHU Events Team",
    "event_date": "2026-02-15T18:00:00Z"
  }
]
```

---

## Roadmaps (Text-only)

Roadmaps intentionally do not include images. Use `icon_name`, `description`, and `content` instead.

---

## How to Add Images in Blog (and other content)

There are **3 ways** to add images:

### Method 1: Using Django Admin (Easiest)

1. Go to http://127.0.0.1:8000/admin/
2. Click on "Blog posts" (or Projects/Events/Roadmaps)
3. Click "Add Blog Post"
4. Fill in the fields:
   - Title
   - Summary
   - Content (use the rich text editor)
   - **Image**: Click "Choose File" and upload
   - Author name
   - Tags
5. Click "Save"

### Method 2: Using curl (Command Line)

**Create a blog post with image:**

```powershell
# PowerShell example
curl -X POST http://127.0.0.1:8000/api/blog/ `
  -F "title=My First Blog Post" `
  -F "summary=This is a short summary" `
  -F "content=<p><strong>Hello</strong> from the blog!</p>" `
  -F "author_name=GDG NEHU Team" `
  -F "image=@C:\path\to\your\image.jpg"
```

**Response:**
```json
{
  "id": 2,
  "title": "My First Blog Post",
  "summary": "This is a short summary",
  "content": "<p><strong>Hello</strong> from the blog!</p>",
  "image": "http://127.0.0.1:8000/media/blog_images/image.jpg",
  "tags": [],
  "author_name": "GDG NEHU Team",
  "published_date": "2026-02-10T15:00:00Z"
}
```

### Method 3: Using JavaScript/Fetch (Frontend)

**Example for your React/Vue/vanilla JS frontend:**

```javascript
// Create FormData for multipart upload
const formData = new FormData();
formData.append('title', 'My Blog Post');
formData.append('summary', 'Short summary here');
formData.append('content', '<p>Rich text content</p>');
formData.append('author_name', 'GDG NEHU Team');

// Get image from file input
const fileInput = document.querySelector('input[type="file"]');
if (fileInput.files[0]) {
  formData.append('image', fileInput.files[0]);
}

// Optional: add tags
formData.append('tag_ids', [1, 2]); // Tag IDs

// Send to API
fetch('http://127.0.0.1:8000/api/blog/', {
  method: 'POST',
  body: formData,
  // Note: Don't set Content-Type header - browser sets it automatically with boundary
})
  .then(response => response.json())
  .then(data => {
    console.log('Created blog post:', data);
    console.log('Image URL:', data.image);
    console.log('Author:', data.author_name);
    console.log('Published:', data.published_date);
  });
```

**React example:**

```jsx
import React, { useState } from 'react';

function BlogUploadForm() {
  const [file, setFile] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', e.target.title.value);
    formData.append('summary', e.target.summary.value);
    formData.append('content', e.target.content.value);
    formData.append('author_name', e.target.author.value);
    
    if (file) {
      formData.append('image', file);
    }
    
    const response = await fetch('http://127.0.0.1:8000/api/blog/', {
      method: 'POST',
      body: formData,
    });
    
    const data = await response.json();
    console.log('Blog created:', data);
    // data.image will contain the full URL
    // data.author_name will contain the author
    // data.published_date will contain the timestamp
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="title" placeholder="Title" required />
      <input name="summary" placeholder="Summary" required />
      <textarea name="content" placeholder="Content (HTML)" required />
      <input name="author" placeholder="Author Name" required />
      <input 
        type="file" 
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit">Create Blog Post</button>
    </form>
  );
}
```

---

## Important Notes

### Image URLs
- Images are automatically served at: `http://127.0.0.1:8000/media/{folder}/{filename}`
- The API response gives you the **full URL** in the `image` field
- Just use `data.image` directly in your `<img>` tag

### CORS
Your Django settings already allow requests from:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

If your frontend runs on a different port, add it to `CORS_ALLOWED_ORIGINS` in `settings.py`.

### File Size & Types
- Django accepts common image formats: JPG, PNG, GIF, WEBP
- No file size limit is set by default (you can add one if needed)

---

## Complete Example: Create + Display Flow

### 1. Create blog post with image (Frontend)

```javascript
const formData = new FormData();
formData.append('title', 'New Post');
formData.append('summary', 'Summary');
formData.append('content', '<p>Content</p>');
formData.append('author_name', 'Rohit');
formData.append('image', imageFile);

const response = await fetch('http://127.0.0.1:8000/api/blog/', {
  method: 'POST',
  body: formData
});

const newPost = await response.json();
```

### 2. Fetch and display (Frontend)

```javascript
// Fetch all blog posts
const response = await fetch('http://127.0.0.1:8000/api/blog/');
const posts = await response.json();

// Display in HTML
posts.forEach(post => {
  const html = `
    <article>
      <h2>${post.title}</h2>
      <p>By ${post.author_name} on ${new Date(post.published_date).toLocaleDateString()}</p>
      <img src="${post.image}" alt="${post.title}" />
      <p>${post.summary}</p>
      <div>${post.content}</div>
    </article>
  `;
  document.getElementById('blog-container').innerHTML += html;
});
```

---

## Same Pattern for Projects, Events, Roadmaps

All content types work the same way:

- **Projects**: POST to `/api/projects/` with same multipart format
- **Events**: POST to `/api/events/` 
- **Roadmaps**: POST to `/api/roadmaps/`

They all include `author_name`, date fields, `image`, and `content` in responses.

---

## Testing with Postman

1. Open Postman
2. Create new request: POST `http://127.0.0.1:8000/api/blog/`
3. Go to "Body" tab
4. Select "form-data"
5. Add fields:
   - `title` (text): "Test Post"
   - `summary` (text): "Summary"
   - `content` (text): "<p>Content</p>"
   - `author_name` (text): "Rohit"
   - `image` (file): Select image file
6. Click "Send"

Response will include all fields including `author_name`, `published_date`, and the full `image` URL.
