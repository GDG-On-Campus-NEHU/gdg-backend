# 🚀 Complete API Data Reference for Frontend

## 📋 Quick Reference: All Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/blog/` | GET | List all blog posts |
| `/api/blog/{id}/` | GET | Get single blog post |
| `/api/projects/` | GET | List all projects |
| `/api/projects/{id}/` | GET | Get single project |
| `/api/roadmaps/` | GET | List all roadmaps |
| `/api/roadmaps/{id}/` | GET | Get single roadmap |
| `/api/events/` | GET | List all events |
| `/api/events/{id}/` | GET | Get single event |
| `/api/team/` | GET | List all team members |
| `/api/team/{id}/` | GET | Get single team member |

---

## 📊 Complete JSON Response Examples

### 1. Blog Posts - `/api/blog/`

```json
[
  {
    "id": 1,
    "title": "Getting Started with Robotics",
    "summary": "A beginner's guide to building your first robot",
    "content": "<p><strong>Introduction</strong></p><p>Learn how to build robots...</p>",
    "image": "http://127.0.0.1:8000/media/blog_images/robot.jpg",
    "tags": [
      {"name": "Robotics"},
      {"name": "Tutorial"}
    ],
    "author_name": "Rohit Shaw",
    "published_date": "2026-02-10T10:30:00Z"
  }
]
```

### 2. Projects - `/api/projects/`

```json
[
  {
    "id": 1,
    "title": "Smart Home Automation System",
    "description": "IoT-based home automation with voice control",
    "content": "<p><strong>Project Overview</strong></p><p>This project uses Arduino and ESP32...</p>",
    "image": "http://127.0.0.1:8000/media/project_images/smart_home.jpg",
    "tags": [
      {"name": "IoT"},
      {"name": "Arduino"}
    ],
    "author_name": "Alex Doe",
    "published_date": "2026-02-05T14:00:00Z"
  }
]
```

### 3. Roadmaps - `/api/roadmaps/`

```json
[
  {
    "id": 1,
    "icon_name": "🤖",
    "title": "Robotics Learning Path",
    "description": "Complete roadmap from beginner to advanced robotics",
    "content": "<h3>Phase 1: Basics</h3><p>Learn about sensors, motors...</p>",
    "author_name": "Tech Team",
    "published_date": "2026-02-01T09:00:00Z"
  }
]
```

### 4. Events - `/api/events/`

```json
[
  {
    "id": 1,
    "title": "AI/ML Workshop 2026",
    "summary": "Hands-on workshop on machine learning fundamentals",
    "content": "<p><strong>Workshop Details</strong></p><p>Join us for an intensive 3-day workshop...</p>",
    "image": "http://127.0.0.1:8000/media/event_images/workshop.jpg",
    "author_name": "Events Team",
    "event_date": "2026-03-15T18:00:00Z"
  }
]
```

### 5. Team Members - `/api/team/`

```json
[
  {
    "id": 1,
    "name": "Rohit Shaw",
    "role": "President",
    "photo": "http://127.0.0.1:8000/media/team_photos/rohit.jpg",
    "bio": "Passionate about robotics and AI. Leading the GDG NEHU community since 2024.",
    "skills": "Python, Django, React, Robotics, AI/ML",
    "skills_list": ["Python", "Django", "React", "Robotics", "AI/ML"],
    "position_rank": 1,
    "github_url": "https://github.com/rohitshaw",
    "linkedin_url": "https://linkedin.com/in/rohitshaw",
    "instagram_url": "https://instagram.com/rohitshaw",
    "twitter_url": "https://twitter.com/rohitshaw",
    "website_url": "https://rohitshaw.dev"
  }
]
```

---

## 💻 Complete React Components

### Blog List & Detail Pages

