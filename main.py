import requests, json, csv, os, shutil
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime

cwd = os.getcwd()

def getStories(subcats,items=10):
    # raw_input for items ???
    payload = {'subcats': subcats, 'items': items}
    url = 'http://registerguard.com/csp/cms/sites/rg/feeds/json.csp'
    r = requests.get(url, params=payload)
    json = r.json()
    #hits = json['hits']
    stories = json['stories']
    return stories

def getAlbum(sspalbum):
    # raw_input for items ???
    payload = {'id': sspalbum}
    url = 'http://slideshow.registerguard.com/slideshowpro/api/ncs/index.php'
    r = requests.get(url, params=payload)
    album = r.json()
    return album

def storyCSV(stories,csvname='stories.csv'):
    # Error checking for csv extension???
    print("Writing {0}...".format(csvname))
    with open(csvname,'w',newline='') as csvfile:
        fieldnames = ['headline','url','author','pubdate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for story in stories:
            writer.writerow({'headline': story['headline'], 'url': story['path'], 'author': story['byline'], 'pubdate': story['published']})
            #print(story['headline'])
    print("{0} has been written.".format(csvname))

def createFolders(dateDIR):
    if (os.path.isdir('{0}/{1}'.format(cwd, dateDIR)) == False):
        os.makedirs('{0}/{1}'.format(cwd, dateDIR))

def getImage(url,dateDIR):
    filename = url.split('/')[-1]
    path = '{0}/{1}/{2}'.format(cwd, dateDIR, filename)
    rimg = requests.get(url, stream=True, verify=False)
    if (rimg.status_code == 200):
        with open(path, 'wb') as f:
            rimg.raw.decode_content = True
            shutil.copyfileobj(rimg.raw, f)

def writeXML(stories,xmlname='out.xml'):
    ### Write XML
    for story in stories:
        gallery = etree.Element('gallery')
        # Gallery story metadata
        uniqueid = etree.SubElement(gallery,'uniqueid')
        uniqueid.text = story['id']
        title = etree.SubElement(gallery,'title')
        title.text = etree.CDATA(story['headline'])
        date = etree.SubElement(gallery,'date')
        # Do smart date stuff
        dateTEMP = story['published']
        dateTEMP = datetime.strptime(dateTEMP, '%Y-%m-%d %H:%M:%S')
        date.text = dateTEMP.strftime('%Y-%m-%dT%H:%M:%S')
        # Create folder structure
        dateDIR = dateTEMP.strftime('%Y/%m/%d')
        createFolders(dateDIR)
        # Come back to XML
        category = etree.SubElement(gallery,'category')
        category.text = story['section']
        taxonomy = etree.SubElement(gallery,'taxonomy')
        taxonomy.text = story['catid']
        description = etree.SubElement(gallery,'description')
        description.text = etree.CDATA(story['excerpt'])
        # Move into images
        album = getAlbum(story['sspid'])
        #print(story['sspid'])
        images = etree.SubElement(gallery, 'images')
        for pic in album:
            image = etree.SubElement(images, 'image')
            title = etree.SubElement(image,'title')
            title.text = etree.CDATA(pic['id'])
            # Make sure caption is clean
            caption = etree.SubElement(image,'caption')
            captionTEMP = pic['description']
            captionTEMP = captionTEMP.replace('\n','').replace('\r','').replace('\t','')
            caption.text = etree.CDATA(captionTEMP)
            # Make sure credit is clean
            credit = etree.SubElement(image,'credit')
            creditTEMP = pic['byline']
            creditTEMP = creditTEMP.replace('\n','').replace('\r','').replace('\t','')
            credit.text = etree.CDATA(pic['byline'])
            filename = etree.SubElement(image,'filename')
            filename.text = etree.CDATA(pic['filename'])
            getImage(pic['original'], dateDIR)
            # print(etree.tostring(images, pretty_print=True))
        # Move into exporting to file
        # print(etree.tostring(gallery, pretty_print=True))
        out = etree.ElementTree(gallery)
        outFILE = '{0}/{1}/{2}'.format(cwd,dateDIR, xmlname)
        out.write(outFILE, pretty_print=True, xml_declaration=True, encoding='utf-8')

# DT API variables
photoSubcats = "32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756"
videoSubcats = "31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162"
items = 350

# Get stories from DT API (subcat id list, number to return)
stories = getStories(photoSubcats,1)
#print(stories)

# Write those stories to a CSV (stories var, name of output csv)
#storyCSV(stories,'test.csv')

# SSP API variables
#sspalbum = 404
#album = getAlbum(sspalbum)

# Write out to XML
writeXML(stories, 'test.xml')




