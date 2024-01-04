import re
from os import environ

from bs4 import BeautifulSoup
from selenium import webdriver


class Parser:
    def __init__(self):
        path = environ.get('path')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"webdriver.chrome.driver={path}")
        self.browser = webdriver.Chrome(options=chrome_options)

    def get_page(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(2)

    def close(self):
        self.browser.close()
        self.browser.quit()

    def __str_to_date(self, date):
        months = {
            'января': 'January',
            'февраля': 'February',
            'марта': 'March',
            'апреля': 'April',
            'мая': 'May',
            'июня': 'June',
            'июля': 'July',
            'августа': 'August',
            'сентября': 'September',
            'октября': 'October',
            'ноября': 'November',
            'декабря': 'December',
        }
        day, month = date.split()
        month = months[month]
        return f'{day} {month} 2024'


    def parse(self):
        data = [['date', 'day_of_week', 'day_temperature',
                 'night_temperature', 'weather', 'feels_like', 'pressure', 'humidity',
                 'wind', 'wind_direction', 'day_climatic_temperature', 'night_climatic_temperature']]
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        days = soup.find_all(attrs={'class': 'climate-calendar__cell'})[7:]
        for day in days:
            if not 'climate-calendar-day' in day.a.div.get("class"):
                break
            components = re.split('[;,\.]', day.find('span', attrs={'class': 'a11y-hidden'}).getText())

            date =self.__str_to_date(components[0].strip())
            day_of_week = components[1].strip()
            day_temperature = int(components[3].strip()[:-1])
            night_temperature = int(components[5].strip()[:-1])
            weather = components[6].strip()
            feels_like = int(day.find('div', {'class': "climate-calendar-day__detailed-feels-like"}).div.getText().replace("−", "-"))
            info = day.find_all('td', {'class': "climate-calendar-day__detailed-data-table-cell_value_yes"})
            pressure = int(info[0].getText()[:-11])
            humidity = int(info[1].getText()[:-1])
            airflow = info[2].getText().split('м/с')
            wind = float(airflow[0].strip())
            wind_direction = airflow[1].strip()
            day_climatic_temperature = None
            night_climatic_temperature = None

            try:
                day_climatic_temperature = int(day.find('div', {
                    'class': "temp climate-calendar-day__detailed-climate-temp-day"}).getText().strip().replace("−", "-"))

                night_climatic_temperature = int(day.find('div', {
                    'class': "temp climate-calendar-day__detailed-climate-temp-night"}).getText().strip().replace("−", "-"))
            except AttributeError:
                pass

            data.append([date, day_of_week, day_temperature,night_temperature, weather, feels_like, pressure,
                         humidity, wind, wind_direction,day_climatic_temperature,night_climatic_temperature])
        self.close()
        return data
