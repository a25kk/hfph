This is a tool which is used to create references within plone.
It is not specially refined. 

I've only tested this with Plone 2.1.1

Installation
--------------
Install using quick installer

Assumptions/Background
-------------------------
The typical use case for ReferenceMaker assumes that you have or know the id of all the items (target and source) and they already exist in your plone site. For example, you may have a collection of 'events' that must be associated with corresponding 'images', both already present in the site.

To achieve the 'association' or 'reference' as it is called in the Plone world, you create a simple comma separated text file. The file format is outlined below. If you have trouble, it's most likely related to a poor understanding of how the file format relates to the referencing mechanism. The file format is discussed in more detail later on in this document.


Usage
--------
Create a referencemaker in your plone instance and then 

Known Issues

    * I have had issues getting it to behave properly with PloneQueueCatalog installed, this may simply have been due to inexperience with PloneQueueCatalog.
    * Plone does not enforce unique Ids since objects can be further distinguished by their absolute path. 
It is possible to specify a source_path and a target_path as csv fields,
the paths must be the same as they appear in the path properties od portal_catalog objects (e.g. /Plone/item1)
  

Usage
----------

Preparation

Preparation may involve adding the relevant content (events and images in this case) to the portal.

You can make your life easier if you have/know the following:

    * The source type -- this refers to the type that "reaches out" and does the referencing. A reference maker can only use a single content type as a 'source type' our source type would be an 'event'.
    * The source ids -- The ids of the objects that will be doing the "reaching out"
    * The target ids -- The ids of the objects that will be referenced.

The source ids and target ids could be arranged in a table (the id is the name that Plone uses to call an object)::

 source ids 	target ids
 turn_on_computer 	feeling_good_picture.jpg
 program_crashes 	not_so_good_picture.jpg

1. Add a Referencemaker instance to your site.
2. Give it a 'title' then click 'next'
3. Choose a portal_type. for our example we choose 'ATContentTypes?.ATEvent?' (that's the "Zope name" for an event) from the dropdown menu provided then click 'next'
4. Choose a csv file or put the csv list in the textbox provided
5. Then map fields
6. Finally procede with the import

More information about the CSV File Format
---------------------------------------------
Most spreadsheet programs have the ability to create the comma separated (csv) file format. If you are creating it by hand the file must be formated as follows (note the first row which contains the names 'source_id' and 'target_id')::

 source_id,target_id
 turn_on_computer,feeling_good_picture.jpg
 program_crashes,not_so_good_picture.jpg
 ctrl_alt_del_not_responding,upset_picture.jpg
 blue_screen,reallymadpicture.jpg

Important!!! That first row is used as a label it is NOT dummy data it MUST be there. The data starts in the second row.

'source_id' means the item that will reference the other item, in our example above it would be the 'events'

So a 'target_id' (an image) is referenced by a 'source_id' (an event)



