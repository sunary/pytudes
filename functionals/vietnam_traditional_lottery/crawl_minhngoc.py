# -*- coding: utf-8 -*-
__author__ = 'sunary'


import requests
import re
from datetime import datetime, timedelta


RANGE_DEFAULT = 30
MINHNGOC_URL = 'http://www.minhngoc.com.vn/getkqxs/'
LOCATION_DEFINE = {
    'mien-bac': {
        'url': 'mien-bac',
        'name': 'Miền Bắc'
    },
    'mien-trung': {
        'url': ['thua-thien-hue', 'quang-nam', 'da-nang', 'quang-tri', 'ninh-thuan', 'da-nang', 'kon-tum'],
        'name': ['Thừa Thiên Huế', 'Quảng Nam', 'Đà Nẵng', 'Quảng Trị', 'Ninh Thuận', 'Đà Nẵng', 'Kon Tum']
    },
    'mien-nam': {
        'url': '',
        'name': ''
    }
}


class CrawlMinhNgoc(object):

    def __init__(self):
        pass

    def crawl_lottery(self, location, crawl_date=None):
        res = requests.get(self.location_url(crawl_date=crawl_date, location=location)).text
        if 'giai1' not in res:
            return

        giai_title = ['giaidb', 'giai1', 'giai2', 'giai3', 'giai4', 'giai5', 'giai6', 'giai7', 'giai8']
        lottery_result = []
        for g in giai_title:
            match = re.search('<td\sclass="{0}">([^<]+)</td>'.format(g), res)
            if match:
                row = match.group(1).strip().replace(' ', '').split('-')
                row = [str(r) for r in row]

                lottery_result.append(row)

        return lottery_result

    def last_2_digits(self, lottery_result):
        two_digits = []
        for row in lottery_result:
            for elem in row:
                two_digits.append(elem[-2:])

        return two_digits

    def range_available_data(self, location, length_expected=RANGE_DEFAULT):
        start_date = datetime.utcnow()

        if requests.get(self.location_url(location, start_date), allow_redirects=False).status_code == 302:
            start_date -= timedelta(days=1)

        today = start_date
        crawl_dates = []
        for i in range(length_expected):
            crawl_dates.append(start_date)
            start_date -= timedelta(days=1)

        return crawl_dates, today

    def location_url(self, location, crawl_date=None):
        url = LOCATION_DEFINE[location]['url']
        url = url[crawl_date.weekday()] if isinstance(url, list) else url

        return MINHNGOC_URL + '{}/{}.js'.format(url, crawl_date.strftime('%d-%m-%Y'))

    def location_name(self, location, crawl_date):
        name = LOCATION_DEFINE[location]['name']
        return name[crawl_date.weekday()] if isinstance(name, list) else name

    def serialize(self, lottery_result):
        str_data = []
        for row in lottery_result:
            str_data.append(','.join(row))

        return ';'.join(str_data)

    def deserialize(self, str_data):
        lottery_result = str_data.split(';')
        for i in range(len(lottery_result)):
            lottery_result[i] = lottery_result[i].split(',')

        return lottery_result


if __name__ == '__main__':
    crawler = CrawlMinhNgoc()
    rs = crawler.crawl_lottery('mien-bac', datetime(2018, 9, 22))
    if rs:
        print(rs)
        print crawler.last_2_digits(rs)
