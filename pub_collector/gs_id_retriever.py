import requests

def get_fabric_users(url, offset=0, limit=50):
    """
    Retrieve Fabric users from the database.
    """
    params = {
        'exact_match': 'false',
        'offset': offset,
        'limit': limit
    }
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_author_details(people_data):
    headers = {
        'accept': 'application/json'
    }
    base_url = 'https://uis.fabric-testbed.net/people'
    
    author_details = {}
    
    for person in people_data.get('results', []):
        uuid = person.get('uuid')
        name = person.get('name')

        if not uuid or not name:
            continue  # skip bad entries

        detail_url = f"{base_url}/{uuid}"
        params = {'as_self': 'false'}
        
        response = requests.get(detail_url, headers=headers, params=params)
        response.raise_for_status()
        detail_data = response.json()
        
        affiliation = None
        if detail_data.get('results'):
            affiliation = detail_data['results'][0].get('affiliation')

        author_details[uuid] = {
            'name': name,
            'affiliation': affiliation
        }
    
    return author_details