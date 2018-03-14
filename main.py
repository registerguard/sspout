import requests, lxml, json, csv
from bs4 import BeautifulSoup

photoSubcats = "32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756"
videoSubcats = "31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162"
items = 350
payload = {'subcats': photoSubcats, 'items': items}
url = 'http://registerguard.com/csp/cms/sites/rg/feeds/json.csp'
r = requests.get(url, params=payload)

#print(r.status_code)


json = r.json()
stories = json['stories']

with open('photogalleries.csv','w',newline='') as csvfile:
    fieldnames = ['headline','url','author','pubdate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for story in stories:
        writer.writerow({'headline': story['headline'], 'url': story['path'], 'author': story['author'], 'pubdate': story['published']})
        #print(story['headline'])

