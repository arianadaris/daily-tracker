import requests
from datetime import datetime, timezone
import json

NOTION_TOKEN = "secret_ezOH8uZ6BdKKyBcCNI8HFGXAvy2VWiZA0GEtOJQo7TZ"
DATABASE_ID = "dbcc15e7590b46999c34b24d1921e98f"

headers = {
    "Authorization": f'Bearer {NOTION_TOKEN}',
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Get a page
def get_page_id(num_pages=None):
    # If num_pages None, get all pages
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

    get_all = num_pages is None
    page_size = 1 if get_all else num_pages

    payload = {
        "page_size": page_size
    }
    res = requests.post(url, headers=headers, json=payload)
    data = res.json()

    results = data["results"][0]
    # while data["has_more"] and get_all:
    #     payload = {
    #         "page_size": page_size,
    #         "start_cursor": data["next-cursor"]
    #     }

    #     url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    #     res = requests.post(url, headers=headers, json=payload)
    #     data = res.json()
    #     results.extend(data['results'])

    return results['id']

# Update a page
def update_page(data):
    page_id = get_page_id();
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": {}}

    for d in data:
        for key, value in d.items():
            payload["properties"][key] = value

    res = requests.patch(url, headers=headers, data=json.dumps(payload))

    if res.status_code == 200:
        print("Page updated successfully.")
    else:
        print("Failed to update the page. Error: ", res.status_code)

    return res

# Get database
def get_db():
    res = requests.get(f'https://api.notion.com/v1/databases/{DATABASE_ID}', headers=headers)
    return res.json()

# Get DB attributes
def get_attrs():
    data = get_db()
    attrs = []

    # Get attributes names (Sleep Hour, Sleep Min, etc.)
    attr_names = data["properties"].keys()

    # For each attr name, get input type and select options if applicable
    for name in attr_names:
        attr_type = data['properties'][name]['type']
        if attr_type != "formula" and attr_type != "date" and attr_type != "title" and attr_type != "rich_text":
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

    ordered_attrs = [
        'To Sleep Hr. (1am = 13, 2am = 14)',
        'To Sleep Minute',
        'Awake Hour',
        'Awake Minute',
        'Mood',
        'Work out',
        'Gym Day'
    ]

    count = 0
    attr_names = [attr['name'] for attr in attrs]
    for attr in ordered_attrs:
        index = attr_names.index(attr)
        attrs[count], attrs[index] = attrs[index], attrs[count]
        count += 1

    return attrs

# Input user data
def get_input(date, attributes):
    date = data['Open']['title'][0]['plain_text']
    divider = '----------------------------'
    print(f'Daily Tracker - {date}\n{divider}')
    inputs = []

    for attr in attributes:
        input_dict = {}
        if attr["type"] == "checkbox":
            val = input(f'{attr["name"]} (True/False): ')
            if val != 'True': val = False
            else: val = True

            input_dict = {
                attr["name"]: {
                    attr["type"]: val
                }
            }
        elif attr["type"] == "number":
            val = input(f'{attr["name"]}: ')

            input_dict = {
                attr["name"]: {
                    attr["type"]: int(val)
                }
            }
        elif attr["type"] == "select":
            options = ', '.join(attr["select"])
            val = input(f'{attr["name"]} ({options}): ')
            if val == '': pass
            else:
                input_dict = {
                    attr["name"]: {
                        "select": {
                            "name": val
                        }
                    }
                }
        elif attr["type"] == "rich_text":
            val = input(f'{attr["name"]}: ')

            input_dict = {
                attr["name"]: {
                    attr["type"]: [val]
                }
            }
            
        else:
            val = input(f'{attr["name"]}: ')

            input_dict = {
                attr["name"]: {
                    attr["type"]: val
                }
            }
        
        inputs.append(input_dict)

    return inputs

if(__name__ == "__main__"):
    # Format date string
    date = datetime.now().strftime('%B %d, %Y')
    if(date[date.index('0') + 1].isdigit() and date[date.index('0') - 1] != '2'):
        date = date.replace('0', '', 1)

    # Data - dictionary of default attributes for a page
    data = {
        'Open': {
            'title': [{
                'plain_text': date
            }]
        }
    }

    # Get user input
    # page_data = get_input(data['Open']['title'][0]['plain_text'], get_attrs())

    # Get today's page ID
    # page_id = get_page_id()

    # # Update today's page
    # update_page(page_id, page_data)