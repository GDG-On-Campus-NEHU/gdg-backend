# Local Testing Guide - Project Metadata Features

## Server Status
✅ Django development server should now be running on: **http://127.0.0.1:8000**

## Quick Start Testing

### 1. Access Admin Panel
```
URL: http://127.0.0.1:8000/admin/
```

Log in with your superuser credentials. If you don't have one:
```bash
python manage.py createsuperuser
```

### 2. Test via Admin Panel

#### Create a Project with Publishers & Contributors:
1. Go to: http://127.0.0.1:8000/admin/landing_page/project/
2. Click "Add Project"
3. Fill in basic info:
   - Title: "AI Chatbot"
   - Description: "Smart conversational AI"
   - Status: "In Progress"
   - ✅ Check "Is open source"
   - Repo URL: "https://github.com/yourorg/chatbot"
   - Demo URL: "https://chatbot.demo.com"

4. **Add Publishers** (scroll down to "Publishers" section):
   - Row 1: "R. K. Shaw"
   - Row 2: "S. S. Kashyap"
   - Row 3: "D. Patar"
   - They will automatically sort alphabetically!

5. **Add Contributors** (scroll to "Contributors" section):
   - Contributor 1:
     - Name: "Alice Johnson"
     - Role type: "Backend"
     - Role title: "Lead Developer"
     - Order: 1
     - Photo URL: "https://i.imgur.com/example1.jpg"
     - GitHub: "https://github.com/alice"
     - LinkedIn: "https://linkedin.com/in/alice"
     - Website: "https://alice.dev"
     - Bio: "Full-stack engineer specializing in Django and React"
   
   - Contributor 2:
     - Name: "Bob Smith"
     - Role type: "Design"
     - Role title: "UI/UX Designer"
     - Order: 2
     - Photo URL: "https://i.imgur.com/example2.jpg"
     - LinkedIn: "https://linkedin.com/in/bob"

6. Click "Save"

### 3. Test via API

#### View All Projects (List):
```bash
curl http://127.0.0.1:8000/api/projects/
```

#### View Project Detail:
```bash
curl http://127.0.0.1:8000/api/projects/<project-slug>/
```

Example response:
```json
{
  "id": 1,
  "slug": "ai-chatbot",
  "title": "AI Chatbot",
  "description": "Smart conversational AI",
  "image_url": "",
  "is_open_source": true,
  "status": "in_progress",
  "repo_url": "https://github.com/yourorg/chatbot",
  "demo_url": "https://chatbot.demo.com",
  "tags": [],
  "tag_ids": [],
  "author_name": "",
  "published_date": "2026-03-02T14:00:00Z",
  "content": "",
  "publishers": [
    {"id": 3, "name": "D. Patar", "slug": "d-patar"},
    {"id": 1, "name": "R. K. Shaw", "slug": "r-k-shaw"},
    {"id": 2, "name": "S. S. Kashyap", "slug": "s-s-kashyap"}
  ],
  "contributors": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "role_type": "Backend",
      "role_title": "Lead Developer",
      "photo_url": "https://i.imgur.com/example1.jpg",
      "github_url": "https://github.com/alice",
      "linkedin_url": "https://linkedin.com/in/alice",
      "website_url": "https://alice.dev",
      "bio": "Full-stack engineer specializing in Django and React",
      "order": 1
    },
    {
      "id": 2,
      "name": "Bob Smith",
      "role_type": "Design",
      "role_title": "UI/UX Designer",
      "photo_url": "https://i.imgur.com/example2.jpg",
      "github_url": "",
      "linkedin_url": "https://linkedin.com/in/bob",
      "website_url": "",
      "bio": "",
      "order": 2
    }
  ]
}
```

