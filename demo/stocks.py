from bs4 import BeautifulSoup
import time
import urllib3


def get_soup_from_local_file(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, features="lxml")
    return soup


def get_cbk_dollar_rate():
    soup = get_soup_from_local_file("cbk.html");
    trs = soup.select('tr')
    dollar_tr = list(filter(
        lambda x: x.__repr__().find('tg-4eph') > 0
        and x.get_text().lower().find('dollar') > 0, trs))[0]
    return float(dollar_tr.select('td')[1].get_text())


def get_commodities_prices_from_nse():
    soup = get_soup_from_local_file("nse.html")
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
    a = get_commodities_prices_from_nse()
    return list(filter(lambda x: x[0] in searches, a))


def format_commodities(commodities):
    for a in commodities:
        log = 'P {} {} Ksh {:.2f}'.format(
                time.strftime("%Y/%m/%d %H:%M:%S"), a[0], a[1]) 
        yield log


def format_dollar(amount):
    return 'P {} {} Ksh {:.2f}'.format(
                time.strftime("%Y/%m/%d %H:%M:%S"), '$', amount)


def out_to_console():
    dollar_conv = format_dollar(get_cbk_dollar_rate())
    print(dollar_conv)
    commodities = format_commodities(
            get_select_commodities(['SCOM', 'CIC', 'UMME']))
    for i in commodities:
        print(i)


out_to_console()
