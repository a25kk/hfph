## Script (Python) "startmemberexport"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=
##

response=context.REQUEST.RESPONSE

csv_header = ['login',]
if context.getExport_roles():
    csv_header = csv_header + ['roles',]    
if context.getExport_groups():
    csv_header = csv_header + ['groups',]    
if context.getExport_password():
    csv_header = csv_header + ['password',]    
member_fields= context.portal_memberdata.propertyIds()
if member_fields:
    csv_header = csv_header + list(member_fields)
additional_props = context.getAdditional_properties()
if additional_props:
    csv_header = csv_header + list(additional_props)

multivalsep = context.getMulti_valued_separator()
logpropdict = context.getLog_property_dictionary()

members=[]

response.setHeader('Content-type', 'text/html')
response.write('<font size=2>[%s]: Starting export...<br />' % str(DateTime().strftime('%H:%M.%S')))

try:
    counter=0
    memberids = context.getMember_ids()

    total=len(memberids)
    
    pm = context.portal_membership

    response.write('Processing %d members<br />' % total)

    for memberid in memberids:
        member = None
        try:
            member = pm.getMemberById(memberid)
        except:
            exception_info = context.HTMLFormatExceptionInfo()
            response.write("Getting the member by id failed due to the following error: %s" % str(exception_info))
        if member is None:
            if context.getStop_export_when_member_not_found():
                response.write('Stopping export because a member was not found: %s<br />' % memberid)
                return
            else:
                pass
        else:
            memberdict = {'login':memberid}
            if context.getExport_roles():
                memberdict['roles'] = []
                try:
                    memberdict['roles']=member.getRoles()
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Getting member roles failed due to the following error: %s" % exception_info)
                if same_type(memberdict['roles'],[]) or same_type(memberdict['roles'],()):
                    memberdict['roles']=multivalsep.join(memberdict['roles'])                    
            if context.getExport_groups():
                memberdict['groups'] = []
                try:
                    memberdict['groups']=member.getGroupNames()
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Getting member groups failed due to the following error: %s" % exception_info)
                if same_type(memberdict['groups'],[])  or same_type(memberdict['groups'],()):
                    memberdict['groups']=multivalsep.join(memberdict['groups'])                    
            if context.getExport_password():
                memberdict['password'] = ''
                try:
                    memberdict['password']=context.get_member_password(member, memberid)
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Getting member password failed due to the following error: %s" % exception_info)
            for field in member_fields:
                memberdict[field]=''
                try:                    
                    memberdict[field]=getattr(member,field)
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Getting member property info failed due to the following error: %s" % exception_info)                        
                if same_type(memberdict[field],[]) or same_type(memberdict[field],()):
                    memberdict[field]=multivalsep.join(memberdict[field])                    
            for field in additional_props:
                memberdict[field]=''
                try:
                    memberdict[field]=member.getProperty(field)
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Getting extra member info failed due to the following error: %s" % exception_info)
                if same_type(memberdict[field],[]) or same_type(memberdict[field],()):
                    memberdict[field]=multivalsep.join(memberdict[field])                    
            members.append(memberdict)
            counter=counter+1
            
        perc=float(counter)/float(total)*100
        if logpropdict:
            response.write('Processing: id: %s, properties:%s<br />' % (memberid,str(memberdict)))
        else:
            response.write('Processing: id: %s<br />' % memberid)
        response.write('[progress:%i out of %i (%.2f %%)]<br />' % (counter,total,perc))
except:
    exception_info = context.HTMLFormatExceptionInfo()
    response.write("An error has occured: %s" % exception_info)
    raise

response.write('Writing .csv file')
context.createcsv(csv_header, members)
response.write('[%s]: Done!' % str(DateTime().strftime('%H:%M.%S')))

return

