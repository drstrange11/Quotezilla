import requests
from bs4 import BeautifulSoup
from random import choice
import itertools
import sys
import time

all_quotes = []
BASE_URL = "http://quotes.toscrape.com"

#Scrapes the title, author and the about author page

def scrape():
    url = "/page/1"
    while url:
        src_code = requests.get(f"{BASE_URL}{url}").text
        soup = BeautifulSoup(src_code, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({"text": soup.find(class_="text").get_text(),
                               "author": soup.find(class_="author").get_text(),
                               "link": soup.find(class_="author").find_next_sibling()["href"]})
            nxt = soup.find(class_="next")
            url = nxt.find("a")["href"] if nxt else None


def play_game():
    rem_guess = 4
    quote_pick = choice(all_quotes)
    print("\n\nHere's a quote:\n\n", quote_pick["text"])
    while rem_guess > 0:
        print(f"\nWho said this? Guesses remaining: {rem_guess}")
        ans = input().lower()
        if ans == quote_pick["author"].lower():
            print("\nBAZINGA! You guessed correctly! Congratulations!")
            break
        else:
            rem_guess -= 1
            if rem_guess != 0:
                print("\nOhh...That's Wrong! It's okay, try again")
                print("\nHere's a hint for you :)")
            if rem_guess == 3:
                bio = requests.get(BASE_URL + quote_pick["link"]).text
                bio_soup = BeautifulSoup(bio, "html.parser")
                born_date = bio_soup.find(class_="author-born-date").get_text()
                place = bio_soup.find(class_="author-born-location").get_text()
                print(f"The author was born in {born_date} in {place}")
            elif rem_guess == 2:
                print(
                    f"\nThe Author's first name starts with {quote_pick['author'].split()[0][0]}")
            elif rem_guess == 1:
                print(
                    f"\nThe Author's last name starts with {quote_pick['author'].split()[1][0]}")
            else:
                print(
                    f"\nSorry, you've ran out of guesses. The Answer is {quote_pick['author']}")

    print("\nWould you like to play again? (Y/N)")
    reply = input()
    if reply.lower() in ['no', 'n']:
        print("\nThanks for playing. See you again next time!")
    else:
        print("\nHere we go again.....")
        return play_game()

#Load Screen
def animate():
    i = 1
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        time.sleep(0.1)
        i += 1

        if i == 150: #This is just to compensate the waiting time 
            sys.stdout.write("\rLoaded successfully!")
            break

if __name__ == "__main__":
    print("\nWELCOME TO QUOTEZILLA!!  :P ")
    print("\nShall we start playing? (Y/N)")
    if(input().lower() in ['yes', 'yeah', 'y']):
        print("\nPlease wait. Getting things ready for you.\n")
        animate()
        scrape()
        play_game()
    else:
        print("Ohh Okay :( . See ya again next time!")
