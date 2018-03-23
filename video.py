import requests, json, csv, os, shutil
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone
from scripts import *

cwd = os.getcwd()
pacific = timezone('America/Los_Angeles')
videoSubcats = "31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162"
items = 750

def main():
    stories = getStories(videoSubcats, items)
    #writeVideoXML(stories)

    # Write those stories to a CSV (stories var, name of output csv)
    storyCSV(stories,'video.csv')

main()