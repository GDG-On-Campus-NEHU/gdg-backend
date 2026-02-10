# 📸 Complete Guide: How Data Flows to Frontend

## 🔍 Quick Answer

### How author_name and date are sent to frontend:
✅ **Automatically included in every API response**

The serializers in `landing_page/serializers.py` define these fields:

```python
# BlogPostSerializer
fields = ['id', 'title', 'summary', 'content', 'image', 'tags', 'tag_ids', 'author_name', 'published_date']
```

When you call `GET /api/blog/`, Django REST Framework automatically converts the BlogPost model to JSON and includes `author_name` and `published_date`.

### How to add images:
✅ **Use multipart/form-data when POSTing**

---

## 📊 Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND (React/Vue/etc)                                   │
│                                                              │
│  1. User uploads image + fills form                         │
│  2. JavaScript creates FormData                             │
│  3. fetch() sends POST to /api/blog/                       │
└────────────────────┬────────────────────────────────────────┘
                     │ 
                     │ HTTP POST (multipart/form-data)
                     │ Content: title, summary, content, 
                     │          author_name, image file
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  DJANGO BACKEND                                             │
│                                                              │
│  BlogPostViewSet → BlogPostSerializer                       │
│                                                              │
│  1. Validates data                                          │
│  2. Saves image to media/blog_images/                      │
│  3. Creates BlogPost in database                            │
│  4. Returns JSON with all fields                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP 201 Response (JSON)
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND receives:                                         │
│                                                              │
│  {                                                          │
│    "id": 1,                                                 │
│    "title": "My Post",                                     │
│    "summary": "Summary",                                    │
│    "content": "<p>Rich text</p>",                          │
│    "image": "http://127.0.0.1:8000/media/blog_images/x.jpg"│
│    "author_name": "GDG NEHU Team",         ← HERE             │
│    "published_date": "2026-02-10T14:30:00Z"  ← HERE        │
│  }                                                          │
│                                                              │
│  3. Display in UI using data.author_name, data.image       │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Examples

### Example 1: Plain JavaScript (Vanilla)

```html
<!DOCTYPE html>
<html>
<body>
  <h2>Create Blog Post</h2>
  <form id="blogForm">
    <input type="text" id="title" placeholder="Title" required><br>
    <textarea id="summary" placeholder="Summary" required></textarea><br>
    <textarea id="content" placeholder="Content (HTML)" required></textarea><br>
    <input type="text" id="author" placeholder="Author Name" required><br>
    <input type="file" id="image" accept="image/*"><br>
    <button type="submit">Submit</button>
  </form>

  <div id="result"></div>

  <script>
    document.getElementById('blogForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      // Create FormData (handles multipart automatically)
      const formData = new FormData();
      formData.append('title', document.getElementById('title').value);
      formData.append('summary', document.getElementById('summary').value);
      formData.append('content', document.getElementById('content').value);
      formData.append('author_name', 'GDG NEHU Team');
      
      const imageFile = document.getElementById('image').files[0];
      if (imageFile) {
        formData.append('image', imageFile);
      }
      
      // Send to API
      const response = await fetch('http://127.0.0.1:8000/api/blog/', {
        method: 'POST',
        body: formData
        // Don't set Content-Type - browser does it automatically with boundary
      });
      
      const data = await response.json();
      
      // Display result - author_name and published_date are automatically included
      document.getElementById('result').innerHTML = `
        <h3>Created!</h3>
        <p><strong>ID:</strong> ${data.id}</p>
        <p><strong>Author:</strong> ${data.author_name}</p>
        <p><strong>Published:</strong> ${data.published_date}</p>
        <p><strong>Image:</strong> <img src="${data.image}" width="200"></p>
      `;
    });
  </script>
</body>
</html>
```

### Example 2: React with Hooks

