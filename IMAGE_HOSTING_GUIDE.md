# External Image Hosting Guide

## Overview
To minimize server storage costs on free-tier deployments, this backend uses **external image hosting** instead of storing images locally. All image fields have been converted from `ImageField` to `URLField`.

## Supported Image Hosting Services

### Recommended: Imgur
- **Free**: Unlimited uploads
- **No account required**: Upload anonymously
- **Direct links**: Easy to get image URLs
- **CDN**: Fast global delivery

**How to upload to Imgur:**
1. Go to https://imgur.com/upload
2. Upload your image (no account needed)
3. Click the image to open it
4. Right-click → "Copy Image Address"
5. Paste the URL into the Django admin

### Alternative Services
- **Cloudinary**: Free tier with 25GB storage
- **ImageKit**: Free tier with 20GB bandwidth
- **PostImages**: Free anonymous hosting
- **ImgBB**: Free hosting with API

## Using the Admin Panel

### Adding Images to Content

1. **Upload your image** to Imgur or similar service
2. **Copy the direct image URL** (must end in .jpg, .png, .webp, etc.)
3. **Paste the URL** in the appropriate field:
   - Projects: `image_url`
   - Blog Posts: `image_url`
   - Events: `image_url`
   - Team Members: `photo_url`

### Example URLs
```
✅ Valid:
https://i.imgur.com/abc123.jpg
https://res.cloudinary.com/demo/image/upload/sample.jpg

❌ Invalid (page URL, not direct image):
https://imgur.com/abc123
https://imgur.com/gallery/abc123
```

## Benefits

### For Free Tier Deployments
- **Zero storage costs**: No local media files
- **No bandwidth charges**: Images served from CDN
- **Smaller backups**: Database-only backups
- **Faster deployments**: No need to sync media files

### For Performance
- **CDN delivery**: Images served from nearest edge location
- **Automatic optimization**: Many services auto-optimize images
- **Better caching**: External CDNs handle cache management

## Migration Details

The following fields were converted:
- `BlogPost.image` → `BlogPost.image_url`
- `Project.image` → `Project.image_url`
- `Event.image` → `Event.image_url`
- `TeamMember.photo` → `TeamMember.photo_url`

All URL fields accept up to 500 characters and are optional (except `photo_url` for team members).

## For Frontend Developers

### API Response Format
All image fields now return direct URLs:

```json
{
  "id": 1,
  "title": "Sample Project",
  "image_url": "https://i.imgur.com/example.jpg"
}
```

Simply use these URLs directly in `<img>` tags:
```html
<img src={project.image_url} alt={project.title} />
```

### Handling Missing Images
Check if URL is empty before rendering:
```javascript
{blog.image_url && <img src={blog.image_url} alt={blog.title} />}
```

## Troubleshooting

### Image Not Loading?
1. Check if URL is a **direct image link** (ends in .jpg, .png, etc.)
2. Open the URL in a browser - should show ONLY the image
3. Some services block hotlinking - use Imgur to avoid this
4. Ensure the URL uses HTTPS (not HTTP)

### CORS Issues?
Imgur and most CDNs include proper CORS headers. If you encounter CORS issues, the image host may be blocking cross-origin requests. Switch to Imgur.

### Image Too Large?
Most hosting services automatically optimize images. For manual optimization:
- Use https://tinypng.com/ to compress before uploading
- Target < 500KB for good performance
- Use WebP format when possible

## Deployment Notes

### Environment Variables
No special configuration needed! Since images are external, you don't need:
- ❌ `MEDIA_ROOT`
- ❌ `MEDIA_URL`
- ❌ File upload middleware
- ❌ Storage backends

### Server Requirements
- ✅ Minimal storage (database only)
- ✅ No file upload limits to configure
- ✅ No need for persistent storage volumes

## Future Considerations

If you need local uploads in the future, you can:
1. Add Django storage backends (e.g., `django-storages` with S3)
2. Implement image upload API that pushes to Imgur API
3. Use both URL and upload fields for flexibility

For now, manual URL entry keeps the system simple and cost-effective.

