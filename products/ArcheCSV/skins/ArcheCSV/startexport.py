## Script (Python) "startmemberexport"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=
##

response=context.REQUEST.RESPONSE

csv_header = []

multivalsep = context.getMulti_valued_separator()
logpropdict = context.getLog_property_dictionary()
export_type = context.getExport_type()
portal_type = export_type.split('.')[-1]
exported_content=[]

response.setHeader('Content-type', 'text/html')
response.write('<font size=2>[%s]: Starting export...<br />' % str(DateTime().strftime('%H:%M.%S')))

try:
    counter=0
    contentbrains = context.portal_catalog.searchResults(portal_type = portal_type)

    total=len(contentbrains)
    
    pm = context.portal_membership

    response.write('Processing %d content objects found in the portal catalog for portal_type "%s"<br />' % (total, portal_type))

    for contentbrain in contentbrains:
        content = None
        try:
            content = contentbrain.getObject()
        except:
            exception_info = context.HTMLFormatExceptionInfo()
            response.write("Getting the content by id failed due to the following error: %s" % exception_info)
        if content is None:
            if context.getStop_export_when_content_not_found():
                response.write('Stopping export because a content was not found: %d<br />' % brain.getId)
                return
            else:
                pass
        else:
            contentdict = {'id':content.getId(), 'title':content.Title()}

            # Build CSV header once for the first content
            if csv_header == []:
                csv_header = ['id','title']
                for field in content.Schema().fields():
                    if field.getName() in ['id','title']:
                        pass
                    else:
                        csv_header.append(field.getName())
            
            for field in content.Schema().fields():
                if field.getName() in ['id', 'title']:
                    continue
                handler_id = context.normalize_field(field) + '_export'
                try:
                    handler = getattr(context, handler_id)
                except AttributeError:
                    handler = context.defaultfield_export
                handler(content, field, contentdict)
            exported_content.append(contentdict)

            counter=counter+1
            
        perc=float(counter)/float(total)*100
        if logpropdict:
            response.write('Processing: id: %s, properties:%s<br />' % (contentdict['id'],str(contentdict)))
        else:
            response.write('Processing: id: %s<br />' % contentdict['id'])
        response.write('[progress:%i out of %i (%.2f %%)]<br />' % (counter,total,perc))
except:
    exception_info = context.HTMLFormatExceptionInfo()
    response.write("An error has occured: %s" % exception_info)
    raise

response.write('Writing .csv file')
context.createcsv(csv_header, exported_content)
response.write('[%s]: Done!' % str(DateTime().strftime('%H:%M.%S')))

return

