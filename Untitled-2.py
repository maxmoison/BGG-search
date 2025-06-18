import requests
import xml.etree.ElementTree as ET
import time
 
# Search for a game by name
def search_game(game_name):
    url = f'https://boardgamegeek.com/xmlapi/search?search={game_name}'
    response = requests.get(url)
    response.raise_for_status()
    return ET.fromstring(response.content)
 

# Get detailed info about a game by ID
def get_game_details(game_id):
    url = f'https://boardgamegeek.com/xmlapi/boardgame/{game_id}?stats=1'
    time.sleep(5)  # Respect BGG's rate limits
    response = requests.get(url)
    response.raise_for_status()
    return ET.fromstring(response.content)
game_input = input("what game are you looking for?")
print(game_input) 
search_results = search_game(game_input)
# Print out the entire XML response for debugging
print("Full XML response:")
print(ET.tostring(search_results, encoding="unicode"))
 
# Pick the first result
first_game = search_results.find("boardgame")
if first_game is not None:
    game_id = first_game.attrib["objectid"]
    print(f"Found Game ID: {game_id}")
 
    # Get details
    details = get_game_details(game_id)
    name = details.find("boardgame/name").text
    year = details.find("boardgame/yearpublished").text
    description = details.find("boardgame/description").text[:300] + "..."
    
    statistics = details.find("boardgame/statistics")
    ratings = statistics.find("ratings")
    average_rating = ratings.find("average").text
    min_players = details.find("boardgame/minplayers").text
    max_players = details.find("boardgame/maxplayers").text

 
    print(f"Title: {name}")
    print(f"Year: {year}")
    print(f"Description: {description}")
    print(f"Average rating: {average_rating}")
    print(f"Player: {min_players} - {max_players}")
else:
    print("Game not found.")
 