from bs4 import BeautifulSoup
import requests
import re
import csv

# all the search results will be written down in a created file.csv
file = open('strefa-biznesu.csv', 'w')
pagesrc = 'https://dziennikbaltycki.pl/strefa-biznesu/z-regionu'
source = requests.get(pagesrc).text
soup = BeautifulSoup(source, 'lxml')
writer = csv.writer(file)
writer.writerow(['Article headline', 'No of matches', 'Link'])

# loop over every page of the last 10 pages on the newspage Dziennik Baltycki
for page in range(1,10):
    nextpagesource = requests.get(f"https://dziennikbaltycki.pl/strefa-biznesu/z-regionu/{page}").text
    soup = BeautifulSoup(nextpagesource, "lxml")
    section = soup.find('section', class_='componentsListingLargeRow componentsListingLargeRow--withGrid1N componentsListingLargeRow--withMobileBig component')
    articles = section.find_all('div',class_='atomsListingArticleTileWithSeparatedLink atomsListingArticleTileWithSeparatedLink--withGrid component')
    article = soup.find_all('a', class_='atomsListingArticleTileWithSeparatedLink__titleLink')
    art_count = 0

    # define the string we are looking for in the articles
    words_wyciek = re.sub(r'(u dany|dan|owi dany)\b', '', 'wyciek')
    words_hak = re.sub(r'(owa|er)', '', 'hak')
    words_cyfr = re.sub(r'yzow|yzac|ow', '', 'cyfr')
    pattern = re.compile(f'cyber | {words_hak} | {words_wyciek} | {words_cyfr}', flags=re.X | re.I)

    # loop through articles
    for article in article:
        art_count +=1
        link = article['href']
        arturl = f'{pagesrc}{link}'
        artsource = requests.get(f'https://dziennikbaltycki.pl/strefa-biznesu/z-regionu{link}').text
        artsoup = BeautifulSoup(artsource, 'lxml')
        artText = artsoup.findAll('p', class_=None)
        artHead = artsoup.find('h1').text
        if artHead == 'Biznes w regionie':
            pass
        else:
            # search through the paragraphs of the article and counting occurrences
            # concatenate paragraphs of the article
            par_text = [par.text for par in artText]
            all_par = '-'.join(par_text)
            matchesno = len(pattern.findall(all_par))

            # write down the articles with more than 2 occurrences of the words
            if matchesno > 2:
                print(artHead + ': ' + str(matchesno) + ' wynikow')
                writer.writerow([artHead, matchesno, arturl])

# write down how many articles have been searched
writer.writerow(['Searched through ' + str(art_count) + ' articles'])