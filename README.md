Python project to do the following:

* [x] Loop over DT photo gallery stories (web.gal-) and grab metadata (including SSP id)
* [x] Go grab metadata from SSP API
* [x] Figure out date folder structure
* [x] Go grab images from SSP
* [x] Package each story up into folder with XML and images for NCS importing
* [ ] Smart dates (timezone)
  * See: https://bitbucket.org/registerguard/turin/src/ebf92578ab06b9219ac1555cfa286bbd8cc7292e/scripts/export_saxotech.py?at=xml_export&fileviewer=file-view-default#export_saxotech.py-60

## Preliminary research

Gallery subcats: `32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756`
Video subcats: `31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162`


There are between 337 and 360 stories slotted with the gallery subcategories. I would guess 337 is the "more" accurate value. The 360 number could include stories that are not "published" officially.

* 337 is the number returned by the [json API](http://registerguard.com/csp/cms/sites/rg/feeds/json.csp?items=400&subcats=32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756#)
* 360 is the number returned by a db query: `SELECT storyId FROM dbo.Story WHERE Story.subCategoryId in (32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756)`

*Side note: When you do the JSON query, there is an error returned.*

Wrote out first CSV file on 3/14. 

Story data structure from DT API looks like this (clean and raw):

* byline
* category
* cat id
* count (total stories returned)
* deck
* headline
* path (full URL)
* publish date (YYYY-MM-DD HH:MM:SS)
* server (???)
* author
* excerpt
* sspid
* image (DT 990 file)

```
[{'byline': 'The Register-Guard Staff', 'category': 'Sports', 'catid': '32058784', 'count': 1, 'deck': 'From Willamette High to the NCAA Tournament, half a decadeof Lexi Bando in pictures', 'headline': 'The Bando bandwagon', 'path': 'http://registerguard.com/rg/photo/36550000-321/the-bando-bandwagon.html.csp', 'published':'2018-03-14 14:30:01', 'server': '', 'author': 'The Register-Guard Staff', 'excerpt': '', 'sspid': '679', 'image': 'http://registerguard.com/csp/cms/sites/dt.common.streams.StreamServer.cls?STREAMOID=I6uQtLL7vX76Kmq_8xB8Y8$daE2N3K4ZzOUsqbU5sYuSguc0JOxw0CVWS_uWjGHFWCsjLu883Ygn4B49Lvm9bPe2QeMKQdVeZmXF$9l$4uCZ8QDXhaHEp3rvzXRJFdy0KqPHLoMevcTLo3h8xh70Y6N_U_CryOsw6FTOdKL_jpQ-&amp;CONTENTTYPE=image/jpeg'}]
```

Example gallery field mapping for NCS
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<gallery>
	<uniqueid></uniqueid>
	<title><![CDATA[]]></title>
	<date></date>
    <category>PHOTOGALLERY</category>
	<taxonomies></taxonomies>
	<description>GALLERY CAPTION</description>
	<images>
        <image>
            <title><![CDATA[]]></title>
            <caption><![CDATA[]]></caption>
            <credit><![CDATA[]]></credit>
            <filename></filename>
        </image>
	</images>
	<seo-label></seo-label>
</gallery>
```

Data coming out of [SSP API](http://slideshow.registerguard.com/slideshowpro/api/ncs/index.php?id=404):

* image (990)
* thumb (150)
* byline (name only)
* description (caption)
* id (unique ssp id)
* filename (original filename)
* original (original image file)


This worked to download image:

```python
r = requests.get(url, stream=True, verify=False)
path = '/Users/rdenton/Desktop/test.jpg'
if r.status_code = 200:
	with open(path, 'wb') as f:
	    r.raw.decode_content = True
	    shutil.copyfileobj(r.raw,f)
```