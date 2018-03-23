import requests, json, csv, os, shutil
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from scripts import *

cwd = os.getcwd()
pacific = timezone('America/Los_Angeles')
videoSubcats = "31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162"
items = 999
startDate = pacific.localize(datetime(2018,1,1,0,0,1))
endDate = pacific.localize(datetime(2018,2,28,11,59,59))

def writeVideoXML(stories):
    for story in stories:
        # Do some string cleaning for YouTube ID
        vid = story['video']
        vidTest = False
        if (re.search('youtube\.com',vid)):
            vid = vid.split('=')[1]
            vidTest = True
        elif (re.search('youtu\.be',vid)):
            vid = vid.split('/')[3]
            vidTest = True
        if (vidTest == True):
            # Do date checking
            dt = getDatetime(story['published'])
            if (startDate <= dt <= endDate):
                print("Getting {0}: {1}".format(story['headline'],story['path']))
                article = etree.Element('article')
                # article story metadata
                uniqueid = etree.SubElement(article,'uniqueid')
                uniqueid.text = story['id']
                title = etree.SubElement(article,'title')
                title.text = etree.CDATA(story['headline'])
                date = etree.SubElement(article,'date')
                date.text = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
                # Create folder structure
                dtDIR = dt.strftime('%Y/%m/%d')
                filePath = '{0}/video/{1}/'.format(cwd, dtDIR)
                createFolders(filePath)
                # Come back to XML
                category = etree.SubElement(article,'category')
                category.text = story['section']
                byline = etree.SubElement(article, 'byline')
                byline.text = story['byline']
                taxonomy = etree.SubElement(article,'taxonomy')
                taxonomy.text = story['catid']
                video = etree.SubElement(article,'videoID')
                video.text = vid
                seo = etree.SubElement(article,'seo-label')
                seoRegex = r'http://registerguard.com(\/.*\.html.csp)'
                seo.text = re.search(seoRegex,story['path'])[1]
                # Move into exporting to file
                # print(etree.tostring(article, pretty_print=True))
                out = etree.ElementTree(article)
                outFILE = '{0}/{1}-{2}.xml'.format(filePath, dt.strftime('%Y%m%d'), story['id'])
                out.write(outFILE, pretty_print=True, xml_declaration=True, encoding='utf-8')

def main():
    stories = getStories(videoSubcats, items)
    writeVideoXML(stories)

    # Write those stories to a CSV (stories var, name of output csv)
    #storyCSV(stories,'video2.csv')

main()