```jsx
// BlogList.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function BlogList() {
  const [blogs, setBlogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/blog/')
      .then(res => res.json())
      .then(data => {
        setBlogs(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading blogs...</div>;

  return (
    <div className="blog-list">
      <h1>Latest Blogs</h1>
      <div className="blog-grid">
        {blogs.map(blog => (
          <article key={blog.id} className="blog-card">
            <Link to={`/blog/${blog.id}`}>
              {blog.image && (
                <img src={blog.image} alt={blog.title} className="blog-image" />
              )}
              <h2>{blog.title}</h2>
              <p className="blog-meta">
                By {blog.author_name} • {new Date(blog.published_date).toLocaleDateString()}
              </p>
              <p className="blog-summary">{blog.summary}</p>
              <div className="blog-tags">
                {blog.tags.map((tag, idx) => (
                  <span key={idx} className="tag">{tag.name}</span>
                ))}
              </div>
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}

// BlogDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function BlogDetail() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/blog/${id}/`)
      .then(res => res.json())
      .then(data => {
        setBlog(data);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (!blog) return <div>Blog not found</div>;

  return (
    <article className="blog-detail">
      <h1>{blog.title}</h1>
      <div className="blog-meta">
        <span>By {blog.author_name}</span>
        <span>{new Date(blog.published_date).toLocaleDateString()}</span>
      </div>
      {blog.image && <img src={blog.image} alt={blog.title} className="featured-image" />}
      <div className="blog-tags">
        {blog.tags.map((tag, idx) => (
          <span key={idx} className="tag">{tag.name}</span>
        ))}
      </div>
      <div className="blog-content" dangerouslySetInnerHTML={{ __html: blog.content }} />
    </article>
  );
}

export { BlogList, BlogDetail };
```

### Projects List & Detail Pages

```jsx
// ProjectList.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function ProjectList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/projects/')
      .then(res => res.json())
      .then(data => setProjects(data));
  }, []);

  return (
    <div className="project-list">
      <h1>Our Projects</h1>
      <div className="project-grid">
        {projects.map(project => (
          <div key={project.id} className="project-card">
            <Link to={`/projects/${project.id}`}>
              {project.image && (
                <img src={project.image} alt={project.title} />
              )}
              <h3>{project.title}</h3>
              <p>{project.description}</p>
              <div className="project-meta">
                <span>By {project.author_name}</span>
                <span>{new Date(project.published_date).toLocaleDateString()}</span>
              </div>
              <div className="tags">
                {project.tags.map((tag, idx) => (
                  <span key={idx} className="tag">{tag.name}</span>
                ))}
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

// ProjectDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function ProjectDetail() {
  const { id } = useParams();
  const [project, setProject] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/projects/${id}/`)
      .then(res => res.json())
      .then(data => setProject(data));
  }, [id]);

  if (!project) return <div>Loading...</div>;

  return (
    <div className="project-detail">
      <h1>{project.title}</h1>
      {project.image && <img src={project.image} alt={project.title} className="hero-image" />}
      <div className="project-meta">
        <span>Created by {project.author_name}</span>
        <span>{new Date(project.published_date).toLocaleDateString()}</span>
      </div>
      <div className="tags">
        {project.tags.map((tag, idx) => (
          <span key={idx} className="tag">{tag.name}</span>
        ))}
      </div>
      <div className="project-content" dangerouslySetInnerHTML={{ __html: project.content }} />
    </div>
  );
}

export { ProjectList, ProjectDetail };
```

### Roadmaps Page

```jsx
// RoadmapList.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function RoadmapList() {
  const [roadmaps, setRoadmaps] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/roadmaps/')
      .then(res => res.json())
      .then(data => setRoadmaps(data));
  }, []);

  return (
    <div className="roadmap-list">
      <h1>Learning Roadmaps</h1>
      <div className="roadmap-grid">
        {roadmaps.map(roadmap => (
          <div key={roadmap.id} className="roadmap-card">
            <Link to={`/roadmaps/${roadmap.id}`}>
              <div className="roadmap-icon">{roadmap.icon_name}</div>
              <h3>{roadmap.title}</h3>
              <p>{roadmap.description}</p>
              <p className="author">By {roadmap.author_name}</p>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

// RoadmapDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function RoadmapDetail() {
  const { id } = useParams();
  const [roadmap, setRoadmap] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/roadmaps/${id}/`)
      .then(res => res.json())
      .then(data => setRoadmap(data));
  }, [id]);

  if (!roadmap) return <div>Loading...</div>;

  return (
    <div className="roadmap-detail">
      <div className="roadmap-header">
        <span className="icon">{roadmap.icon_name}</span>
        <h1>{roadmap.title}</h1>
      </div>
      <p className="description">{roadmap.description}</p>
      <div className="roadmap-content" dangerouslySetInnerHTML={{ __html: roadmap.content }} />
      <p className="author">Created by {roadmap.author_name}</p>
    </div>
  );
}

