import re
import requests
from bs4 import BeautifulSoup

PAGE_URL = 'https://google.com'

def get_html_of(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)
    return resp.text

def get_text_of_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def list_of_words(text):
    return re.findall(r"\w+", text)

def dict_word_count(wordlist):
    worddict = {}
    for word in wordlist:
        if word not in worddict:
            worddict[word] = 1
        else:
            count = worddict.get(word)
            worddict[word] = count + 1       
    return worddict

def get_sorted_tupel_list(worddict):
    return sorted(worddict.items(), key=lambda item: item[1], reverse=True)

def count_words():
    html = get_html_of(PAGE_URL)
    text = get_text_of_html(html)
    wordlist = list_of_words(text)
    worddict = dict_word_count(wordlist)
    sortedfinallist = get_sorted_tupel_list(worddict)
    for index, word in enumerate(sortedfinallist):
        if index >= min(5, len(sortedfinallist)):
            break
        print(word[0], "->", word[1])

count_words()