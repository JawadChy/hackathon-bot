from bs4 import BeautifulSoup
from datetime import datetime

class Hackathon:
    def __init__(self, name, start, end, city, state, link):
        self.name = name
        self.start = datetime.strptime(start, "%Y-%m-%d")
        self.end = datetime.strptime(end, "%Y-%m-%d")
        self.start_string = datetime.strftime(self.start, "%m-%d-%y")
        self.end_string = datetime.strftime(self.end, "%m-%d-%y")
        self.city = city
        self.state = state
        self.location = (city + ", " + state)
        self.link = "<" + link + ">"
    
    @property
    def status(self):
        now = datetime.now()
        days_left = (self.start - now).days
        # More than 1 days before hackathon begins
        if days_left > 1:
            return f"{days_left} days until start!"
        # Approx 1 day remaining before hackathon begins
        elif days_left == 1:
            return "1 day left until start!"
        # TODO:
        # Have to implement specific time for below branches to work properly.
        # EX: Hackathon starts at 3PM Today, it's 11AM. Bot thinks hackathon is ongoing, but hackathon hasn't started.
        # Hackathon ongoing
        elif (self.start <= now <= self.end):
           return "Hackathon is ongoing!"
        # If above branches haven't excecuted, and this condition is true this means hackathon begins soon (<24Hrs Remaining)
        elif (now < self.start):
            return "Hackathon starting soon!"
        # If now is after end of hackathon hackathon has ended.
        elif (now > self.end):
            return "Hackathon has ended."
        
# For simplicity's sake I'm just creating an empty list, and we'll append hackathons to it.
# I really want to import sqlite3 and store hackathons in the DB, so in the future I might do that.
hackathons = []

# Open mlhevents.html file and read its contents into a string
with open('mlhevents.html', 'r') as f:
    contents = f.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(contents, 'html.parser')

# Find all divs with the class 'event-wrapper'
event_cards = soup.find_all('div', class_='event-wrapper')

# Iterate through all cards, and collect information about each event and create hackathon object for each corresponding event
for event in event_cards:
    event_name_tag = event.find('h3', class_='event-name')
    event_name = event_name_tag.text if event_name_tag else None

    event_start_meta = event.find('meta', itemprop='startDate')
    event_start = event_start_meta['content'] if event_start_meta else None

    event_end_meta = event.find('meta', itemprop='endDate')
    event_end = event_end_meta['content'] if event_end_meta else None

    event_city_tag = event.find('span', itemprop='city')
    event_city = event_city_tag.text if event_city_tag else None

    event_state_tag = event.find('span', itemprop='state')
    event_state = event_state_tag.text if event_state_tag else None

    event_link_a = event.find('a', class_='event-link')
    event_link = event_link_a['href'] if event_link_a else None

    if event_name and event_start and event_end and event_city and event_state and event_link:
        hackathon_to_add = Hackathon(event_name, event_start, event_end, event_city, event_state, event_link)
        hackathons.append(hackathon_to_add)