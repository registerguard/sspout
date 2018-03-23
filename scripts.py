import json, csv, requests, os, shutil, re
from datetime import datetime
from pytz import timezone

def getStories(subcats,items=10):
    # raw_input for items ???
    payload = {'items': items, 'subcats': subcats}
    url = 'http://registerguard.com/csp/cms/sites/rg/feeds/json.csp'
    try:
        r = requests.get(url, params=payload)
        print("got {}".format(r.url))
    except:
        print('bad request: {0}?items={1}&subcats={2}'.format(url, items, subcats))
    try:
        json = r.json()
        print("got json")
    except:
        print('bad json: {0}?items={1}&subcats={2}'.format(url, items, subcats))
    #hits = json['hits']
    stories = json['stories']
    return stories

def storyCSV(stories,csvname='stories.csv'):
    # Error checking for csv extension???
    print("Writing {0}...".format(csvname))
    with open(csvname,'w',newline='') as csvfile:
        fieldnames = ['headline','url','author','pubdate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for story in stories:
            writer.writerow({'headline': story['headline'], 'url': story['path'], 'author': story['byline'], 'pubdate': story['published']})
            # print(story['headline'])
        """
        fieldnames = ['headline','url','author','pubdate','video']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for story in stories:
            vid = story['video']
            vidRegex = r"youtube\.com|youtu\.be"
            vidTest = re.search(vidRegex,vid)
            if (vidTest):
                writer.writerow({'headline': story['headline'], 'url': story['path'], 'author': story['byline'], 'pubdate': story['published'], 'video': story['video']})
                # print(story['headline'])
        """
    print("{0} has been written.".format(csvname))

def createFolders(filePath):
    if (os.path.isdir('{0}'.format(filePath)) == False):
        os.makedirs('{0}'.format(filePath))

def getDatetime(dateString):
    # Return datetime object
    dateTEMP = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    pacific = timezone('America/Los_Angeles')
    dateTEMP = pacific.localize(dateTEMP)
    return dateTEMP