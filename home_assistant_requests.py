import requests
import threading
import matplotlib.colors as mcolors
import time

# Replace the following with your own values
base_url = '<home-assistant-url>'
headers = {'Authorization': 'Bearer <home-assistant-token>',
           'Content-Type': 'application/json'}
entities_list = ['<entity-name-1>','<entity-name-2>', '<entity-name-3>', '<entity-name-4>', '<entity-name-5>']


def to_rgb(color):
    rgb = mcolors.CSS4_COLORS[color.lower()]
    return [int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:7], 16)]

def light_post(entity, brightness, color, transition):
    payload = {'entity_id': entity, 'brightness': brightness, 'rgb_color': to_rgb(color)}
    if transition is not None:
        payload['transition'] = transition
    response = requests.post(f'{base_url}/api/services/light/turn_on',
                             headers=headers,
                             json=payload)

    if response.status_code == 200:
        return f'Light turned on {entity}'
    else:
        return f'Error {entity} {response.status_code} {response.reason}'
    
def light_post_all(entity, brightness, color, transition):
    payload = {'entity_id': entity, 'brightness': brightness, 'rgb_color': to_rgb(color)}
    if transition is not None:
        payload['transition'] = transition
    response = requests.post(f'{base_url}/api/services/light/turn_on',
                             headers=headers,
                             json=payload)

    if response.status_code == 200:
        return f'Light turned on {entity}'
    else:
        return f'Error {entity} {response.status_code} {response.reason}'
    
def light_post_all_thread(entity_list, brightness, color, transition):
    threads = []
    for entity in entity_list:
        thread = threading.Thread(target=light_post_all, args=(entity, brightness, color, transition))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def light_post_off(entity, transition):
    payload = {'entity_id': entity}
    if transition is not None:
        payload['transition'] = transition
    response = requests.post(f'{base_url}/api/services/light/turn_off',
                             headers=headers,
                             json=payload)

    if response.status_code == 200:
        return f'Light turned off {entity}'
    else:
        return f'Error {entity} {response.status_code} {response.reason}'
    
def light_post_off_all_thread(entity_list, transition):
    threads = []
    for entity in entity_list:
        thread = threading.Thread(target=light_post_off, args=(entity, transition))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()