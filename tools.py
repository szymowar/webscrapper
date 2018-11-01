# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re

def is_string(s):
    return isinstance(s, str)

def get_all_archive_links(link, number_of_subsites=14):
    link_list = []
    for page in range(1, number_of_subsites + 1):
        p = ArchiveLinks(link, page)
        link_list += p.get_current_page_links()
    return link_list
# functions below organize data from scrapped website and create html

def create_html_comments(comments):
    new_comments = ''
    for c in comments:
        comment = PageComment(c)
        new_comments += article_comments(comment.get_pub_date(), \
        comment.get_username(), comment.get_comment_content())
    return new_comments


def create_html_art_content(url, till = 2):
    links = get_all_archive_links(url)
    links = links[0:till]
    new_page_content =''
    new_table_of_content = ''
    table_and_content = []
    for link in links:
        page = PageContent(link)
        new_table_of_content += table_of_content(page.get_date(), page.get_title())
        new_page_content += article_header_content(page.get_date(),\
         page.get_title(), page.get_content())\
         + create_html_comments(page.get_comments())
    table_and_content.append(new_table_of_content)
    table_and_content.append(new_page_content)
    return table_and_content

#functions below create html pieces for knigu

def table_of_content(date,title):
    return """
    <div class="header">
        <div class="article-data">{date}
        </div>
        <div>............</div>
        <div class="article-title"><a href="#{date}" class="tableLinks">{title}</a>
        </div>
    """.format(date=date, title=title)

def article_header_content(date, title, article):
    return """<div class="header header-art">
    <div class="article-data">{date}
    </div>
    <div>-</div>
    <div class="article-title" id="{date}">{title}
    </div>
</div>
<br>
<br>
<div class="article" >
    {article}
    </div>
<hr>
<hr>""".format(date=date, title=title, article=article)

def article_comments(comment_date, user, comment_content):
    return """<div class="header header-comment">
        <div class="comment-data">{comment_date}
        </div>
        <div> : </div>
        <div class="user">{user}
        </div>
    </div>
    <hr>
    <div class="comment">
        {comment_content}
    </div>
    <hr>
    <hr>""".format(comment_date=comment_date, user=user, comment_content=comment_content)

def create_base():
    return """<!DOCTYPE HTML>
            <html lang="eng">
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <div class="content" id="independenttraderScrappedBook">
                    <div class="table-content" id="table">
                        </div>
                    <div class="content-article" id="art">
                        </div>
                </div>
            </body>
            </html>"""

#funcions that organize and update content in Knigu
def content_book_links(soup):
    return len(soup.find_all(class_="tableLinks"))

def diff_archiv_and_book(URL, soup):
    return len(get_all_archive_links(URL)) - content_book_links(soup)

def add_to_table(table_links, soup):
    soup.find(id = "table").append(table_links)

def add_to_content(content, soup):
    soup.find(id = "art").append(content)

def add_updated_data(table_links, content, soup):
    add_to_table(table_links, soup)
    add_to_content(content, soup)

def update(URL, soup, till=2):
    update_content = create_html_art_content(URL, till)
    add_updated_data(update_content[0], update_content[1], soup)

class Knigu:
    URL = 'https://independenttrader.pl'

    def __init__(self, content = create_base()):
        self.content = content
        if isinstance(self.content, str):
            self.soup = BeautifulSoup(self.content, 'html.parser')
        else:
            self.soup = BeautifulSoup(self.content, 'html.parser')


    def is_updated(self, URL, soup):
        if diff_archiv_and_book(URL, soup) == 0:
            return True
        else:
            return False


class PageContent:

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


class PageComment:

    def __init__(self,comment):
        self.comment = comment

    def get_pub_date(self):
        comment_pub_date = self.comment.find('time').string.strip()
        return comment_pub_date

    def get_username(self):
        comment_username = self.comment.find(class_ = re.compile('cWho')).string.strip()
        return comment_username

    def get_comment_content(self):
        comment_content = self.comment.find(class_ = 'edit-comment')
        comment_content = comment_content.find_all(string= is_string)
        comment_content = ''.join(comment_content).strip()
        return comment_content

class ArchiveLinks:

    def __init__(self, url, page = 1):
        self.url = url
        self.arch_url = '/archiwum.html'
        self.page = '?page=' + str(page)
        self.pagelink = requests.get(self.url + self.arch_url)
        self.soup = BeautifulSoup(self.pagelink.text, 'html.parser')


    def get_current_page_links(self):
        links = self.soup.tbody.find_all('a')
        linksList = []
        for link in links:
            liveLink = self.url + link.get('href')
            linksList.append(liveLink)
        return linksList

    def get_number_of_pages(self):
        res = self.soup.find(class_='next').previous_sibling()[0].string
        return res
