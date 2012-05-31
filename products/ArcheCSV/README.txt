ArcheCSV 2.0

(c) Lorenzo Musizza
1000 ASA s.r.l.
http://www.1000asa.com
contact: lorenzo.musizza at 1000asa.com
License terms in LICENSE.GPL
--
20070415
CREDITS: Thanks to Maik Ršder for adding nice new features, like zip files handling!

FEATURES ADDED:
- zip file batch content adding:

It is now possible to batch-add photos (or other content) in a .zip file: upload a zip file containing images in Plone as an ATFile, then use a csv file to map image filenames, e.g.
"title","image"
"Image wedding 1","img1.jpg"
"Image wedding 2","img2.jpg"

(check out the examples in ArcheCSV/example)

- member adding (see instructions below)
- References adding (incorporated RefMaker and improved it)

BUGFIX:
using meta_type to correctly identify ATContentTypes content

20051216
ArcheCSV allows to batch import content and members into a Plone Site using
a .csv file. In the case of content types, the .csv fields are mapped to the
corresponding Archetypes fields. In the case of a member import the .csv fields
are mapped to memberdata properties.

Patches and suggesion are welcome!

REQUIREMENTS:
tested on Plone 2.5.2 

Usage instructions for content import:

1) create an "importer" instance inside the folder that will contain the batch-created objects
2) follow the step based wizard (schematas):
   - give a title to the importer (you may have multiple importers around)
   - choose the portal type of the objects you want to import
   - upload/paste a csv formatted file.
     The headers should be present, but can be optionally be omitted. 
     The startimport Python Script is used for importing unless you specify your own.
     The import target path can be specified, for example Plone/myfolder/anotherfolder
   - map csv fields to AT fields, if you don't want to use a particular csv field choose "Not used";
     if you get an error in this step it is most likely that the csv file previously uploaded is not valid.
     Here you can also choose a prefix to use for the imported objects.
   - start the batch import and examine log for details
3) check out the imported objects

Usage instructions for member import:

1) create a "memberimporter" instance inside any folder
2) follow the step based wizard (schematas):
   - give a title to the importer (you may have multiple importers around)
   - choose the portal type of the objects you want to import
   - upload/paste a csv formatted file *headers must be present* (see example/sample_csv)
   - map csv fields to AT fields, if you don't want to use a particular csv field choose "Not used";
     if you get an error in this step it is most likely that the csv file previously uploaded is not valid.
     Here you can also choose a prefix to use for the imported objects.
   - start the batch import and examine log for details
3) check out the imported objects

To test it out it is possible to use the Sample_AT and sample_csv provided in example folder.
To use Sample_AT it must be copied on the product folder and must be included in init.py.

See screenshot in doc folder.

If you are interested in extending this product please contact me.