#### Create Project via API (requires authentication):
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "title": "Machine Learning Pipeline",
    "description": "Automated ML workflow",
    "is_open_source": true,
    "status": "completed",
    "repo_url": "https://github.com/org/ml-pipeline",
    "demo_url": "https://ml-demo.com",
    "publishers": [
      {"name": "John Doe"},
      {"name": "Jane Smith"}
    ],
    "contributors": [
      {
        "name": "Charlie",
        "role_type": "ML Engineer",
        "role_title": "Senior ML Engineer",
        "photo_url": "https://i.imgur.com/charlie.jpg",
        "github_url": "https://github.com/charlie",
        "order": 1
      }
    ]
  }'
```

### 4. Key Things to Verify

✅ **Publishers Alphabetization**:
- Add publishers in random order (e.g., Zara, Aaron, Mike)
- After saving, they should display alphabetically: Aaron, Mike, Zara

✅ **Contributor Ordering**:
- Set different `order` values (e.g., 3, 1, 2)
- Contributors should display by order: 1, 2, 3

✅ **Free-Form Role Types**:
- Try various role types: "Backend", "Frontend", "ML", "DevOps", "QA", "Design"
- All should save successfully

✅ **Optional Fields**:
- Leave some contributor fields blank (bio, website, GitHub)
- Should work fine with partial data

✅ **Open Source Toggle**:
- Toggle `is_open_source` checkbox
- Should reflect in API response

✅ **Status Field**:
- Try all status options: Idea → In Progress → Completed → Archived
- Should update in both admin and API

### 5. Testing Endpoints

Base URL: `http://127.0.0.1:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects/` | GET | List all projects (includes publishers/contributors in detail view) |
| `/api/projects/<slug>/` | GET | Get project detail with full nested data |
| `/api/projects/` | POST | Create new project (auth required) |
| `/api/projects/<slug>/` | PUT/PATCH | Update project (auth required) |
| `/api/projects/<slug>/` | DELETE | Delete project (auth required) |
| `/admin/landing_page/project/` | - | Admin interface |

### 6. Sample Test Data

Quick copy-paste for testing:

**Publishers:**
- R. K. Shaw
- S. S. Kashyap
- D. Patar

**Contributor 1:**
- Name: Deobrat Patar
- Role Type: Full-Stack
- Role Title: Backend Lead
- Order: 1
- Photo: https://i.imgur.com/deobrat.jpg
- GitHub: https://github.com/deobrat
- LinkedIn: https://linkedin.com/in/deobrat
- Website: https://deobrat.dev
- Bio: Passionate about building scalable systems

**Contributor 2:**
- Name: Rohit Shaw
- Role Type: DevOps
- Role Title: Infrastructure Engineer
- Order: 2
- Photo: https://i.imgur.com/rohit.jpg
- GitHub: https://github.com/rohitshaw
- LinkedIn: https://linkedin.com/in/rohitshaw

### 7. Troubleshooting

**Server not starting?**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python manage.py runserver 8080
```

**Can't log in to admin?**
```bash
# Create superuser
python manage.py createsuperuser
```

**Database issues?**
```bash
# Verify migrations
python manage.py showmigrations landing_page

# If needed, remigrate
python manage.py migrate landing_page
```

**API returns empty publishers/contributors?**
- Make sure you saved the project with inlines in admin
- Check the API detail endpoint (not list endpoint)
- List endpoint may not include nested data by default

## Browser Testing

1. **Admin Panel**: http://127.0.0.1:8000/admin/landing_page/project/
2. **API Browser**: http://127.0.0.1:8000/api/projects/
3. **DRF Browsable API**: Click on any project to see detail view with nested data

## What to Look For

✅ Publishers appear in alphabetical order  
✅ Contributors appear in order specified by `order` field  
✅ All links (GitHub, LinkedIn, Website) are saved correctly  
✅ Open source flag works  
✅ Status dropdown has all 4 options  
✅ API returns nested JSON with all fields  
✅ Admin inlines allow easy editing  

## Ready for Production?

Once you've verified everything works locally:
1. Test creating/editing multiple projects
2. Verify alphabetical ordering works correctly
3. Test all CRUD operations via API
4. Check admin panel usability

Then you can proceed with deploying to Supabase! 🚀

