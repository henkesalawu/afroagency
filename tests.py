import requests

# Base URL for your Flask application
BASE_URL = 'http://localhost:8080'

# Replace 'your_jwt_token' with an actual JWT token if needed
JWT_TOKEN = 'your_jwt_token'

# Headers for authenticated requests
headers = {
    'Authorization': f'Bearer {JWT_TOKEN}',
    'Content-Type': 'application/json'
}

def get_dancers():
    response = requests.get(f'{BASE_URL}/dancers')
    print('GET /dancers:', response.json())

def get_events():
    response = requests.get(f'{BASE_URL}/events')
    print('GET /events:', response.json())

def get_dancer_details(dancer_id):
    response = requests.get(f'{BASE_URL}/dancers/{dancer_id}', headers=headers)
    print(f'GET /dancers/{dancer_id}:', response.json())

def get_event_details(event_id):
    response = requests.get(f'{BASE_URL}/events/{event_id}', headers=headers)
    print(f'GET /events/{event_id}:', response.json())

def add_dancer(name, age, gender, phone=None, website=None):
    data = {
        'name': name,
        'age': age,
        'gender': gender,
        'phone': phone,
        'website': website
    }
    response = requests.post(f'{BASE_URL}/dancers', json=data, headers=headers)
    print('POST /dancers:', response.json())

def add_event(name, address, date):
    data = {
        'name': name,
        'address': address,
        'date': date
    }
    response = requests.post(f'{BASE_URL}/events', json=data, headers=headers)
    print('POST /events:', response.json())

def update_dancer(dancer_id, name=None, age=None, gender=None, phone=None, website=None):
    data = {
        'name': name,
        'age': age,
        'gender': gender,
        'phone': phone,
        'website': website
    }
    response = requests.patch(f'{BASE_URL}/dancers/{dancer_id}', json=data, headers=headers)
    print(f'PATCH /dancers/{dancer_id}:', response.json())

def update_event(event_id, name=None, address=None, date=None):
    data = {
        'name': name,
        'address': address,
        'date': date
    }
    response = requests.patch(f'{BASE_URL}/events/{event_id}', json=data, headers=headers)
    print(f'PATCH /events/{event_id}:', response.json())

def delete_dancer(dancer_id):
    response = requests.delete(f'{BASE_URL}/dancers/{dancer_id}', headers=headers)
    print(f'DELETE /dancers/{dancer_id}:', response.json())

def delete_event(event_id):
    response = requests.delete(f'{BASE_URL}/events/{event_id}', headers=headers)
    print(f'DELETE /events/{event_id}:', response.json())

# Example usage
if __name__ == '__main__':
    # Test public routes
    get_dancers()
    get_events()

    # Test authenticated routes (use valid IDs and token)
    get_dancer_details(1)
    get_event_details(1)
    add_dancer('John Doe', 30, 'Male')
    add_event('Dance Show', '123 Main St', '2024-09-20')
    update_dancer(1, name='Jane Doe')
    update_event(1, address='456 Elm St')
    delete_dancer(1)
    delete_event(1)
