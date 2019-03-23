from bs4 import BeautifulSoup
import time
import urllib3


def get_commodities_prices():
    with open("nse.html") as fp:
        soup = BeautifulSoup(fp, features="lxml")

    pricebar = soup.select('div #mycrawler')[0]
    commodities = []
    prices = []
    for index, span in enumerate(pricebar.find_all('span')):
        pos = index % 3
        if (pos == 0):
            commodities.append(span.text.strip())
        elif (pos == 1):
            prices.append(float(span.text.split()[-1]))
    return list(zip(commodities, prices))


def get_select_commodities(searches):
    a = get_commodities_prices()
    return list(filter(lambda x: x[0] in searches, a))


def format_commodities(commodities):
    for a in commodities:
        log = 'P {} {} Ksh {:.2f}'.format(
                time.strftime("%Y/%m/%d %H:%M:%S"), a[0], a[1]) 
        print(log)


format_commodities(get_select_commodities(['SCOM', 'CIC', 'UMME']))
