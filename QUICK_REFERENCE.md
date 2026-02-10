# 🎯 Quick API Reference Card

> **Maintainer note:** This quick reference is for **Google Developer's Group, NEHU (GDG NEHU)**. Update `SITE_NAME` in `backend_core/settings.py` if branding changes.
> Keep examples aligned with serializer fields when you add or remove model fields.

Copy-paste these into your frontend code!

---

## 📞 API Calls

```javascript
const API = 'http://127.0.0.1:8000/api';

// Blogs
const blogs = await fetch(`${API}/blog/`).then(r => r.json());
const blog = await fetch(`${API}/blog/1/`).then(r => r.json());

// Projects
const projects = await fetch(`${API}/projects/`).then(r => r.json());
const project = await fetch(`${API}/projects/1/`).then(r => r.json());

// Roadmaps
const roadmaps = await fetch(`${API}/roadmaps/`).then(r => r.json());
const roadmap = await fetch(`${API}/roadmaps/1/`).then(r => r.json());

// Events
const events = await fetch(`${API}/events/`).then(r => r.json());
const event = await fetch(`${API}/events/1/`).then(r => r.json());

// Team
const team = await fetch(`${API}/team/`).then(r => r.json());
const member = await fetch(`${API}/team/1/`).then(r => r.json());
```

---

## 🎨 Display Snippets

### Blog Card
```jsx
<div className="blog-card">
  <img src={blog.image} alt={blog.title} />
  <h3>{blog.title}</h3>
  <p>{blog.summary}</p>
  <span>By {blog.author_name}</span>
  <span>{new Date(blog.published_date).toLocaleDateString()}</span>
</div>
```

### Project Card
```jsx
<div className="project-card">
  <img src={project.image} alt={project.title} />
  <h3>{project.title}</h3>
  <p>{project.description}</p>
  <div>
    {project.tags.map(tag => (
      <span key={tag.name}>{tag.name}</span>
    ))}
  </div>
</div>
```

### Event Card
```jsx
<div className="event-card">
  <img src={event.image} alt={event.title} />
  <h3>{event.title}</h3>
  <p>{event.summary}</p>
  <time>{new Date(event.event_date).toLocaleString()}</time>
  <span>By {event.author_name || 'GDG NEHU Team'}</span>
</div>
```

### Team Member Card (with Skills & Social Links!)
```jsx
import { FaGithub, FaLinkedin, FaInstagram } from 'react-icons/fa';

<div className="team-card">
  <img src={member.photo} alt={member.name} />
  <h3>{member.name}</h3>
  <p>{member.role}</p>
  <p>{member.bio}</p>
  
  {/* Skills as badges */}
  <div className="skills">
    {member.skills_list.map(skill => (
      <span key={skill} className="skill-badge">{skill}</span>
    ))}
  </div>
  
  {/* Social links */}
  <div className="social">
    {member.github_url && (
      <a href={member.github_url} target="_blank">
        <FaGithub />
      </a>
    )}
    {member.linkedin_url && (
      <a href={member.linkedin_url} target="_blank">
        <FaLinkedin />
      </a>
    )}
    {member.instagram_url && (
      <a href={member.instagram_url} target="_blank">
        <FaInstagram />
      </a>
    )}
  </div>
</div>
```

### Roadmap Card
```jsx
<div className="roadmap-card">
  <span className="icon">{roadmap.icon_name}</span>
  <h3>{roadmap.title}</h3>
  <p>{roadmap.description}</p>
</div>
```

> Roadmaps are text-first and do not include images.

---

## 📦 What Each Response Contains

### Blog Response
```json
{
  "id": 1,
  "title": "string",
  "summary": "string",
  "content": "<p>HTML</p>",
  "image": "http://127.0.0.1:8000/media/...",
  "tags": [{"name": "tag1"}],
  "author_name": "GDG NEHU Team",
  "published_date": "2026-02-10T10:00:00Z"
}
```

### Project Response
```json
{
  "id": 1,
  "title": "string",
  "description": "string",
  "content": "<p>HTML</p>",
  "image": "http://127.0.0.1:8000/media/...",
  "tags": [{"name": "tag1"}],
  "author_name": "GDG NEHU Projects Team",
  "published_date": "2026-02-10T10:00:00Z"
}
```

### Event Response
```json
{
  "id": 1,
  "title": "string",
  "summary": "string",
  "content": "<p>HTML</p>",
  "image": "http://127.0.0.1:8000/media/...",
  "author_name": "GDG NEHU Events Team",
  "event_date": "2026-02-10T18:00:00Z"
}
```

### Team Member Response ⭐
```json
{
  "id": 1,
  "name": "string",
  "role": "string",
  "photo": "http://127.0.0.1:8000/media/...",
  "bio": "GDG NEHU community member and mentor.",
  "skills": "Python, Django, React",
  "skills_list": ["Python", "Django", "React"],
  "position_rank": 1,
  "github_url": "https://github.com/...",
  "linkedin_url": "https://linkedin.com/...",
  "instagram_url": "https://instagram.com/...",
  "twitter_url": "https://twitter.com/...",
  "website_url": "https://..."
}
```

### Roadmap Response
```json
{
  "id": 1,
  "icon_name": "🤖",
  "title": "string",
  "description": "string",
  "content": "<p>HTML</p>",
  "author_name": "string",
  "published_date": "2026-02-10T10:00:00Z"
}
```

---

## 🎨 Quick CSS

```css
.skill-badge {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  margin: 2px;
  display: inline-block;
}

.social a {
  color: #333;
  margin: 0 8px;
  font-size: 1.5rem;
}

.social a:hover {
  color: #1976d2;
}
```

---

## 🚀 Install React Icons

```bash
npm install react-icons
```

Then import:
```javascript
import { FaGithub, FaLinkedin, FaInstagram, FaTwitter, FaGlobe } from 'react-icons/fa';
```

---

## ⚡ Quick Test

Open: **`test_api.html`** in your browser to see all data!

---

## 🧹 Maintainer Note

If you update branding, adjust `SITE_NAME` in `backend_core/settings.py` and refresh examples here.

---

**That's it! All endpoints are ready. Just fetch and display!** 🎉
