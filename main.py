# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

def is_string(s):
    return isinstance(s, str)

link = requests.get('https://independenttrader.pl/czym-fundusze-etf-podpadly-finansowej-elicie.html')
soup = BeautifulSoup(link.text, 'html.parser')
# scrapping article content
post_date_and_title = soup.find(class_ = "additionalBarWithoutBorder")
post_date = post_date_and_title.find(class_ = "icon-clock").next_sibling.strip()
post_title = post_date_and_title.h1.string.strip()
post_content = soup.find(class_ = "postContent").get_text()
output_file = open('letter', 'w', encoding='utf-8')
output_file.write(post_date)
output_file.write('\n\n')
output_file.write(post_title)
output_file.write('\n')
output_file.write(post_content)

#scrapping article comment section
comment_section = soup.find(class_ = "commentsList").find(id = "comment-74548")
comment_pub_date = comment_section.find('time').string.strip()
comment_username = comment_section.find(class_ = 'cWho').string.strip()
comment_content = comment_section.find(class_ = 'edit-comment')
comment_content = comment_content.find_all(string= is_string)
comment_content = ''.join(comment_content).strip()
output_file.write('\n')
output_file.write(comment_username)
output_file.write('\t')
output_file.write(comment_pub_date)
output_file.write('\n\n')
output_file.write(comment_content)
output_file.close()
