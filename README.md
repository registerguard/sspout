Python project to do the following:

* Loop over DT photo gallery stories (web.gal-) and grab metadata (including SSP id)
* Go grab metadata from SSP API
* Go grab images from SSP
* Package each story up into folder with XML and images for NCS importing

## Preliminary research

Gallery subcats: `32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756`
Video subcats: `31994433,32058759,32058196,32003307,32058816,32042463,32042459,32058748,31994425,32058825,32042583,32042464,32058820,32058774,32042460,32003311,32058826,32058162`


There are between 337 and 360 stories slotted with the gallery subcategories. I would guess 337 is the "more" accurate value. The 360 number could include stories that are not "published" officially.

* 337 is the number returned by the [json API](http://registerguard.com/csp/cms/sites/rg/feeds/json.csp?items=400&subcats=32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756#)
* 360 is the number returned by a db query: `SELECT storyId FROM dbo.Story WHERE Story.subCategoryId in (32058824,32067956,32058769,32058823,32058773,32058730,32058735,32058827,32058745,31994432,32058749,32058736,32058195,32058817,32068003,32058784,32058756)`

*Side note: When you do the JSON query, there is an error returned.*