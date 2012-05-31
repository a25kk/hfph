## Script (Python) "startimport"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=
##

response=context.REQUEST.RESPONSE


#head=context.head
#prefix=context.getPrefix()
csvdata=context.getCSVdata()
map_fields=context.getMap_fields()



#target_type=context.target_type
#target_type=context.target_type.split('.')[1]
at_mapping={}

response.setHeader('Content-type', 'text/html')
response.write('<font size=2>[%s]: Starting job...<br>' % str(DateTime().strftime('%H:%M.%S')))

try:



#skipping header
    atdictionaries=[]
    csvdata_final=csvdata[1:]
    
  
    
    counter=0
    total= len(csvdata_final)
    for i in range(total):
        s_id= csvdata_final[i]['source_id']
        t_id = csvdata_final[i]['target_id']

        counter=counter+1
        perc=float(counter)/float(total)*100
        
        if csvdata_final[i].has_key('source_path'):
      		sres=context.portal_catalog.searchResults(id=s_id,path=csvdata_final[i]['source_path'])
      	else:
      		sres=context.portal_catalog.searchResults(id=s_id)
      	
      	if csvdata_final[i].has_key('target_path'):	
       		tres=context.portal_catalog.searchResults(id=t_id,path=csvdata_final[i]['target_path'])
        else:
       		tres=context.portal_catalog.searchResults(id=t_id)
        
        #response.write('debug: %s' % (len(tres)))
        #response.write('debug: %s' % (context.portal_catalog.searchResults(id='07KD')))
        response.write('[progress:%i out of %i (%.2f %%)]' % (counter,total,perc))
        if len(sres)+len(tres)>1:

            sobj=sres[0].getObject()
            tobj=tres[0].getObject()
            sobj_uid=sobj.UID()
            tobj_uid=tobj.UID()
            response.write('should look for: %s and make a reference of kind %s to %s <br>' % ( s_id, map_fields,t_id))
            sobj.addReference(tobj_uid,relationship=map_fields)
            #lorty: take the first result, getObject, makereference

            response.write('added reference from %s(%s) to %s(%s) <br><br>' % (sobj.id,sobj_uid,tobj.id,tobj_uid))
        else:
            response.write('object not found for %s or %s <br><br>' % (s_id,t_id))


#     for i in range(len(csvdata)):
#         atdict={}
#         for f in at_fields:
#             try:
#                 k=at_mapping[f.getName()]
#                 atdict[f.getName()]=csvdata[i][k]
#             except(KeyError):
#                 pass
#         atdictionaries.append(atdict)




#     counter=0
#     total=len(atdictionaries)
#     for atd in atdictionaries:
# 
#        counter=counter+1
#        id=generateId(context, prefix)
#        context.invokeFactory(import_type,id, **atd)
# 
#        #workflow:
#        #wfcontext=context.portal_workflow.doActionFor(context[id],
#        #                                                    'publish',
#        #                                                    comment='importazione iniziale')
# 
#        perc=float(counter)/float(total)*100
#        response.write('[progress:%i out of %i (%.2f %%)] imported: %s<br>with dict:%s<br><br>' % (counter,total,perc,id,str(atd)))
#     
#     response.write('[%s]: Done!' % str(DateTime().strftime('%H:%M.%S')))

except Exception, val:
    response.write('An error has occured: %s:' % str(val))


return

