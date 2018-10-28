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


class PageComment:
    def __init__(self,comment):
        self.comment = comment
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

class ArchiveLinks:
    def __init__(self, url, page = 1):
        self.url = url
        self.arch_url = '/archiwum.html'
        self.page = '?page=' + str(page)
        self.pagelink = requests.get(self.url + self.arch_url)
        self.soup = BeautifulSoup(self.pagelink.text, 'html.parser')
        self.linksList = []

    def get_current_page_links(self):
        links = self.soup.tbody.find_all('a')
        for link in links:
            liveLink = self.url + link.get('href')
            self.linksList.append(liveLink)
        return self.linksList

    def get_number_of_pages(self):
        res = self.soup.find(class_='next').previous_sibling()[0].string
        return res
