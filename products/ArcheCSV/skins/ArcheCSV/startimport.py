response=context.REQUEST.RESPONSE

import_type=context.getImport_type()
head=context.head
prefix=context.getPrefix()
csvdata=context.getCSVdata()

map_fields=list(context.getMap_fields())
package=import_type.split('.')[0]
import_type=import_type.split('.')[2]
at_fields= context.getArchFields()
at_mapping={}

response.setHeader('Content-type', 'text/html')
response.write('<font size=2>[%s]: Starting import...<br />' % str(DateTime().strftime('%H:%M.%S')))

response.write('Import type: %s<br />' % str(context.getImport_type()))

for i in range(len(head)):
    at_mapping[map_fields[i]]=head[i]
    print "assigning "+head[i]+'-->'+map_fields[i]
    
    
atdictionaries=[]
csvdata=csvdata[1:]
multivalsep = context.getMulti_valued_separator()

for i in range(len(csvdata)):
    atdict={}
    zipdict={}
    for f in at_fields:
        if at_mapping.has_key(f.getName()):
            k=at_mapping[f.getName()]
            if f.multiValued:
                atdict[f.getName()]=csvdata[i][k].split(multivalsep)
            else:
                atdict[f.getName()]=csvdata[i][k]
            zipdict[f.getName()] = context.getMap_zip_fields()[head.index(k)]

    if context.getMap_local_target():
        local_target = csvdata[i].get(head[int(context.getMap_local_target())])
    else:
        local_target = None
    atdictionaries.append( ( zipdict, local_target, atdict))
    
# this function ripped out of CMFPlone/FactoryTool.py
def generateId(self, type, loop=0):
    now = DateTime()
    name = type.replace(' ', '')+'.'+now.strftime('%Y-%m-%d')+'.'+now.strftime('%H%M%S')
    if loop:
        name='%s-%s' %(name,loop)
    
    # Reduce chances of an id collision (there is a very small chance that somebody will
    # create another object during this loop)
    base_name = name
    objectIds = self.getParentNode().objectIds()
    i = 1
    while name in objectIds:
        name = base_name + "-" + str(i)
        i = i + 1
    return name
    

counter=0
total=len(atdictionaries)
loop=0
operation = context.getOperation()

try:
    for zipdict, local_target, atd in atdictionaries:
        loop += 1
        if not atd.has_key('id'):
            atd['id']=generateId(context, prefix, loop)
        else:
            if not atd['id']:
                atd['id']=generateId(context, prefix, loop)
        #loop through each dictionary item to see if it has a :modifier
    
        if context.getImport_target() or context.getMap_local_target():
            target = context.getImport_target()
            if local_target:
                folder=context.restrictedTraverse(context.getImport_target() + '/'+ local_target)
            else:
                folder=context.restrictedTraverse(context.getImport_target())        
        else:
            folder=context.aq_parent
    
        parent = context.getParentNode()
    
        files = {}
    
        for key, value in zipdict.items():
            if value != 'None':
                response.write('Looking in zip %s to fill the field %s<br />' % (value, key))
                response.write('Uploading image %s to field %s<br />' % (atd[key], key))
                if files.has_key(value):
                    file = files[value]
                else:
                    if value in parent.objectIds():
                        file = parent[value].getFile()
                        files[value]=file
                    else:
                        response.write('Stopping because zip file %s not found in %s<br />' % (value, parent.absolute_url()))
                        return
                image = context.get_file_from_zip(file, atd[key])
                if image:
                    atd[key]=image
                else:
                    del atd[key]
    
        content = getattr(folder, atd['id'], None)
        if content is None:
            if operation in ['add', 'add_and_update']:
                try:
                    folder.invokeFactory(import_type, **atd)
                    counter=counter+1
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Adding the content failed due to the following error: %s" % exception_info)
            elif operation == 'update':
                response.write("Content not found: %s<br />" % atd['id'])
                if context.getStop_import_when_content_not_found_on_update():
                    response.write("Stopping import because content to update was not found")
                    return
            else:
                raise "Unknown operation"
        else:
            if operation == 'add':
                if context.getStop_import_when_content_already_exists_on_add():
                    response.write("Stopping import because content to add alreay exists: %s<br />" % atd['id'])
                    return
            elif operation == 'add_and_update':
                pass
            elif operation == 'update':
                pass
            else:
                raise "Unknown operation"
            try:
                content.edit(**atd)
                counter=counter+1
            except:
                exception_info = context.HTMLFormatExceptionInfo()
                response.write("Editing the content failed due to the following error: %s" % exception_info)

        #workflow:
        #wfcontext=context.portal_workflow.doActionFor(context[id],
        #                                                    'publish',
        #                                                    comment='importazione iniziale')
    
        perc=float(counter)/float(total)*100
    
        response.write('Processing: %s<br />with dict:%s<br />' % (atd['id'],str(atd)))
        response.write('[progress:%i out of %i (%.2f %%)]<br />' % (counter,total,perc))
        
    response.write('[%s]: Done!' % str(DateTime().strftime('%H:%M.%S')))

except:
    exception_info = context.HTMLFormatExceptionInfo()
    response.write("An error has occured: %s" % exception_info)
    raise

return
