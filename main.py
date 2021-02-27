from bs4 import BeautifulSoup
from random import choice
from time import sleep
import requests

BASE_URL = "http://quotes.toscrape.com/"

# def main():
#     authors = scrape_pages(url)
#
#     while True:
#         game_quote = random.choice(authors)
#         attemts = 4
#         print(game_quote)
#         print("Who is the author of: "+game_quote[0])
#         author_birthday = get_author_birthday(url+game_quote[2])
#
#         while attemts > 0:
#             if check_answer(attemts, game_quote[1], author_birthday):
#                 print("WOO-HOO")
#                 print("You are right")
#                 break
#             elif attemts > 1:
#                 attemts -= 1
#                 print("it is wrong answer.")
#                 print(f"{attemts} attemts left")
#             elif attemts == 1:
#                 attemts -= 1
#                 print("You lose the game")
#         if input("do you want to play again? (yes/no)") == "no":
#             break
#
#     print("Good luck!")

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
        # sleep(2)
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

main()
