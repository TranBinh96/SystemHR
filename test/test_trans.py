import configparser
import os

config = configparser.ConfigParser()
config.read('translations.ini', encoding='utf-8')

print("Sections:", config.sections())
print("Vietnamese welcome:", config['vi']['welcome_back'])
print("English welcome:", config['en']['welcome_back'])
print("Japanese welcome:", config['ja']['welcome_back'])
