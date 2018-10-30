# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
import tools
import data

if __name__ == '__main__':
    print(tools.create_html_art_content(data.URL))
