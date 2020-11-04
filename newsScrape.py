#!/usr/bin/env python
'''Accessing a website'''
import urllib.request
import ssl
from bs4 import BeautifulSoup
import re
import os


def web_scrape(link, fileAddr):
    '''In website,
    click all subsequent links that begin with the same link string'''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    '#html = urllib.request.urlopen(link, context=ctx)#'
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    with open(fileAddr, 'w') as fhandle:
        for tag in tags:
            # print(tag.get('href', '')) #
            fhandle.write(tag.get('href', ''))
            fhandle.write('\n')
            if re.search(link, tag.get('href', '')):
                #try:
                req = urllib.request.Request(tag.get('href', ''), headers={'User-Agent': 'Mozilla/5.0'})
                nhtml = urllib.request.urlopen(req).read()
                '''nhtml = urllib.request.urlopen(tag.get('href', None))'''
                soup = BeautifulSoup(nhtml, 'html.parser')
                tags = soup('a')
                for tag in tags:
                    # print(tag.get('href', '')) #
                    fhandle.write(tag.get('href', ''))
                    fhandle.write('\n')
                #except:
                #    continue


def clean_data(fileAddr, destfile, searchstr):
    with open(destfile, 'w') as dhandle:
        with open(fileAddr, 'r') as fhandle:
            f = fhandle.readlines()
            f = list(set(f))
            for line in f:
                if (re.search(searchstr, line)) and (re.search('.ece', line)):
                    print(line)
                    dhandle.write(line)


if __name__ == '__main__':
    newsWebsite = "https://www.thehindu.com/"
    web_scrape(newsWebsite, 'newsLinks.txt')
    clean_data('newsLinks.txt', 'newsLinksCleaned.txt', newsWebsite)
    os.system("notify-send Ready newLinks")
