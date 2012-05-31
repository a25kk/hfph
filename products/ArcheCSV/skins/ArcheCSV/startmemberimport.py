## Script (Python) "startmemberimport"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=
##

response=context.REQUEST.RESPONSE

head=context.head
csvdata=context.getCSVdata()

map_fields=list(context.getMap_fields())

member_fields= context.portal_memberdata.propertyIds()



member_mapping={}

response.setHeader('Content-type', 'text/html')
response.write('<font size=2>[%s]: Starting import...<br />' % str(DateTime().strftime('%H:%M.%S')))

try:
    for i in range(len(head)):
       member_mapping[map_fields[i]]=head[i]
       #response.write("assigning "+head[i]+'-->'+map_fields[i])

    memberdictionaries=[]
    csvdata=csvdata[1:]
    multivalsep = context.getMulti_valued_separator()

    for i in range(len(csvdata)):
        memberdict={}
        for f in member_fields:
            if member_mapping.has_key(f):
                k=member_mapping[f]
                # if it is a LinesField generated a list by splitting on the the ';' character
                # eventually this separator should be done based on a character defined at run time

                if context.portal_memberdata.getPropertyType(f) == 'boolean':
                    if csvdata[i][k] == "True":
                        memberdict[f] = 1
                    elif csvdata[i][k] == "False":
                        memberdict[f] = 0
                    else:
                        memberdict[f]=int(csvdata[i][k])
                elif context.portal_memberdata.getPropertyType(f) == 'float':
                    memberdict[f]=float(csvdata[i][k])
                elif context.portal_memberdata.getPropertyType(f) == 'int':
                    memberdict[f]=int(csvdata[i][k])
                elif context.portal_memberdata.getPropertyType(f) == 'lines':
                    memberdict[f]=csvdata[i][k].split(multivalsep)
                    memberdict[f]=[m.strip() for m in memberdict[f]]
                    memberdict[f]=memberdict[f].join('\n')
                elif context.portal_memberdata.getPropertyType(f) == 'long':
                    memberdict[f]=long(csvdata[i][k])
                elif context.portal_memberdata.getPropertyType(f) == 'tokens':
                    memberdict[f]=csvdata[i][k].split(multivalsep)
                    memberdict[f]=[m.strip() for m in memberdict[f]]
                elif context.portal_memberdata.getPropertyType(f) == 'multiple':
                    memberdict[f]=csvdata[i][k].split(multivalsep)
                    memberdict[f]=[m.strip() for m in memberdict[f]]
                else: 
                    memberdict[f]=csvdata[i][k]
        
        login = csvdata[i].get(head[int(context.getMap_login_field())]).strip()
        
        password = None
        if context.getMap_password_field():
            password = csvdata[i].get(head[int(context.getMap_password_field())]).strip()
        #response.write('csvdata[i] %s<br />' % str(csvdata[i]))
        #response.write('login field %s<br />' % context.getMap_login_field())
        #response.write('login %s<br />' % login)

        if context.getMap_password_field():
            password = csvdata[i].get(head[int(context.getMap_password_field())]).strip()

        roles = []
        if context.getMap_role_field():
            roles = csvdata[i].get(head[int(context.getMap_role_field())]).split(multivalsep)
            roles = [r.strip() for r in roles]
        #response.write('roles %s<br />' % str(roles))

        groups=[]
        if context.getMap_group_field():
            groups = csvdata[i].get(head[int(context.getMap_group_field())]).split(multivalsep)
            groups = [g.strip() for g in groups]
        #response.write('groups %s<br />' % str(groups))

        memberdictionaries.append((login, memberdict, roles, groups, password))

    counter=0
    total=len(memberdictionaries)

    pm = context.portal_membership

    response.write('Processing %d members<br />' % len(memberdictionaries))

    operation = context.getOperation()

    for login, properties, roles, groups, password in memberdictionaries:
        member = None
        try:
            member = pm.getMemberById(login)
        except:
            #exception_info = context.HTMLFormatExceptionInfo()
            response.write("Getting the member by id failed due to the following error: %s" % str(pm.getMemberById))
        if member is None:
            if operation in ['add', 'add_and_update']:
                try:
                    context.addMember(login, properties, roles, groups, password)
                    counter=counter+1
                except:
                    exception_info = context.HTMLFormatExceptionInfo()
                    response.write("Member could not be added due to the following error: %s" % str(exception_info))
            elif operation == 'update':
                response.write("Member not found: %s<br />" % login)
                if context.getStop_import_when_member_not_found_on_update():
                    response.write("Stopping import because member to update was not found")
                    return
            else:
                raise "Unknown operation"
        else:
            if operation == 'add':
                response.write("Member already exists: %s<br />" % login)
                if context.getStop_import_when_member_already_exists_on_add():
                    response.write("Stopping import because member to add alreay exists")
                    return
            elif operation == 'add_and_update':
                pass
            elif operation == 'update':
                pass
            else:
                raise "Unknown operation"
            try:
                context.updateMember(login, properties, roles, groups)
                counter=counter+1
            except:
                exception_info = context.HTMLFormatExceptionInfo()
                response.write("Updating the member failed due to the following error: %s" % str(exception_info))
            #context.setMemberProperties(member, properties)
        perc=float(counter)/float(total)*100
        response.write('Processing: login: %s, roles: %s, groups: %s, properties:%s<br />' % (login,str(roles), str(groups), str(properties)))
        response.write('[progress:%i out of %i (%.2f %%)]<br />' % (counter,total,perc))
    response.write('[%s]: Done!' % str(DateTime().strftime('%H:%M.%S')))

except:
    exception_info = context.HTMLFormatExceptionInfo()
    response.write("An error has occured: %s" % exception_info)
    raise

return

