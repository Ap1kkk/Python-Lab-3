import socket
import statistics

from pythonping import ping
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


def get_ip(site_url):
    try:
        python_ip = socket.gethostbyname(site_url)
        return python_ip
    except socket.error as err:
        print(f"Error: {err}")
        return None


def ping_website(site_url):
    try:
        response = ping(site_url, size=4, count=11)
        rtt_times = [resp.time_elapsed_ms for resp in response]
        stddev_rtt = statistics.stdev(rtt_times)
        return stddev_rtt, rtt_times
    except Exception as err:
        print(f"Error: {err}")
        return None, None


def print_RTT(rtt_times):
    plt.hist(rtt_times, bins='auto', density=True)
    plt.xlabel('RTT (ms)')
    plt.ylabel('Плотность вероятности')
    plt.title('Распределение RTT')
    plt.grid(True)
    plt.show()


def get_exchange_rate(site_url):
    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    aud_element = soup.find('a', {'title': 'Австралийский доллар'})

    exchange_rate = aud_element.find_all('div')
    code = exchange_rate[0].text.strip()
    denomination = exchange_rate[1].text.strip()
    currency = exchange_rate[2].text.strip()
    value = exchange_rate[3].text.strip()
    change = exchange_rate[4].text.strip()
    percent = exchange_rate[5].text.strip()

    return code, denomination, currency, value, change, percent


url_to_ping = "www.python.org"
url_to_parse = "https://finance.rambler.ru/currencies/"

ip = get_ip(url_to_ping)
print(f"The IP address of {url_to_ping} is {ip}")

stddevRRT, timesRTT = ping_website(url_to_ping)
print(f"Среднее квадратичное отклонение RTT = {stddevRRT}")

print_RTT(timesRTT)


values = get_exchange_rate(url_to_parse)
print(f"\nКод: {values[0]}")
print(f"Номинал: {values[1]}")
print(f"Валюта: {values[2]}")
print(f"Курс ЦБ: {values[3]}")
print(f"Изменение: {values[4]}")
print(f"%: {values[5]}")
