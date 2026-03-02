# Project Metadata Feature Implementation

## Summary
Enhanced the `landing_page` app to support rich project metadata including open-source status, publishers, and detailed contributor information.

## What Was Implemented

### 1. New Project Fields
- `is_open_source` (Boolean) - Whether the project is open or closed source
- `status` (Choice field) - Project status: Idea, In Progress, Completed, Archived
- `repo_url` (URL) - Repository link (e.g., GitHub)
- `demo_url` (URL) - Live demo/deployment link

### 2. New Models

#### ProjectPublisher
Stores project publisher names with automatic alphabetical ordering:
- `name` - Publisher name (e.g., "R. K. Shaw")
- `normalized_name` - Auto-generated lowercase version for sorting
- `slug` - Auto-generated slug
- **Ordering**: Alphabetically by name (enforced on save)

#### ProjectContributor  
Stores detailed information about each team member who contributed:
- `name` - Contributor name
- `role_type` - Free-form text (e.g., "Backend", "Design", "ML")
- `role_title` - Position/title (e.g., "Lead Developer")
- `photo_url` - Profile photo URL
- `github_url` - GitHub profile link
- `linkedin_url` - LinkedIn profile link
- `website_url` - Personal website
- `bio` - Optional biography
- `order` - Manual ordering (lower = higher priority)

### 3. API Changes

#### Project List/Detail Endpoints
Now include nested data:
```json
{
  "id": 1,
  "title": "Project Alpha",
  "description": "Short description",
  "is_open_source": true,
  "status": "in_progress",
  "repo_url": "https://github.com/example/project",
  "demo_url": "https://demo.example.com",
  "publishers": [
    {"id": 1, "name": "R. K. Shaw", "slug": "r-k-shaw"},
    {"id": 2, "name": "S. S. Kashyap", "slug": "s-s-kashyap"}
  ],
  "contributors": [
    {
      "id": 1,
      "name": "Aarav",
      "role_type": "Design",
      "role_title": "Product Designer",
      "photo_url": "https://imgur.com/photo.png",
      "github_url": "",
      "linkedin_url": "",
      "website_url": "",
      "bio": "",
      "order": 1
    },
    {
      "id": 2,
      "name": "Deobrat",
      "role_type": "Backend",
      "role_title": "Lead Dev",
      "photo_url": "https://imgur.com/a.png",
      "github_url": "https://github.com/deobrat",
      "linkedin_url": "https://linkedin.com/in/deobrat",
      "website_url": "https://deobrat.dev",
      "bio": "Builder",
      "order": 2
    }
  ],
  "tags": [...],
  "author_name": "Alex Doe",
  "published_date": "2026-03-02T10:00:00Z"
}
```

#### Creating/Updating Projects
Publishers and contributors can be nested in POST/PUT requests:
```json
{
  "title": "New Project",
  "description": "Description",
  "is_open_source": true,
  "status": "in_progress",
  "repo_url": "https://github.com/user/repo",
  "publishers": [
    {"name": "John Doe"},
    {"name": "Jane Smith"}
  ],
  "contributors": [
    {
      "name": "Alice",
      "role_type": "Frontend",
      "role_title": "UI Engineer",
      "order": 1
    }
  ]
}
```

### 4. Admin Panel Updates
- Project admin now has inline forms for adding publishers and contributors
- New fields visible in project list: `status`, `is_open_source`
- Organized fieldsets: Basic Info, Meta, Links & Status
- Search includes publisher and contributor names

### 5. Database Migration
- Migration `0018_project_demo_url_project_is_open_source_and_more.py` created
- Successfully applied to local SQLite database
- Production Supabase DB untouched (as requested)

### 6. Tests
All tests passing (6/6):
- ✅ Project creation with nested publishers/contributors
- ✅ Alphabetical ordering of publishers enforced
- ✅ Contributor ordering by `order` field
- ✅ API detail endpoint returns nested data
- ✅ List/detail serializers work correctly
- ✅ Anonymous users blocked from creating projects

## Key Features

### Automatic Publisher Alphabetization
Publishers are automatically sorted alphabetically by name when saved:
- "Zara" and "Aaron" → stored/returned as ["Aaron", "Zara"]
- Uses `normalized_name` field for case-insensitive sorting

### Flexible Contributor Ordering
Contributors can be manually ordered using the `order` field:
- Lower order = appears first
- Default order = 100
- Allows full control over team member display sequence

### Free-Form Role Types
Role types are free-form text fields allowing any designation:
- "Backend", "Frontend", "Design", "ML", "DevOps", etc.
- No predefined choices - maximum flexibility

## Files Modified
1. `landing_page/models.py` - Added new models and fields
2. `landing_page/serializers.py` - Nested serializers with create/update logic
3. `landing_page/admin.py` - Inline admins and fieldsets
4. `landing_page/views.py` - Prefetch related data for performance
5. `landing_page/tests.py` - Comprehensive test coverage

## Migration Status
- ✅ Local SQLite: Migrated successfully
- ⏸️ Production Supabase: Not touched (as requested)

## Next Steps (When Ready for Production)
1. Backup production database
2. Apply migration to Supabase: `python manage.py migrate landing_page`
3. Test on staging environment
4. Update frontend to consume new API fields
5. Add publisher/contributor data to existing projects via admin panel

## Feature Complete ✅
All requested functionality has been implemented and tested successfully.

