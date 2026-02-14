"""
Quick test script to demonstrate image upload to blog API.
Run this script directly after starting the Django server.
"""

import io
import json



def main() -> None:
    import requests
    from PIL import Image
    # Create a test image in memory (100x100 red pixel PNG)
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Prepare the multipart form data
    files = {
        'image': ('test_image.png', img_bytes, 'image/png')
    }

    data = {
        'title': 'Blog Post with Image',
        'summary': 'This post includes an uploaded image',
        'content': '<p>Check out the image below!</p>',
        'author_name': 'Test Author',
    }

    # Send POST request
    print('Sending POST request to create blog with image...')
    response = requests.post(
        'http://127.0.0.1:8000/api/blog/',
        files=files,
        data=data,
        timeout=10,
    )

    print(f'\nStatus Code: {response.status_code}')

    if response.status_code == 201:
        result = response.json()
        print('\n✅ Blog post created successfully!')
        print(f"\nID: {result.get('id')}")
        print(f"Title: {result.get('title')}")
        print(f"Author: {result.get('author_name')}")
        print(f"Published: {result.get('published_date')}")

        image_value = result.get('image_url') or result.get('image')
        print(f'Image URL: {image_value}')

        print('\nFull response:')
        print(json.dumps(result, indent=2))
    else:
        print(f'\n❌ Error: {response.text}')


if __name__ == '__main__':
    main()
