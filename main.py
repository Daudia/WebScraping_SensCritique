import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.senscritique.com/musique/tops/top100-des-top10'

# Send a request to the page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the album titles by searching for the relevant HTML tags and attributes
album_titles = soup.find_all('a', {
    'class': 'Text__SCText-sc-kgt5u3-0 Link__SecondaryLink-sc-1vfcbn2-1 gwWwBt eDKWEX '
             'ProductListItem__StyledProductTitle-sc-ico7lo-3 ivaIVy'},
                             href=True)

# Extract the text of the album titles and store them in a list
titles_list = [title.text for title in album_titles]

# Print the list of album titles
print(titles_list)
