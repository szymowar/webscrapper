# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re

def is_string(s):
    return isinstance(s, str)

URL1 = 'https://independenttrader.pl/czym-fundusze-etf-podpadly-finansowej-elicie.html'
URL2 = 'https://independenttrader.pl/jakie-bledy-popelniaja-inwestorzy.html'

class PageContent():
    def __init__(self, link):
        self.link = link
        self.pagelink = requests.get(self.link)
        self.soup = BeautifulSoup(self.pagelink.text, 'html.parser')
        self.post_date_and_title = self.soup.find(class_ = "additionalBarWithoutBorder")

    def get_title(self):
        post_title = self.post_date_and_title.h1.string.strip()
        return post_title

    def get_date(self):
        post_date = self.post_date_and_title.find(class_ = "icon-clock").next_sibling.strip()
        return post_date

    def get_content(self):
        post_content = self.soup.find(class_ = "postContent").get_text()
        return post_content
    def get_comments(self):
        comment_section = self.soup.find_all(id = re.compile('comment-'))
        return comment_section


p1 = PageContent(URL1)
p2 = PageContent(URL2)


"""
output_file = open('letter', 'w', encoding='utf-8')
output_file.write(p1.get_date())
output_file.write('\n\n')
output_file.write(p2.get_title())
output_file.write('\n')
output_file.write(p1.get_content())
"""
#scrapping article comment section

class Comment:
    def __init__(self,comment):
        self.comment = comment
    def show(self):
        print(self.comment)
    def get_pub_date(self):
        comment_pub_date = self.comment.find('time').string.strip()
        return comment_pub_date
    def get_username(self):
        comment_username = self.comment.find(class_ = 'cWho' or 'cWhoAdmin').string.strip()
        return comment_username
    def get_comment_content(self):
        comment_content = self.comment.find(class_ = 'edit-comment')
        comment_content = comment_content.find_all(string= is_string)
        comment_content = ''.join(comment_content).strip()
        return comment_content

data = p1.get_comments()[1]


p3 = Comment(data)

print(p3.show())

"""
output_file = open('letter', 'w', encoding='utf-8')
output_file.write('\n')
output_file.write(p1.get_username())
output_file.write('\t')
output_file.write(p1.get_pub_date())
output_file.write('\n\n')
output_file.write(p1.get_comment_content())

output_file.close()
"""
