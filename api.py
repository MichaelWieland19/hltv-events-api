from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def get_all():
    return '', 204

@app.route('/matches-from-event')
def get_matches_for_event():
    # Fetch featured events
    featured_events = fetch_hltv_events()

    # Initialize a list to store matches for each event
    events_matches = []

    # Iterate over each featured event to fetch matches
    for event in featured_events:
        event_matches = fetch_matches_for_event(event)
        events_matches.append(event_matches)

    return jsonify(events_matches)

def fetch_matches_for_event(event):
    # Web scraping logic to fetch matches for a specific event
    # For each event, you will need to determine the URL of the event page

    event_url = generate_clean_url(event['id'],event['name'])  # Assuming you have stored the URL of the event in the event object
    # Use the event URL to make a request and scrape match details

    # Placeholder for match details
    match_details = []

    # Psuedo code to scrape match details from event page
    # This will involve finding the appropriate HTML elements and extracting match information

    # Append match details to the list

    return match_details
@app.route('/events')
def get_events():
    # Web scraping logic to fetch events from HLTV.org
    events = fetch_hltv_events()
    return jsonify(events)

def fetch_hltv_events():
    # Define a custom User-Agent header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Make a GET request to the HLTV events page with the custom User-Agent header
    response = requests.get('https://www.hltv.org/events', headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the container element that holds the featured event details
        featured_events_container = soup.find('div', class_='tab-content', id='FEATURED')

        # Initialize a list to store featured event details
        featured_events = []

        # Find all the ongoing event holders under the featured events container
        ongoing_event_holders = featured_events_container.find_all('div', class_='ongoing-event-holder')

        # Loop through each ongoing event holder to extract event details
        for event_holder in ongoing_event_holders:
            # Extract event details such as name, date, location, etc.
            name = event_holder.find('div', class_='event-name-small').text.strip()
            date = event_holder.find('span', class_='col-desc').text.strip()

            # Extract the event URL to get the event ID
            event_url = event_holder.find('a')['href']
            event_id = event_url.split('/events/')[1].split('/')[0]

            # Check if the location element exists
            location_elem = event_holder.find('div', class_='eventlocation')
            location = location_elem.text.strip() if location_elem else None

            # Create a dictionary to store the event details
            event_details = {
                'id': event_id,
                'name': name,
                'date': date,
                'location': location
            }

            # Add the event details to the list of featured events
            featured_events.append(event_details)

        return featured_events
    else:
        # Handle failed request
        print('Failed to fetch HLTV events:', response.status_code)
        return []


# Function used to clean the event name for URL input
def generate_clean_url(event_id,event_name):
    # Replace the spaces with hyphens and remove any newlines
    event_name = event_name.replace(' ','-').split('\n')[0]
    # Make all lowercase
    event_name = event_name.lower()
    # Create the URL
    event_url = f'https://www.hltv.org/events/{event_id}/{event_name}'
    return event_url


# Test the function
featured_events = fetch_hltv_events()
for event in featured_events:
    print(generate_clean_url(event['id'],event['name']))

if __name__ == '__main__':
    app.run(debug=True)