```jsx
import React, { useState, useEffect } from 'react';

function BlogManager() {
  const [blogs, setBlogs] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    summary: '',
    content: '',
    author_name: ''
  });
  const [imageFile, setImageFile] = useState(null);

  // Fetch blogs (author_name and published_date come automatically)
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/blog/')
      .then(res => res.json())
      .then(data => setBlogs(data));
  }, []);

  // Create blog with image
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formDataToSend = new FormData();
    Object.keys(formData).forEach(key => {
      formDataToSend.append(key, formData[key]);
    });
    
    if (imageFile) {
      formDataToSend.append('image', imageFile);
    }
    
    const response = await fetch('http://127.0.0.1:8000/api/blog/', {
      method: 'POST',
      body: formDataToSend
    });
    
    const newBlog = await response.json();
    setBlogs([newBlog, ...blogs]); // Add to list
  };

  return (
    <div>
      <h2>Create Blog</h2>
      <form onSubmit={handleSubmit}>
        <input 
          placeholder="Title"
          value={formData.title}
          onChange={e => setFormData({...formData, title: e.target.value})}
        />
        <textarea 
          placeholder="Summary"
          value={formData.summary}
          onChange={e => setFormData({...formData, summary: e.target.value})}
        />
        <textarea 
          placeholder="Content"
          value={formData.content}
          onChange={e => setFormData({...formData, content: e.target.value})}
        />
        <input 
          placeholder="Author Name"
          value={formData.author_name}
          onChange={e => setFormData({...formData, author_name: e.target.value})}
        />
        <input 
          type="file" 
          accept="image/*"
          onChange={e => setImageFile(e.target.files[0])}
        />
        <button type="submit">Create</button>
      </form>

      <h2>Blog Posts</h2>
      {blogs.map(blog => (
        <article key={blog.id}>
          <h3>{blog.title}</h3>
          {/* Author name and date are automatically in the response */}
          <p>By {blog.author_name} on {new Date(blog.published_date).toLocaleDateString()}</p>
          {blog.image && <img src={blog.image} alt={blog.title} style={{maxWidth: '200px'}} />}
          <p>{blog.summary}</p>
          <div dangerouslySetInnerHTML={{__html: blog.content}} />
        </article>
      ))}
    </div>
  );
}
```

### Example 3: Vue 3 Composition API

```vue
<template>
  <div>
    <h2>Create Blog Post</h2>
    <form @submit.prevent="createBlog">
      <input v-model="title" placeholder="Title" required>
      <textarea v-model="summary" placeholder="Summary" required></textarea>
      <textarea v-model="content" placeholder="Content" required></textarea>
      <input v-model="authorName" placeholder="Author Name" required>
      <input type="file" @change="handleFileChange" accept="image/*">
      <button type="submit">Submit</button>
    </form>

    <h2>Blog Posts</h2>
    <article v-for="blog in blogs" :key="blog.id">
      <h3>{{ blog.title }}</h3>
      <!-- author_name and published_date come from API automatically -->
      <p>By {{ blog.author_name }} on {{ formatDate(blog.published_date) }}</p>
      <img v-if="blog.image" :src="blog.image" :alt="blog.title" style="max-width: 200px">
      <p>{{ blog.summary }}</p>
      <div v-html="blog.content"></div>
    </article>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const blogs = ref([]);
const title = ref('');
const summary = ref('');
const content = ref('');
const authorName = ref('');
const imageFile = ref(null);

onMounted(async () => {
  const response = await fetch('http://127.0.0.1:8000/api/blog/');
  blogs.value = await response.json();
});

const handleFileChange = (event) => {
  imageFile.value = event.target.files[0];
};

const createBlog = async () => {
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('summary', summary.value);
  formData.append('content', content.value);
  formData.append('author_name', authorName.value);
  
  if (imageFile.value) {
    formData.append('image', imageFile.value);
  }
  
  const response = await fetch('http://127.0.0.1:8000/api/blog/', {
    method: 'POST',
    body: formData
  });
  
  const newBlog = await response.json();
  blogs.value.unshift(newBlog);
  
  // Reset form
  title.value = '';
  summary.value = '';
  content.value = '';
  authorName.value = '';
  imageFile.value = null;
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};
</script>
```

---

## 🧪 Test It Right Now

### Step 1: Make sure server is running
```powershell
python manage.py runserver
```

### Step 2: Run the test script I created
```powershell
python test_image_upload.py
```

This will:
1. Create a test image
2. Upload it to `/api/blog/`
3. Show you the response with `author_name`, `published_date`, and `image` URL

### Step 3: Verify in browser
Open: http://127.0.0.1:8000/api/blog/

You'll see JSON with all fields including `author_name` and dates.

---

## 🎯 Key Points

1. **author_name and dates are ALWAYS sent** - they're in the serializer fields list
2. **Images must use FormData** - not JSON
3. **Image URLs are absolute** - ready to use in `<img src>`
4. **No special code needed** - Django REST Framework handles serialization automatically

---

## 🐛 Troubleshooting

### "Image field is empty in response"
- Make sure you're using `FormData`, not JSON
- Check file input has `accept="image/*"`

### "CORS error"
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py
- Already added: localhost:5173 and 127.0.0.1:5173

### "Can't see author_name in response"
- It's there! Check the serializer includes it in `fields` list
- Look at the test above - it prints the exact response

---

## 📱 Test with curl (Quick)

```bash
# Create blog with image
curl -X POST http://127.0.0.1:8000/api/blog/ \
  -F "title=Quick Test" \
  -F "summary=Test summary" \
  -F "content=<p>Test</p>" \
  -F "author_name=Rohit" \
  -F "image=@path/to/image.jpg"

# Get all blogs (will show author_name and published_date)
curl http://127.0.0.1:8000/api/blog/
```

That's it! The backend is fully wired to send everything to your frontend.
