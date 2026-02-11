# Quick JSON Schema Reference

## All API Endpoints

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/blog/` | GET | Blog posts with `image_url` |
| `/api/projects/` | GET | Projects with `image_url` |
| `/api/team/` | GET | Team members with `photo_url` |
| `/api/events/` | GET | Events with `image_url` |
| `/api/roadmaps/` | GET | Roadmaps (no images) |
| `/api/tags/` | GET | Tags |

---

## Quick Reference

### Blog Post
```json
{
  "id": 1,
  "title": "string",
  "summary": "string",
  "content": "HTML string",
  "image_url": "https://i.imgur.com/...",
  "tags": [{"name": "Python"}],
  "author_name": "string",
  "published_date": "2024-02-11T10:30:00Z"
}
```

### Project
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "content": "HTML string",
  "image_url": "https://i.imgur.com/...",
  "tags": [{"name": "Mobile"}],
  "author_name": "string",
  "published_date": "2024-02-11T10:30:00Z"
}
```

### Team Member
```json
{
  "id": 1,
  "name": "string",
  "role": "string",
  "photo_url": "https://i.imgur.com/...",
  "bio": "string",
  "skills": "Python, React, Django",
  "skills_list": ["Python", "React", "Django"],
  "position_rank": 1,
  "github_url": "https://github.com/...",
  "linkedin_url": "https://linkedin.com/in/...",
  "instagram_url": "",
  "twitter_url": "",
  "website_url": ""
}
```

### Event
```json
{
  "id": 1,
  "title": "string",
  "summary": "string",
  "content": "HTML string",
  "image_url": "https://i.imgur.com/...",
  "author_name": "string",
  "event_date": "2024-03-15T14:00:00Z"
}
```

### Roadmap
```json
{
  "id": 1,
  "icon_name": "🤖",
  "title": "string",
  "description": "string",
  "content": "HTML string",
  "author_name": "string",
  "published_date": "2024-02-01T09:00:00Z"
}
```

---

## Key Points

✅ **All image fields use external URLs** (Imgur, Cloudinary)  
✅ **Use `image_url` for blogs/projects/events**  
✅ **Use `photo_url` for team members**  
✅ **Dates are ISO 8601 format**  
✅ **Content fields contain HTML**  

---

## TypeScript Types

```typescript
interface BlogPost {
  id: number;
  title: string;
  summary: string;
  content: string;
  image_url: string;
  tags: Array<{name: string}>;
  author_name: string;
  published_date: string;
}

interface Project {
  id: number;
  title: string;
  description: string;
  content: string;
  image_url: string;
  tags: Array<{name: string}>;
  author_name: string;
  published_date: string;
}

interface TeamMember {
  id: number;
  name: string;
  role: string;
  photo_url: string;
  bio: string;
  skills: string;
  skills_list: string[];
  position_rank: number;
  github_url: string;
  linkedin_url: string;
  instagram_url: string;
  twitter_url: string;
  website_url: string;
}
```

---

## React Example

```tsx
// Fetch and display
const [blogs, setBlogs] = useState<BlogPost[]>([]);

useEffect(() => {
  fetch('http://localhost:8000/api/blog/')
    .then(r => r.json())
    .then(setBlogs);
}, []);

return (
  <div>
    {blogs.map(blog => (
      <div key={blog.id}>
        <img src={blog.image_url} alt={blog.title} />
        <h2>{blog.title}</h2>
        <p>{blog.summary}</p>
      </div>
    ))}
  </div>
);
```

---

**Full documentation:** See `FRONTEND_JSON_SCHEMA.md`

