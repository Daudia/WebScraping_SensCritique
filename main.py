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

titles_list = []
publi_years_list = []
artist_list = []
number_of_rating_list = []
global_rating_list = []
label_list = []
registered_number_list =[]
favorite_number_list = []


for i in range (len(href)) :
    url = href[i]

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the album title
    album_title = soup.find_all('h1')
    titles_list.append(album_title[0]['title'])

    # Get the year of publication
    publi_year = soup.find_all('p', {
        'class': 'Text__SCTitle-sc-kgt5u3-1 CoverProductInfos__StyledText-sc-cbcfd0-10 hDmvGP fnFfaR'})
    publi_years_list.append(publi_year[0].text)

    # Get the artist
    artist = soup.find_all('span',href=True)
    artist_list.append(artist[0].text)

    # Get the number of ratings and the number of time the album was added to registered
    number_of_rating_and_registered = soup.find_all('p', {'class' : 'Text__SCText-sc-kgt5u3-0 Stats__Text-sc-l0a962-2 hrLruZ IwdGM'})
    number_of_rating_list.append(number_of_rating_and_registered[0].text)
    registered_number_list.append(number_of_rating_and_registered[1].text)

    # Get the global rating
    global_rating = soup.find_all('div', { 'class' : 'Rating__GlobalRating-sc-1rkvzid-5 eCIKNi'})
    global_rating_list.append(global_rating[0].text)

    # Get the number of time the album was added to favorites
    favorite_number = soup.find_all('p', {'class': 'Text__SCText-sc-kgt5u3-0 Stats__Text-sc-l0a962-2 hrLruZ FlIXF'})
    favorite_number_list.append(favorite_number[0].text)

print (titles_list)
print (publi_years_list)
print (artist_list)
print (number_of_rating_list)
print (registered_number_list)
print (global_rating_list)
print (favorite_number_list)