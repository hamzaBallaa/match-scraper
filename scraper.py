import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
URL = "https://shot.yacine-tv.tv/matches-today/"

def scrape_matches():
    # Send a GET request to the website
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all match containers
    matches = []
    match_containers = soup.find_all('div', class_='match-container')
    
    for container in match_containers:
        # Extract team names
        team1_name = container.find('div', class_='team-name').get_text(strip=True)
        team2_name = container.find_all('div', class_='team-name')[1].get_text(strip=True)

        # Extract team logos
        team1_logo = container.find('img', class_='hqy-lazy')['data-src']
        team2_logo = container.find_all('img', class_='hqy-lazy')[1]['data-src']

        # Extract match time
        match_time = container.find('div', class_='match-time').get_text(strip=True)

        # Extract channel and league info
        channel_info = container.find('li').get_text(strip=True)
        league_info = container.find_all('li')[2].get_text(strip=True)

        # Add match data to the list
        matches.append({
            'team1': {
                'name': team1_name,
                'logo': team1_logo
            },
            'team2': {
                'name': team2_name,
                'logo': team2_logo
            },
            'time': match_time,
            'channel': channel_info,
            'league': league_info
        })

    return matches

def save_to_json(data, filename='matches.json'):
    # Save the extracted data to a JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Scrape matches and save to JSON
    matches = scrape_matches()
    if matches:
        save_to_json(matches)
    else:
        print("No matches found.")
