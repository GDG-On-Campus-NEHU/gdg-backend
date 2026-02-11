# Global Search API Documentation

## 🔍 Search Endpoint

### URL
```
GET /api/search/?q=search_term
```

### Query Parameters
| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `q` | Yes | string | Search query (minimum 2 characters) |

---

## Response Schema

```json
{
  "query": "search term",
  "blogs": [...],
  "projects": [...],
  "team": [...],
  "events": [...],
  "roadmaps": [...],
  "tags": [...]
}
```

---

## Example Request & Response

### Request
```bash
curl "http://localhost:8000/api/search/?q=python"
```

### Response
```json
{
  "query": "python",
  "blogs": [
    {
      "id": 1,
      "title": "Getting Started with Python",
      "summary": "Learn Python basics",
      "content": "<p>Python is a great language...</p>",
      "image_url": "https://i.imgur.com/example.jpg",
      "tags": [{"name": "Python"}],
      "author_name": "John Doe",
      "published_date": "2024-02-11T10:30:00Z"
    }
  ],
  "projects": [
    {
      "id": 1,
      "title": "Python AI Project",
      "description": "An AI project built with Python",
      "content": "<p>Project details...</p>",
      "image_url": "https://i.imgur.com/project.jpg",
      "tags": [{"name": "AI/ML"}, {"name": "Python"}],
      "author_name": "Jane Smith",
      "published_date": "2024-02-10T14:00:00Z"
    }
  ],
  "team": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "role": "Python Developer",
      "photo_url": "https://i.imgur.com/alice.jpg",
      "bio": "Expert in Python and AI",
      "skills": "Python, Machine Learning, Django",
      "skills_list": ["Python", "Machine Learning", "Django"],
      "position_rank": 1,
      "github_url": "https://github.com/alice",
      "linkedin_url": "https://linkedin.com/in/alice",
      "instagram_url": "",
      "twitter_url": "",
      "website_url": ""
    }
  ],
  "events": [
    {
      "id": 1,
      "title": "Python Workshop",
      "summary": "Learn Python in this intensive workshop",
      "content": "<h2>Workshop Details</h2><p>Join us...</p>",
      "image_url": "https://i.imgur.com/event.jpg",
      "author_name": "Bob Lee",
      "event_date": "2024-03-15T14:00:00Z"
    }
  ],
  "roadmaps": [
    {
      "id": 1,
      "icon_name": "🐍",
      "title": "Python Learning Roadmap",
      "description": "Complete guide to learning Python",
      "content": "<h2>Beginner Phase</h2><ul><li>Python basics</li>...</ul>",
      "author_name": "Jane Smith",
      "published_date": "2024-02-01T09:00:00Z"
    }
  ],
  "tags": [
    {"name": "Python"},
    {"name": "Programming"}
  ]
}
```

---

## Searchable Fields

### Blog Posts
- `title` - Post title
- `summary` - Short summary
- `content` - Full HTML content
- `author_name` - Author name

### Projects
- `title` - Project title
- `description` - Project description
- `content` - Full HTML content
- `author_name` - Author name

### Team Members
- `name` - Member name
- `role` - Job role/title
- `bio` - Biography
- `skills` - Skills (comma-separated)

### Events
- `title` - Event title
- `summary` - Event summary
- `content` - Full HTML content
- `author_name` - Organizer name

### Roadmaps
- `title` - Roadmap title
- `description` - Short description
- `content` - Full HTML content

### Tags
- `name` - Tag name

---

## Search Behavior

### Case-Insensitive
Search is **case-insensitive**:
```
/api/search/?q=python     # matches "Python", "PYTHON", etc.
```

### Partial Matching
Searches match **any part** of the text:
```
/api/search/?q=app        # matches "App", "Application", "Apple", etc.
```

### Results Limit
Each category returns **up to 10 results**:
- Max 10 blogs
- Max 10 projects
- Max 10 team members
- Max 10 events
- Max 10 roadmaps
- Max 10 tags

### Minimum Query Length
Query must be **at least 2 characters**:
```bash
# ❌ Error - too short
curl "http://localhost:8000/api/search/?q=a"

# ✅ OK
curl "http://localhost:8000/api/search/?q=ai"
```

### Response on Invalid Query
```json
{
  "query": "a",
  "error": "Search query must be at least 2 characters",
  "blogs": [],
  "projects": [],
  "team": [],
  "events": [],
  "roadmaps": [],
  "tags": []
}
```

---

## Frontend Implementation Examples

### React Hook
```typescript
import { useState } from 'react';

interface SearchResults {
  query: string;
  blogs: any[];
  projects: any[];
  team: any[];
  events: any[];
  roadmaps: any[];
  tags: any[];
}

function useGlobalSearch() {
  const [results, setResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);

  const search = async (query: string) => {
    if (query.length < 2) {
      setResults(null);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/search/?q=${encodeURIComponent(query)}`
      );
      const data = await response.json();
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  return { results, loading, search };
}
```

### Search Component
```tsx
import { useState } from 'react';
import { useGlobalSearch } from './useGlobalSearch';

