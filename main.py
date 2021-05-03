from selenium import webdriver
from bs4 import BeautifulSoup
import platform
import time

if platform.system() == "Windows":
    driver_path = 'chrome_driver/chromedriver.exe'
elif platform.system() == "Darwin":
    driver_path = 'chrome_driver/chromedriver'


def treat(page_source):
    try:
        return BeautifulSoup(page_source, "html.parser").find("title").text.replace(" - Wikipedia", "")
    except AttributeError:
        return "error"


def start(start_point="https://en.wikipedia.org/wiki/Special:Random",
          end_point="https://en.wikipedia.org/wiki/Special:Random",
          dr=None):
    options = webdriver.ChromeOptions()
    if dr is None:
        dr = webdriver.Chrome(
            driver_path,
            options=options,
        )
    dr.get(end_point)
    end_page = treat(dr.page_source)
    print(f"get to: {end_page}")
    time.sleep(5)
    dr.get(start_point)
    current_page = treat(dr.page_source)
    history = []
    while treat(dr.page_source) != end_page:
        if treat(dr.page_source) != current_page:
            history.append(current_page)
            current_page = treat(dr.page_source)
            if dr.current_url == "http://stop.com/":
                dr.close()
                return "0", []
            if dr.current_url == "https://venture.com/domains/restart.com":
                print(chr(27) + "[2J")
                start(dr=dr)
    score = 1050 - 50*len(history)
    history.append(current_page)
    dr.close()
    return score, history


if __name__ == '__main__':
    score, history = start()
    print(f"score: {score}\npath: {' -> '.join(history)}")

