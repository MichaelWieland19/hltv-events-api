HLTV Events API
This API provides endpoints to retrieve information about upcoming, ongoing, and past events from HLTV.org, a leading Counter-Strike: Global Offensive (CS:GO) esports platform.

Endpoints:

1. /eventsUpcoming
Method: GET
Description: Fetches information about upcoming events.
Response: JSON object containing details of upcoming events, including event ID, name, date, and location.

2. /eventsOngoing
Method: GET
Description: Retrieves information about ongoing events.
Response: JSON object containing details of ongoing events, including event ID, name, date, and location.

3. /matches-from-event
Method: GET
Description: Fetches matches for each event, including upcoming and ongoing events.
Response: JSON object containing details of matches for each event, including match time, teams, and team logos.
Running the Application
Clone this repository to your local machine.
Install the required dependencies using pip install -r requirements.txt.
Run the Flask application using python app.py.
Access the API endpoints using the provided URLs.

Dependencies
Flask
BeautifulSoup4
Requests
