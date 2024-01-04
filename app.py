import csv

from parse import Parser


def save_to_csv(data, newline=""):
    with open('parse.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)


if __name__ == '__main__':
    parser = Parser()
    parser.get_page('https://yandex.kz/pogoda/month?lat=43.273564&lon=76.914851&via=hnav')
    data = parser.parse()
    save_to_csv(data)
