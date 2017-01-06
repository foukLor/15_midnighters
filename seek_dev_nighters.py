import requests
import pytz
from datetime import datetime

API_URL = 'https://devman.org/api/challenges/solution_attempts/'

def request_api_page(page_num):
    payload = {'page':page_num}
    return requests.get(API_URL, params=payload)

def load_attempts():
    pages = 1
    first_page = 1
    response = request_api_page(first_page).json()
    number_of_pages = response['number_of_pages'];
    for page_num in range(number_of_pages):
        for record in response['records']:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone']
            }
        response = request_api_page(page_num + 1).json()


def get_midnighters(records):
    midnighters = []
    for record in records:
        time = get_time(record['timestamp'], record['timezone'])
        if time is not None and (1<= time.hour < 5):
            midnighters.append(record['username'])
    return set(midnighters)


def get_time(timestamp, timezone):
    if timestamp is None or timezone is None:
        return None
    return datetime.fromtimestamp(timestamp, pytz.timezone(timezone))


def print_midnighters(midnighters):
    print("These people solved tasks after midnight")
    for person in midnighters:
        print(person)


if __name__ == '__main__':
    records = load_attempts()
    print_midnighters(get_midnighters(records))

