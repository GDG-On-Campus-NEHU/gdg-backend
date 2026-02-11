"""
Quick API Test Script
Run this to verify all endpoints are working
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_endpoint(endpoint, name):
    """Test a single API endpoint"""
    try:
        response = requests.get(f'{BASE_URL}{endpoint}', timeout=5)
        if response.status_code == 200:
            print(f'✅ {name:25s} - Status: 200 OK')
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                # Show first item's keys
                print(f'   Fields: {list(data[0].keys())}')
            return True
        else:
            print(f'❌ {name:25s} - Status: {response.status_code}')
            return False
    except requests.exceptions.ConnectionError:
        print(f'⚠️  {name:25s} - Server not responding')
        return False
    except Exception as e:
        print(f'❌ {name:25s} - Error: {str(e)[:50]}')
        return False

if __name__ == '__main__':
    print('=' * 70)
    print('API ENDPOINT TEST')
    print('=' * 70)
    print()

    endpoints = [
        ('/blog/', 'Blog Posts'),
        ('/projects/', 'Projects'),
        ('/team/', 'Team Members'),
        ('/events/', 'Events'),
        ('/roadmaps/', 'Roadmaps'),
        ('/tags/', 'Tags'),
    ]

    results = []
    for endpoint, name in endpoints:
        results.append(test_endpoint(endpoint, name))

    print()
    print('=' * 70)
    if all(results):
        print('✅ ALL ENDPOINTS WORKING!')
    else:
        print(f'⚠️  {sum(results)}/{len(results)} endpoints working')
    print('=' * 70)

