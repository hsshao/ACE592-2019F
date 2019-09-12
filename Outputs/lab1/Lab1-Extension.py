import requests
from lxml import html
from urllib.parse import urljoin
import re

Results = []


def scrape(pageURL, num=0):

    resp = requests.get(url=pageURL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    })

    tree = html.fromstring(html=resp.text)
    Agents = tree.xpath("//div[@class='block__data']")

    for Agent in Agents:
        a = {
            'Name': Agent.xpath(".//h4[@class='titolo text-primary']/a/text()")[0],
            'Address': Agent.xpath(".//p/text()")[0].strip(),
        }
        Results.append(a)

    next_page = tree.xpath("//ul[@class='pull-right pagination']/li[1]/a/@href")

    num += 1

    if num >= 10000:
        return

    if len(next_page) != 0:
        scrape(pageURL=urljoin(base=pageURL, url=next_page[0]), num=num)
    else:
        return


scrape(pageURL='https://www.immobiliare.it/agenzie-immobiliari/roma-provincia/')
print(Results)

with open('results.txt', 'w') as the_file:
    the_file.write('Name, Address, Zip, City\n')
    for agent in Results:
        Name = agent.get('Name')
        AddAll = agent.get('Address')
        try:   
            Address = re.findall(r"(.*)(?:\s{4})", AddAll)[0].strip()
            Zip = re.findall(r"(\d{3,})", AddAll)[0].strip()
            City = re.findall(r"([^\s]*$)", AddAll)[0].strip()
        except IndexError:
            continue
        the_file.write(Name + ', ' + Address + ', ' + Zip + ', ' + City + '\n')