export { RoadmapList, RoadmapDetail };
```

### Events Page

```jsx
// EventList.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function EventList() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/events/')
      .then(res => res.json())
      .then(data => setEvents(data));
  }, []);

  return (
    <div className="event-list">
      <h1>Upcoming Events</h1>
      <div className="event-grid">
        {events.map(event => (
          <div key={event.id} className="event-card">
            <Link to={`/events/${event.id}`}>
              {event.image && <img src={event.image} alt={event.title} />}
              <h3>{event.title}</h3>
              <p className="event-date">
                📅 {new Date(event.event_date).toLocaleDateString()} at{' '}
                {new Date(event.event_date).toLocaleTimeString()}
              </p>
              <p>{event.summary}</p>
              <p className="organizer">Organized by {event.author_name}</p>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

// EventDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function EventDetail() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/events/${id}/`)
      .then(res => res.json())
      .then(data => setEvent(data));
  }, [id]);

  if (!event) return <div>Loading...</div>;

  return (
    <div className="event-detail">
      <h1>{event.title}</h1>
      {event.image && <img src={event.image} alt={event.title} className="event-banner" />}
      <div className="event-info">
        <p className="event-date">
          📅 {new Date(event.event_date).toLocaleDateString()}
          <br />
          🕐 {new Date(event.event_date).toLocaleTimeString()}
        </p>
        <p className="organizer">Organized by {event.author_name}</p>
      </div>
      <div className="event-content" dangerouslySetInnerHTML={{ __html: event.content }} />
    </div>
  );
}

export { EventList, EventDetail };
```

### Team Members Page

```jsx
// TeamList.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaGithub, FaLinkedin, FaInstagram, FaTwitter, FaGlobe } from 'react-icons/fa';

function TeamList() {
  const [team, setTeam] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/team/')
      .then(res => res.json())
      .then(data => setTeam(data));
  }, []);

  return (
    <div className="team-list">
      <h1>Our Team</h1>
      <div className="team-grid">
        {team.map(member => (
          <div key={member.id} className="team-card">
            <Link to={`/team/${member.id}`}>
              <img src={member.photo} alt={member.name} className="team-photo" />
              <h3>{member.name}</h3>
              <p className="role">{member.role}</p>
              
              {/* Skills Preview */}
              {member.skills_list.length > 0 && (
                <div className="skills-preview">
                  {member.skills_list.slice(0, 3).map((skill, idx) => (
                    <span key={idx} className="skill-tag">{skill}</span>
                  ))}
                  {member.skills_list.length > 3 && <span className="more">+{member.skills_list.length - 3}</span>}
                </div>
              )}

              {/* Social Links Preview */}
              <div className="social-links">
                {member.github_url && (
                  <a href={member.github_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    <FaGithub />
                  </a>
                )}
                {member.linkedin_url && (
                  <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    <FaLinkedin />
                  </a>
                )}
                {member.instagram_url && (
                  <a href={member.instagram_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    <FaInstagram />
                  </a>
                )}
                {member.twitter_url && (
                  <a href={member.twitter_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    <FaTwitter />
                  </a>
                )}
                {member.website_url && (
                  <a href={member.website_url} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    <FaGlobe />
                  </a>
                )}
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

// TeamDetail.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { FaGithub, FaLinkedin, FaInstagram, FaTwitter, FaGlobe } from 'react-icons/fa';

function TeamDetail() {
  const { id } = useParams();
  const [member, setMember] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/team/${id}/`)
      .then(res => res.json())
      .then(data => setMember(data));
  }, [id]);

  if (!member) return <div>Loading...</div>;

  return (
    <div className="team-detail">
      <div className="member-header">
        <img src={member.photo} alt={member.name} className="member-photo-large" />
        <div className="member-info">
          <h1>{member.name}</h1>
          <h2 className="role">{member.role}</h2>
          
          {/* Social Links */}
          <div className="social-links-large">
            {member.github_url && (
              <a href={member.github_url} target="_blank" rel="noopener noreferrer" title="GitHub">
                <FaGithub size={28} />
              </a>
            )}
            {member.linkedin_url && (
              <a href={member.linkedin_url} target="_blank" rel="noopener noreferrer" title="LinkedIn">
                <FaLinkedin size={28} />
              </a>
            )}
            {member.instagram_url && (
              <a href={member.instagram_url} target="_blank" rel="noopener noreferrer" title="Instagram">
                <FaInstagram size={28} />
              </a>
            )}
            {member.twitter_url && (
              <a href={member.twitter_url} target="_blank" rel="noopener noreferrer" title="Twitter">
                <FaTwitter size={28} />
              </a>
            )}
            {member.website_url && (
              <a href={member.website_url} target="_blank" rel="noopener noreferrer" title="Website">
                <FaGlobe size={28} />
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Bio */}
      {member.bio && (
        <div className="member-bio">
          <h3>About</h3>
          <p>{member.bio}</p>
        </div>
      )}

      {/* Skills */}
      {member.skills_list.length > 0 && (
        <div className="member-skills">
          <h3>Skills & Expertise</h3>
          <div className="skills-list">
            {member.skills_list.map((skill, idx) => (
              <span key={idx} className="skill-badge">{skill}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export { TeamList, TeamDetail };
```

---

## 🎨 Sample CSS Styling

```css
/* Blog Cards */
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.blog-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.blog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.blog-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.blog-meta {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.blog-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

/* Team Cards */
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.team-card {
  text-align: center;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: transform 0.2s;
}

.team-card:hover {
  transform: scale(1.05);
}

.team-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1rem;
}

.role {
  color: #666;
  font-style: italic;
}

.skills-preview {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
  margin: 1rem 0;
}

.skill-tag {
  background: #f0f0f0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.social-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.social-links a {
  color: #333;
  transition: color 0.2s;
}

.social-links a:hover {
  color: #1976d2;
}

/* Event Cards */
.event-card {
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin-bottom: 1rem;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.event-date {
  font-weight: bold;
  color: #ff9800;
}

/* Roadmap Cards */
.roadmap-card {
  border: 2px solid #4caf50;
  border-radius: 8px;
  padding: 1.5rem;
}

.roadmap-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 1rem;
}
```

---

## 🔄 Complete Fetch Example (All Endpoints)

```javascript
// api.js - Centralized API functions
const API_BASE = 'http://127.0.0.1:8000/api';

export const api = {
  // Blogs
  getBlogs: () => fetch(`${API_BASE}/blog/`).then(r => r.json()),
  getBlog: (id) => fetch(`${API_BASE}/blog/${id}/`).then(r => r.json()),
  
  // Projects
  getProjects: () => fetch(`${API_BASE}/projects/`).then(r => r.json()),
  getProject: (id) => fetch(`${API_BASE}/projects/${id}/`).then(r => r.json()),
  
  // Roadmaps
  getRoadmaps: () => fetch(`${API_BASE}/roadmaps/`).then(r => r.json()),
  getRoadmap: (id) => fetch(`${API_BASE}/roadmaps/${id}/`).then(r => r.json()),
  
  // Events
  getEvents: () => fetch(`${API_BASE}/events/`).then(r => r.json()),
  getEvent: (id) => fetch(`${API_BASE}/events/${id}/`).then(r => r.json()),
  
  // Team
  getTeam: () => fetch(`${API_BASE}/team/`).then(r => r.json()),
  getTeamMember: (id) => fetch(`${API_BASE}/team/${id}/`).then(r => r.json()),
};

// Usage in components:
// import { api } from './api';
// const blogs = await api.getBlogs();
```

---

## ✅ Summary: What You Get From Each Endpoint

### `/api/blog/` → Blog Posts
- ✅ title, summary, content (HTML)
- ✅ image URL
- ✅ author_name, published_date
- ✅ tags (array)

### `/api/projects/` → Projects
- ✅ title, description, content (HTML)
- ✅ image URL
- ✅ author_name, published_date
- ✅ tags (array)

### `/api/roadmaps/` → Roadmaps
- ✅ icon_name, title, description, content (HTML)
- ✅ author_name, published_date

### `/api/events/` → Events
- ✅ title, summary, content (HTML)
- ✅ image URL
- ✅ author_name, event_date

### `/api/team/` → Team Members
- ✅ name, role, photo URL
- ✅ bio
- ✅ skills (string), skills_list (array)
- ✅ position_rank
- ✅ github_url, linkedin_url, instagram_url, twitter_url, website_url

All data is **automatically sent** in JSON format. No special configuration needed!
