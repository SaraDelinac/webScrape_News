# webScrape_News
web scraping of a local newpage Dziennik Baltycki, searching for articles with news about cybersecurity

Used libraries: BeautifulSoup, requests, re, csv

The script is iterating through the last 10 pages of the Polish business news page https://dziennikbaltycki.pl/strefa-biznesu/z-regionu and searching for occurences of words 'data leak', 'hack', 'cyber-' and 'digital' with different suffixes. All the articles with more than 2 occurrences of these words are written down in a csv file in the format: [article headline, number of word occurences, link to the article]. After the iteration, the number of articles that have been searched is written down in the file as well.
