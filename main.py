# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import tools
import data
import sys
import os
import html


if __name__ == '__main__':

    if len(sys.argv[0:]) != 2:
        print("Required parameter is missing")
        sys.exit(1)

    input_file = sys.argv[1]
    if os.path.isfile(input_file) == True:
        print("Checking if updated")
        book = open(input_file, "r", encoding = 'utf-8')
        old_book = tools.Knigu(book)
        book.close()
        if old_book.is_updated(data.URL, old_book.soup):
            print("File is up to date")
            sys.exit(1)
        else:
            print("File is NOT up to date")
            print("Do you want to update? (y/n): ")
            user_input = input()
            if user_input == "y":
                print("Book being updated...")
                tools.write_to_file(data.URL, old_book.soup, input_file)
                print("Updated!")
                sys.exit(1)
            print("Good bye")
            sys.exit(1)
    else:
        print("Create new book? (y/n): ")
        user_input = input()
        if user_input == "y":
            new_book = tools.Knigu()
            tools.write_to_file(data.URL, new_book.soup, input_file)
            print("Book created and up to date.")
            sys.exit(1)
        print("Good bye.")
        sys.exit(1)
