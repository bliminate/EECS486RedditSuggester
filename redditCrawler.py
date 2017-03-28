#!/usr/bin/env python

# Brian Lim
# blimmer

from bs4 import BeautifulSoup
import sys
import re
import os
import math
import sets
from urllib2 import urlopen
from urlparse import urljoin
import urllib2
import time

# function to add urls to queue of urls to visit
def get_urls(seed_url, source_url, tags, urls):
  count = 0
  # make sure the source url is https
  if source_url[4] != 's':
    source_url = source_url[:4] + 's' + source_url[4:]

  # run for each link on the page
  for tag in tags:
    link = tag.get('href', '/')
    # render the complete url
    url = urljoin(source_url.strip(), link.strip())
    # check to make sure url is in the eecs domain
    eecs_space = re.search('www\.eecs\.umich\.edu', url)

    # efficiency upgrade, filter out non-html urls
    pdf = re.search('.*\.pdf', url)
    jpg = re.search('.*\.jpg', url)
    png = re.search('.*\.png', url)
    eps = re.search('.*\.eps', url)
    cgi = re.search('.*\.cgi', url)
    docx = re.search('.*\.docx', url)
    mp4 = re.search('.*\.mp4', url)
    ogv = re.search('.*\.ogv', url)

    if pdf or jpg or png or eps or cgi or docx or mp4 or ogv:
      continue

    if eecs_space:
      # remove any search parameters, and make
      # sure all links are https
      clean_url = url.split('?')
      if clean_url[0][4] == 's':
        add = (clean_url[0].strip(), source_url.strip())
      else:
        c_url = clean_url[0][:4] + 's' + clean_url[0][4:]
        add = (c_url.strip(), source_url.strip())
      urls.append(add)
      count += 1
  return urls

# Crawl web starting with the seed url
def crawl(seed_url, visited_urls, max_urls):
  html_data = urlopen(seed_url).read()
  soup = BeautifulSoup(html_data, 'html.parser')
  a_tags = soup.find_all('a')
  urls = []
  urls = get_urls(seed_url, seed_url, a_tags, urls)
  visit_urls = []
  visit_urls.append(seed_url.strip())
  visited_urls.add((seed_url.strip(), seed_url.strip()))
  last = 0

  # crawl until max_urls unique urls have been crawled
  while len(visit_urls) < max_urls and len(urls) > 0:
    # check to see if this link has already been found
    if urls[0] in visited_urls:
      del urls[0]
      continue

    # If link has not been found, see if the destination
    # of the link has already been crawled, and does not
    # need to be crawled again
    elif urls[0][0] in visit_urls:
      visited_urls.add(urls[0])
      del urls[0]
      continue

    # Crawl the webpage
    try:
      html_d = urlopen(urls[0][0], timeout=9.05)

      # verify that it is an html page
      if 'html' not in html_d.headers.getheader('Content-Type'):
        #print 'non-html' + urls[0][0]
        del urls[0]
        continue

      # extract all of the anchor tags that contain links
      soup_d = BeautifulSoup(html_d, 'html.parser')
      b_tags = soup_d.find_all('a')
      urls = get_urls(seed_url, urls[0][0], b_tags, urls)
      visited_urls.add(urls[0])
      visit_urls.append(urls[0][0])
      del urls[0]

    # catch invalid urls
    except urllib2.HTTPError:
      del urls[0]

    except UnicodeEncodeError:
      del urls[0]

    except urllib2.URLError:
      del urls[0]

  return visit_urls, visited_urls

seed_file = sys.argv[1]
max_urls = sys.argv[2]

visited_urls = set()

start_time = time.time()
seeds = open(seed_file)
#Start crawl for each seed url.
for seed in seeds:
  results = crawl(seed, visited_urls, int(max_urls))

end_time = time.time()

print('Time to crawl: ' + str(end_time - start_time))

crawl_results = open('crawler.output', 'w')
for line in results[0]:
  output = line + '\n'
  crawl_results.write(output)

page_output = open('directed_edges.txt', 'w')
for line in results[1]:
  output = line[1] + ' ' + line[0] + '\n'
  page_output.write(output)
