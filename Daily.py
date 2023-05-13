import requests
from datetime import datetime, timezone
import json

headers = {
    "Authorization": f'Bearer {NOTION_TOKEN}',
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Create a page
def create_page(data: dict):
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
    else:
        print("Failed to create the page. Error: ", res.status_code)

    return res

if (__name__ == "__main__"):
    # Format date elements for today's page
    published_date = datetime.now().astimezone(timezone.utc).isoformat()[0:10]
    
    date = datetime.now().strftime('%B %d, %Y')
    if(date[date.index('0') + 1].isdigit() and date[date.index('0') - 1] != '2'):
        date = date.replace('0', '', 1)

    # Data - dictionary of default attributes for a page
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
        }
    }

    create_page(data)
