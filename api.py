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
    print(featured_events)
    # Iterate over each featured event to fetch matches
    for event in featured_events:
        event_matches = fetch_matches_for_event(event)
        events_matches.append(event_matches)

    return jsonify(events_matches)

def fetch_matches_for_event(event):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    event_url = generate_clean_url(event['id'], event['name'])  # Assuming you have stored the URL of the event in the event object

    # Create the matches URL
    event_url_base = '/'.join(event_url.split('/')[:-1])
    event_url_base += '/matches'

    print(event_url_base)
    # Make a request to the matches page
    response = requests.get(event_url_base, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        matches = soup.find_all('div', class_='upcomingMatch')

        match_details = []

        for match in matches:
            match_time = match.find('div', class_='matchTime').text.strip()
            team1_container = match.find('div', class_='matchTeam team1')
            team2_container = match.find('div', class_='matchTeam team2')
            team1 = team1_container.find('div', class_='matchTeamName').text.strip()
            team2 = team2_container.find('div', class_='matchTeamName').text.strip()
            team1_logo = team1_container.find('img')['src'] if team1_container.find('img') else None
            team2_logo = team2_container.find('img')['src'] if team2_container.find('img') else None

            match_details.append({
                'time': match_time,
                'team1': team1,
                'team2': team2,
                'team1_logo': team1_logo,
                'team2_logo': team2_logo
            })

        return match_details
    else:
        print('Failed to fetch matches page:', response.status_code)
        return None

@app.route('/eventsUpcoming')
def get_upcoming_events():

    events = fetch_upcoming_hltv_events()
    return jsonify(events)

def fetch_upcoming_hltv_events():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get('https://www.hltv.org/events', headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        upcoming_events_container = soup.find('div', class_='big-events')

        if upcoming_events_container:
            upcoming_events = []

            upcoming_event_holders = upcoming_events_container.find_all('a', class_='big-event')

            for event_holder in upcoming_event_holders:
                name_elem = event_holder.find('div', class_='big-event-name')
                name = name_elem.text.strip() if name_elem else None

                date_elem = event_holder.find('td', class_='col-value col-date')
                date = date_elem.text.strip() if date_elem else None

                location_elem = event_holder.find('span', class_='big-event-location')
                location = location_elem.text.strip() if location_elem else None

                # Extract the event URL to get the event ID
                event_url = event_holder['href']
                event_id = event_url.split('/events/')[1].split('/')[0] if event_url else None

                # Determine the event status
                status = "Tier 1" if "big-events" in event_holder.parent.get('class', []) else "Tier 2 or lower"

                event_details = {
                    'id': event_id,
                    'name': name,
                    'date': date,
                    'location': location,
                    'status': status
                }

                upcoming_events.append(event_details)

            return upcoming_events

    print('Failed to fetch upcoming HLTV events:', response.status_code)
    return []

@app.route('/eventsOngoing')
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

        # Check if featured_events_container exists
        if featured_events_container:
            # Initialize a list to store featured event details
            featured_events = []

            # Find all the ongoing event holders under the featured events container
            ongoing_event_holders = featured_events_container.find_all('div', class_='ongoing-event-holder')

            # Loop through each ongoing event holder to extract event details
            for event_holder in ongoing_event_holders:
                # Extract event details such as name, date, location, etc.
                name_elem = event_holder.find('div', class_='event-name-small')
                name = name_elem.text.strip() if name_elem else None
                
                date_elem = event_holder.find('span', class_='col-desc')
                date = date_elem.text.strip() if date_elem else None

                # Extract the event URL to get the event ID
                event_anchor = event_holder.find('a')
                event_url = event_anchor['href'] if event_anchor else None
                event_id = event_url.split('/events/')[1].split('/')[0] if event_url else None

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
            print('No featured events found.')
            return []
    else:
        # Handle failed request
        print('Failed to fetch HLTV events:', response.status_code)
        return []


# Function used to clean the event name for URL input
def generate_clean_url(event_id, event_name):
    if event_name:
        event_name = event_name.replace(' ', '-').split('\n')[0]
        clean_url = f'https://www.hltv.org/events/{event_id}/{event_name}'
        return clean_url
    else:
        print('Event name is missing.')
        return None


# Test the function
featured_events = fetch_hltv_events()
for event in featured_events:
    print(generate_clean_url(event['id'],event['name']))

if __name__ == '__main__':
    app.run(debug=True)