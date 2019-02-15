#          Pizza scraper
#   This software takes a bunch of websites and tries to scrape
#   data off of them. For now it's "hardcoded", as in it contains
#   no machine-learning like stuff. This is needed for an other repo of mine.

import re
import os
from requests import get
from requests import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

program_name    = "pizza scraper"
program_ver     = "0.0.1"

# Basic web scraping based on the following tutorial (as of 15/02/2018):
# https://realpython.com/python-web-scraping-practical-introduction/
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

# getGino() ~ this functions tries to parse ginopizza.hu to get pizza prices and names
def getGino():
    print("Trying to scrape ginopizza.hu...")

    raw_html = simple_get("http://www.ginopizza.hu/index.php?option=com_content&view=article&id=13:vekony-tesztas-pizza&catid=8:menu")

    if(len(raw_html) > 0):
        # Delete "gino.txt" if we have one
        if os.path.exists("gino.txt"):
            os.remove("gino.txt")

        # Actually parse the site
        html = BeautifulSoup(raw_html, 'html.parser')
        for i, tr in enumerate(html.select('tr')):
            name = ""
            price_28 = 0
            price_45 = 0

            # Skip the table header
            if(i == 0):
                continue

            for j, td in enumerate(tr.select('td')):
                if(j == 0):
                    tmp = td.text
                    name = re.sub(
                            r"(.*)\((.*)\)",
                            r"\1",
                            tmp)
                else:
                    if(j == 2):
                        tmp = td.text
                        m = re.search("[0-9]{3,4}", tmp)
                        price_28 = int(m.group(0))

                    if(j == 3):
                        tmp = td.text
                        m = re.search("[0-9]{3,4}", tmp)
                        price_45 = int(m.group(0))

            print("ADAT:", name, price_28, price_45)

            with open('gino.txt', 'a') as gino_file:
                gino_file.write("28,")
                gino_file.write(str(price_28))
                gino_file.write(",Gino,")
                gino_file.write(name)
                gino_file.write("\n")

                gino_file.write("45,")
                gino_file.write(str(price_45))
                gino_file.write(",Gino,")
                gino_file.write(name)
                gino_file.write("\n")

    else:
        print("Failed to scrape ginopizza.hu...")

# getszieg() ~ This function tries to scrape szigetelbar.hu
def getSziget():
    """
    print("Trying to scrape szigetelbar.hu")
    raw_html = simple_get("http://szigetetelbar.hu/index.php/pizza")

    if(len(raw_html) > 0):
        html = BeautifulSoup('html.parser', raw_html)
        print(html)
    else:
        print("Failed to scrape szigetetelbar.hu")
    """
    # Pass for now as there is an error occuring when doing simple_get(...)
    pass


# Main
def main():
    print("Welcome to ", program_name, " v", program_ver, ".", sep='')
    print()

    getGino()
    getSziget()

main()
