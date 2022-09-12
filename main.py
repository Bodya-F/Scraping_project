from bs4 import BeautifulSoup
from random import choice
from time import sleep
import requests

BASE_URL = "http://quotes.toscrape.com/"

def play_game(all_quotes):
    quote = choice(all_quotes)
    remaining_guesses = 4
    guess = ""
    print(quote["text"])
    print(quote["author"])

    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input("Who is the author?\n")
        if guess.lower() == quote["author"].lower():
            print(f"U WIN")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            bith_date = soup.find("span").getText()
            bith_location = soup.find("span").find_next_sibling().getText()
            print(f"Here is author bio: {bith_date} {bith_location}")
        elif remaining_guesses == 2:
            print(f"the first char of the name is {quote['author'][0]}")
        elif remaining_guesses == 1:
            last_name = quote['author'].split(" ")[1]
            print(f"the first char of the last name is {last_name[0]}")
        else:
            print("sorry, you lost the game =(")

    again = ''
    while again not in ("yes", "y", "n", "no"):
        again = input("Do you want to play again?\n")

    if again.lower() == "y" or again.lower() == 'yes':
        return play_game(all_quotes)
    return None

def scrape_quotes():
    url = "/page/1"
    all_quotes = []

    while url:
        print(f"Scrapping following page: {BASE_URL}{url}")
        sleep(5)
        req = requests.get(f"{BASE_URL}{url}")
        data = BeautifulSoup(req.text, "html.parser")
        quotes = data.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({"text": quote.find(class_="text").getText(),
                            "author": quote.find("small").getText(),
                           "bio-link": quote.find("a")["href"]}
                           )

        is_next_page = data.find(class_="next")
        url = is_next_page.find("a")["href"] if is_next_page else None

    return all_quotes

def main():
    all_quotes = scrape_quotes()
    play_game(all_quotes)
    open_file()
#

def open_file():
    f = open('/Users/bohdan/Documents/names.txt', 'r')
    content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    full_name = soup.find_all(class_="attendee-list-item_username__2CJh4 test-id-attendee-name")
    headline = soup.find_all(class_="attendee-list-item_headline__1Z-H5 test-id-attendee-headline")

    for i in range(0, len(full_name)):
        print(f"{full_name[i].get_text()}|{headline[i].get_text()}")

    # print(full_name[0].get_text(), headline)
main()
