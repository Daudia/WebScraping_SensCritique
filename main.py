import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.senscritique.com/musique/tops/top100-des-top10'

# Send a request to the page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the albums page url endings by searching for the relevant HTML tags and attributes
album_titles = soup.find_all('a', {
    'class': 'Text__SCText-sc-kgt5u3-0 Link__SecondaryLink-sc-1vfcbn2-1 gwWwBt eDKWEX '
             'ProductListItem__StyledProductTitle-sc-ico7lo-3 ivaIVy'},
                             href=True)

# Creating a list containing all the albums page url
href = []
for i in range (len(album_titles)):
    href.append("https://www.senscritique.com"+album_titles[i]['href'])

print(href)
