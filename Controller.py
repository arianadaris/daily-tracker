import requests
from datetime import datetime, timezone
import json
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables
load_dotenv(find_dotenv())
NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('DATABASE_ID')

# Format request headers
headers = {
    "Authorization": f'Bearer {NOTION_TOKEN}',
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Required attributes in order
ordered_attrs = [
    'To Sleep Hr. (1am = 13, 2am = 14)',
    'To Sleep Minute',
    'Awake Hour',
    'Awake Minute',
    'Mood',
    'Work out',
    'Gym Day'
]

"""
create_page(datetime_obj)
"""
def create_page(datetime_obj):
    # Format the datetime object
    published_date = datetime_obj.astimezone(timezone.utc).isoformat()[0:10]
    date = datetime_obj.strftime('%B %d, %Y')
    if date[date.index('0') + 1].isdigit() and date[date.index('0') - 1] != '2':
        date = date.replace('0', '', 1)

    # Format data dictionary
    data = {
        'Date': {
            'date': {
                'start': published_date,
                'end': None
            }
        },
        'Open': {
            'title': [{
                'text': {
                    'content': date
                },
                'plain_text': date
            }]
        },
        "To Sleep Hr. (1am = 13, 2am = 14)": { "number": 12 },
        "To Sleep Minute": { "number": 40 },
        "Awake Hour": { "number": 7 },
        "Awake Minute": { "number": 45 },
        "Mood": { "select": { "name": "Excited" } },
        "Work out": { "checkbox": False },
        "Intermittent fasting": { "checkbox": True },
        "Eat 100g of Protein": { "checkbox": False },
        "Drink water": { "checkbox": False },
        "Track Meals": { "checkbox": False },
        "Skincare": { "checkbox": True },
        "Improvements": { "rich_text": [{ "text": { "content": "blue!" } }] }
    }

    # Format POST request
    create_url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {
            "database_id": DATABASE_ID,
        },
        "properties": data
    }

    res = requests.post(create_url, headers=headers, json=payload)

    if res.status_code == 200:
        print("Page created successfully.")
        return res.json()['id']
    else:
        print("Failed to create the page. Error: ", res.status_code)
        return 0

"""
check_page_exists(datetime_obj)
Check if a page already exists for that date
"""
def check_page_exists(datetime_obj):
    # Format datetime object
    date = datetime_obj.isoformat()[0:10]

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    res = requests.post(url, headers=headers)

    if res.status_code == 200:
        pages = res.json().get('results', [])

        # Search for a page with the specified creation date
        for page in pages:
            page_title = page.get('properties', {}).get('Date', {}).get('date', {}).get('start', '')
            if page_title == date:
                print('Page exists')
                return True
            
        print('Page does not exist')
        return False
    else:
        print(f'Error: {res.status_code} - {res.text}')
        return False

"""
get_page_id(date)
"""
def get_page_id(datetime_obj):
    # Format datetime object
    date = datetime_obj.isoformat()[0:10]

    url = 'https://api.notion.com/v1/search'
    res = requests.post(url, headers=headers, json={'query': date})

    if res.status_code == 200:
        data = res.json()
        pages = data.get('results', [])

        # Find first page with specified title
        for page in pages:
            if page.get('object') == 'page':
                page_title = page.get('properties', {}).get('Date', {}).get('date', {}).get('start', '')
                if page_title == date:
                    page_id = page.get('id')
                    print(f'Page ID: {page_id}')
                    return page_id
                
        print("Page not found with specified title")
        return None

"""
update_page(data)
"""
def update_page(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": {}}

    for d in data:
        for key, value in d.items():
            payload["properties"][key] = value

    with open('output.json', 'w') as f:
        json.dump(payload, f)

    # print(payload)

    res = requests.patch(url, headers=headers, data=json.dumps(payload))

    if res.status_code == 200:
        print("Page updated successfully.")
    else:
        print("Failed to update the page. Error: ", res.text)

    return res

"""
get_db()
"""
def get_db():
    res = requests.get(f'https://api.notion.com/v1/databases/{DATABASE_ID}', headers=headers)
    return res.json()

"""
get_attrs()
"""
def get_attrs():
    data = get_db()
    attrs = []

    # Get attributes names (Sleep Hour, Sleep Min, etc.)
    attr_names = data["properties"].keys()

    # For each attr name, get input type and select options if applicable
    for name in attr_names:
        attr_type = data['properties'][name]['type']
        if attr_type != "formula" and attr_type != "date" and attr_type != "title":
            attr = {
                "name": name,
                "type": attr_type
            }

            # Check for select options
            if 'select' in data['properties'][name]:
                options = []
                for option in data['properties'][name]['select']['options']:
                    options.append(option["name"])
                
                attr["select"] = options

            attrs.append(attr)

    count = 0
    attr_names = [attr['name'] for attr in attrs]
    for attr in ordered_attrs:
        index = attr_names.index(attr)
        attrs[count], attrs[index] = attrs[index], attrs[count]
        count += 1

    return attrs

