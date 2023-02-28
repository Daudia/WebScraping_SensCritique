import time
import requests
from bs4 import BeautifulSoup
import sqlite3
from selenium import webdriver

# Script for Selenium to automatically scroll to the bottom of the page to fully load it
driver = webdriver.Chrome(executable_path=r"C:\Users\mathe\Downloads\chromedriver.exe")
driver.get('https://www.senscritique.com/musique/tops/top100-des-top10')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait for the second half of the page to load
time.sleep(10)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

# Find all the albums page url endings by searching for the relevant HTML tags and attributes
album_titles = soup.find_all('a', {
    'class': 'Text__SCText-sc-kgt5u3-0 Link__SecondaryLink-sc-1vfcbn2-1 gwWwBt eDKWEX '
             'ProductListItem__StyledProductTitle-sc-ico7lo-3 ivaIVy'},
                             href=True)

# Creating a list containing all the albums page url
href = []

for i in range(len(album_titles)):
    href.append("https://www.senscritique.com" + album_titles[i]['href'])

title_list = []
publication_year_list = []
artist_list = []
number_of_rating_list = []
global_rating_list = []
label_list = []
registered_number_list = []
favorite_number_list = []

for i in range(len(href)):
    print(len(href), i)
    url = href[i]

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the album title
    album_title = soup.find_all('h1')
    title_list.append(album_title[0]['title'])

    # Get the year of publication
    publication_year = soup.find_all('p', {
        'class': 'Text__SCTitle-sc-kgt5u3-1 CoverProductInfos__StyledText-sc-cbcfd0-10 hDmvGP fnFfaR'})
    publication_year_list.append(publication_year[0].text)

    # Get the artist
    artist = soup.find_all('span', href=True)
    artist_list.append(artist[0].text)

    # Get the number of ratings and the number of time the album was added to registered
    number_of_rating_and_registered = soup.find_all('p', {
        'class': 'Text__SCText-sc-kgt5u3-0 Stats__Text-sc-l0a962-2 hrLruZ IwdGM'})
    number_of_rating_list.append(number_of_rating_and_registered[0].text)
    registered_number_list.append(number_of_rating_and_registered[1].text)

    # Get the global rating
    global_rating = soup.find_all('div', {'class': 'Rating__GlobalRating-sc-1rkvzid-5 eCIKNi'})
    global_rating_list.append(global_rating[0].text)

    # Get the number of time the album was added to favorites
    favorite_number = soup.find_all('p', {'class': 'Text__SCText-sc-kgt5u3-0 Stats__Text-sc-l0a962-2 hrLruZ FlIXF'})
    favorite_number_list.append(favorite_number[0].text)

# Création d'une connexion à la base de données
conn = sqlite3.connect('album_top_100.db')

# Création d'une table dans la base de données
conn.execute('''
    CREATE TABLE album_top_100
    (ranking INTEGER PRIMARY KEY,
    title TEXT,
    publication_year INTEGER,
    artist TEXT,
    global_rating FLOAT,
    rating_number INTEGER,
    registered_number INTEGER,
    favorite_number INTEGER)
''')

# Insertion des données dans la table
for i in range(len(title_list)):
    conn.execute(
        'INSERT INTO album_top_100 (ranking, title, publication_year, artist, global_rating, rating_number, '
        'registered_number, favorite_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (
            i + 1, title_list[i], publication_year_list[i], artist_list[i], global_rating_list[i],
            number_of_rating_list[i],
            registered_number_list[i], favorite_number_list[i]))

# Validation des changements dans la base de données
conn.commit()

# Fermeture de la connexion à la base de données
conn.close()
