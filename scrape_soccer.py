from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time, re, csv, codecs

RE_REMOVE_HTML = re.compile('<.+?>')


SLEEP_SECONDS = 1

fields = ['name', 'pos', 'MP', 'Pri', 'GS', 'Ass', 'CS', 'GC',
    'PM', 'PE', 'PC', 'PS', 'YC', 'RC', 'Sav', 'RB', 'MDP', 'PTS']


XPATH_MAP = {
    'name': "td[1]/a",
    'pos': "td[3]",
    'MP': "td[4]",
    'Pri': "td[5]",
    'GS': "td[6]",
    'Ass': "td[7]",
    'CS': "td[8]",
    'GC': "td[9]",
    'PM': "td[10]",
    'PE': "td[11]",
    'PC': "td[12]",
    'PS': "td[13]",
    'YC': "td[14]",
    'RC': "td[15]",
    'Sav': "td[16]",
    'RB': "td[17]",
    'MDP': "td[18]",
    'PTS': "td[19]",
}

"MP: Minutes Played"
"Pri: Price"
"GS: Goals Scored"
"Ass: Assist"
"CS: Clean Sheets"
"GC: Goals Conceded"
"PM: Penalties Missed"
"PE: Penalties Earned"
"PC: Penalties Conceded"
"PS: Penalties Saved"
"YC: Yellow Cards"
"RC: Red Cards"
"Sav: Saves"
"RB: Recovered Balls"
"MDP: Matchday Points"
"PTS: Points"

stats = []

def process_stats_row(stat_row):
    stats_item = {}
    for col_name, xpath in XPATH_MAP.items():
        
        stats_item[col_name] = RE_REMOVE_HTML.sub('', stat_row.find_element_by_xpath(xpath).get_attribute('innerHTML'))
        stats_item[col_name] = stats_item[col_name].encode('utf-8')
    #print stats_item
    return stats_item

def process_page(driver, page):
    print 'Getting stats...'

    print page

    rows = driver.find_elements_by_xpath("//div[contains(concat(' ',normalize-space(@id),' '),' statisticstable1_wrapper ')]/table/tbody/tr")


    stats = []
    for row in rows:
        
        stats_item = process_stats_row(row)
        stats.append(stats_item)

    print 'Sleeping for', SLEEP_SECONDS
    time.sleep(SLEEP_SECONDS)
    clickme = driver.find_element_by_xpath("//div[contains(concat(' ',normalize-space(@id),' '),' statisticstable1_paginate ')]/span[4]")
    clickme.click()
    
    return stats


def write_stats(stats, out):
    print 'Writing to file', out
    with open('stats.csv','w') as f:
        w = csv.DictWriter(f, delimiter=',', fieldnames=fields)
        w.writeheader()
        for row in stats:
            w.writerow(row)
            

def get_stats():
    
    fp = webdriver.FirefoxProfile()

    driver = webdriver.Firefox(firefox_profile=fp)
     
    time.sleep(SLEEP_SECONDS)

    stats = []

    driver.get('http://en.uclfantasy.uefa.com/UEFA/15813/clientplayerlist.do')

    for page in range(1, 6):
    
        page_stats = process_page(driver, page)
        stats.extend(page_stats)  

    write_stats(stats, 'stats.csv')

    driver.close()

if __name__ == '__main__':
    get_stats()