export function GlobalSearch() {
  const [query, setQuery] = useState('');
  const { results, loading, search } = useGlobalSearch();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    search(value);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="Search blogs, projects, team, events..."
        value={query}
        onChange={handleChange}
        className="search-input"
      />

      {loading && <div>Loading...</div>}

      {results && query.length >= 2 && (
        <div className="search-results">
          {/* Blog Results */}
          {results.blogs.length > 0 && (
            <section>
              <h3>📝 Blogs ({results.blogs.length})</h3>
              {results.blogs.map(blog => (
                <div key={blog.id} className="result-item">
                  <h4>{blog.title}</h4>
                  <p>{blog.summary}</p>
                </div>
              ))}
            </section>
          )}

          {/* Project Results */}
          {results.projects.length > 0 && (
            <section>
              <h3>🚀 Projects ({results.projects.length})</h3>
              {results.projects.map(project => (
                <div key={project.id} className="result-item">
                  <h4>{project.title}</h4>
                  <p>{project.description}</p>
                </div>
              ))}
            </section>
          )}

          {/* Team Results */}
          {results.team.length > 0 && (
            <section>
              <h3>👥 Team ({results.team.length})</h3>
              {results.team.map(member => (
                <div key={member.id} className="result-item">
                  <h4>{member.name}</h4>
                  <p>{member.role} - {member.skills}</p>
                </div>
              ))}
            </section>
          )}

          {/* Event Results */}
          {results.events.length > 0 && (
            <section>
              <h3>📅 Events ({results.events.length})</h3>
              {results.events.map(event => (
                <div key={event.id} className="result-item">
                  <h4>{event.title}</h4>
                  <p>{event.summary}</p>
                </div>
              ))}
            </section>
          )}

          {/* Roadmap Results */}
          {results.roadmaps.length > 0 && (
            <section>
              <h3>🗺️ Roadmaps ({results.roadmaps.length})</h3>
              {results.roadmaps.map(roadmap => (
                <div key={roadmap.id} className="result-item">
                  <h4>{roadmap.icon_name} {roadmap.title}</h4>
                  <p>{roadmap.description}</p>
                </div>
              ))}
            </section>
          )}

          {/* Tag Results */}
          {results.tags.length > 0 && (
            <section>
              <h3>🏷️ Tags ({results.tags.length})</h3>
              <div className="tags">
                {results.tags.map(tag => (
                  <span key={tag.name} className="tag">
                    {tag.name}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* No Results */}
          {Object.values(results).every(arr => !Array.isArray(arr) || arr.length === 0) && (
            <p>No results found for "{query}"</p>
          )}
        </div>
      )}
    </div>
  );
}
```

### Vue.js Example
```vue
<template>
  <div class="search-container">
    <input
      v-model="query"
      @input="handleSearch"
      placeholder="Search blogs, projects, team, events..."
      class="search-input"
    />

    <div v-if="loading">Loading...</div>

    <div v-if="results && query.length >= 2" class="search-results">
      <!-- Blog Results -->
      <section v-if="results.blogs.length > 0">
        <h3>📝 Blogs ({{ results.blogs.length }})</h3>
        <div v-for="blog in results.blogs" :key="blog.id" class="result-item">
          <h4>{{ blog.title }}</h4>
          <p>{{ blog.summary }}</p>
        </div>
      </section>

      <!-- Similar sections for projects, team, events, roadmaps, tags -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const results = ref(null);
const loading = ref(false);

const handleSearch = async () => {
  if (query.value.length < 2) {
    results.value = null;
    return;
  }

  loading.value = true;
  try {
    const response = await fetch(
      `http://localhost:8000/api/search/?q=${encodeURIComponent(query.value)}`
    );
    results.value = await response.json();
  } finally {
    loading.value = false;
  }
};
</script>
```

---

## Database Tables (For Reference)

| Table | Searches |
|-------|----------|
| `landing_page_blogpost` | title, summary, content, author_name |
| `landing_page_project` | title, description, content, author_name |
| `landing_page_teamember` | name, role, bio, skills |
| `landing_page_event` | title, summary, content, author_name |
| `landing_page_roadmap` | title, description, content |
| `landing_page_tag` | name |

---

## API Status

✅ **Endpoint:** `/api/search/`  
✅ **Method:** GET  
✅ **Authentication:** None required  
✅ **Rate Limit:** None  
✅ **CORS:** Enabled  

---

## Testing

### Test with curl
```bash
# Search for "Python"
curl "http://localhost:8000/api/search/?q=python"

# Search for "workshop"
curl "http://localhost:8000/api/search/?q=workshop"

# Search for "AI"
curl "http://localhost:8000/api/search/?q=AI"
```

### Test in browser
```
http://localhost:8000/api/search/?q=python
http://localhost:8000/api/search/?q=workshop
http://localhost:8000/api/search/?q=team
```

---

## Performance Tips

1. **Debounce search input** - Don't search on every keystroke
2. **Limit request frequency** - Wait 300-500ms after user stops typing
3. **Cache results** - Store recent search results to reduce API calls
4. **Show results incrementally** - Display results as they load
5. **Limit display** - Show only top 3-5 results per category initially

### Debounced Search Example (React)
```typescript
function useGlobalSearchDebounced(delay = 300) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const timeoutRef = useRef(null);

  const search = async (q: string) => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    if (q.length < 2) {
      setResults(null);
      return;
    }

    timeoutRef.current = setTimeout(async () => {
      const response = await fetch(
        `http://localhost:8000/api/search/?q=${encodeURIComponent(q)}`
      );
      setResults(await response.json());
    }, delay);
  };

  return { query, setQuery, results, search };
}
```

---

**API Version:** 1.0  
**Last Updated:** February 11, 2026  
**Status:** ✅ Live and tested

