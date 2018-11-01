# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import tools
import data
import sys
import os


if __name__ == '__main__':

    if len(sys.argv[0:]) != 2:
        print("Required parameter is missing")
        sys.exit(1)

    input_file = sys.argv[1]
    if os.path.isfile(input_file) == True:
        print("Checking if updated")
        book = open(input_file, "r", encoding = 'utf-8')
        markup = tools.Knigu(book)
        book.close()
        if markup.is_updated(data.URL, markup.soup):
            print("File is up to date")
            sys.exit(1)
        else:
            print("File is NOT up to date")
            print("Do you want to update? (y/n): ")
            user_input = input()
            if user_input == "y":
                print("Book being updated...")
                tools.update(data.URL, markup.soup)
                book = open(input_file, 'w', encoding = "utf-8")
                book.write(str(markup.soup))
                book.close()
                print("Updated!")
                sys.exit(1)
            print("Good bye")
            sys.exit(1)
    else:
        print("Create new book? (y/n): ")
        user_input = input()
        if user_input == "y":
            new_book = tools.Knigu()
            print(new_book.content)
            sys.exit(1)
        print("Good bye.")
        sys.exit(1)
