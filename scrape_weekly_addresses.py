import requests as req
from bs4 import BeautifulSoup as soup

baseUrl = 'https://www.whitehouse.gov'

weeklyUrl = baseUrl + '/briefing-room/weekly-address' # 'https://www.whitehouse.gov/briefing-room/weekly-address'
urls = [weeklyUrl] + [weeklyUrl + '?page=' + str(i) for i in range(1, 40)]

res = req.get(weeklyUrl)
prez = soup(res.content, 'lxml')
