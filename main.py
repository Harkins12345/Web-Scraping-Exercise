import csv
import requests as r
from bs4 import BeautifulSoup
from time import sleep


def main():
    with open('songInformation.csv', mode='w', newline='', encoding='utf-8') as f:
            TITLES = ['Post Title', 'Post Url', 'Download Link', 'Date Posted']
            writer = csv.writer(f, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)

            writer.writerow(TITLES)

            resp = r.get('https://justnaija.com/music-mp3/')
            page_html = resp.text

            soup = BeautifulSoup(page_html, 'html.parser')

            links = soup.find_all('h3', {'class': 'file-name myhome'})
            next_button = soup.find('a', {'title': 'Next'})

            while next_button:

                #try:

                    next_page_url = next_button['href']

                    for link_element in links:
                        a_tag = link_element.find('a')

                        url = a_tag['href']
                        song_title = a_tag.string


                        song_page_resp = r.get(url)

                        song_page_html = song_page_resp.text

                        song_page_soup = BeautifulSoup(song_page_html, 'html.parser')

                        download_button = song_page_soup.find('p', {'class': 'song-download'})
                        if download_button:
                            download_url = download_button.find('a')['href']
                        else:
                            download_url = None

                        date_div = song_page_soup.find('div', {'class': 'Adxdetails'})
                        date_element = date_div.find('time')

                        if date_element:
                            date_posted = date_element['datetime']
                        else:
                            date_posted = None


                        writer.writerow([song_title, url, download_url, date_posted])

                    resp = r.get(next_page_url)
                    page_html = resp.text

                    soup = BeautifulSoup(page_html, 'html.parser')

                    links = soup.find_all('h3', {'class': 'file-name myhome'})
                    next_button = soup.find('a', {'title': 'Next'})
                #except:
                    sleep(0.1)


if __name__ == "__main__":
    main()
