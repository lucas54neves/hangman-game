import requests
import random

def get_words():
  response = requests.get('https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/BrazilianPortuguese_wordlist')

  text = response.text.split('<li><span lang="pt"><a href="/wiki/')[1:]

  return [element.split('>')[1].split('<')[0] for element in text]

def get_random_word():
  return random.choice(getWords())

def game():
  word = getRandomWord()
