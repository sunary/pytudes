__author__ = 'sunary'


from collections import Counter
from crawl_minhngoc import CrawlMinhNgoc


def statistics_2_digits(lottery_n_days):
    count_appear = []
    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        count_appear.append([i, [0]])

    for lo in count_appear:
        i = 0
        for kq in lottery_n_days:
            if str(lo[0]) in str(kq):
                lo[1] += [0]
                i += 1
            lo[1][i] += 1

    most_disappears = [[lo[0], lo[1][0]] for lo in count_appear]
    most_disappears = sorted(most_disappears, key=lambda item: -item[1])

    most_appears = []
    lottery_n_days = ','.join(lottery_n_days)
    lottery_n_days = lottery_n_days.split(',')
    frequency = Counter(lottery_n_days)

    for i in range(100):
        i = str(i) if i > 9 else '0' + str(i)
        if not frequency.get(i):
            frequency[i] = 0

    for k, v in frequency.items():
        most_appears.append((k, v))

    most_appears = sorted(most_appears, key=lambda item: item[0])

    for i in range(len(most_appears)):
        most_appears[i] = list(most_appears[i])

    count_prefix = [0] * 10
    count_suffix = [0] * 10

    for k in lottery_n_days:
        if k and 0 <= int(k) <= 99:
            count_prefix[int(k[0])] += 1
            count_suffix[int(k[1])] += 1

    return most_disappears, most_appears, count_prefix, count_suffix


if __name__ == '__main__':
    location = 'mien-bac'
    two_digits_result = []

    crawler = CrawlMinhNgoc()
    range_date, today = crawler.range_available_data(location, 10)
    for d in range_date:
        lottery_result = crawler.crawl_lottery(location, d)
        if lottery_result:
            two_digits_result.append(','.join(crawler.last_2_digits(lottery_result)))

    print(statistics_2_digits(two_digits_result))
