## Script (Python) "get_simpleforum_ftests"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
selenium = context.portal_selenium
suite = selenium.getSuite()
target_language='en'
suite.setTargetLanguage(target_language)

selenium.addUser(id = 'sampleadmin',fullname='Sample Admin',roles=['Member', 'Manager',])
selenium.addUser(id = 'samplemember',fullname='Sample Member',roles=['Member',])

test_logout = suite.TestLogout()
test_admin_login  = suite.TestLoginPortlet('sampleadmin')
test_member_login  = suite.TestLoginPortlet('samplemember')
test_switch_language = suite.TestSwitchToLanguage()

plone21 = selenium.getPloneVersion() > "2.0.5"

if plone21:
    delete_from_folder = "/folder_delete?paths:list=" + suite.getTest().base + '/'
else:
    delete_from_folder = "/folder_delete?ids:list="

suite.addTests("SimpleForum",
    'Login as Sample Admin',
    test_admin_login,
    test_switch_language,
    suite.open("/reconfig_form"),
    suite.click("cb_visible_ids"),
    suite.clickAndWait("form.button.Save"),
    'Admin adds SimpleForum',
    suite.open(delete_from_folder + 'simpleforum'),
     suite.open("/"),
    suite.clickAndWait( "//a[contains(text(),'View')]"),
    suite.clickAndWait( "link=Forum"),
    suite.verifyTextPresent("Forum has been created."),
    suite.type("name=id","simpleforum"),
    suite.clickAndWait("name=form_submit"),
    suite.verifyTextPresent("Please correct the indicated errors."),
    suite.type("name=title","SimpleForum"),
    suite.clickAndWait("name=form_submit"),
    suite.verifyTextPresent("Your changes have been saved."),
    "Admin posts new topic",
    suite.open("/simpleforum"),
    suite.clickAndWait( "//a[contains(text(),'Add new topic')]"),
    suite.type('title','My Topic'),
    suite.type('text','My Topic Text'),
    suite.clickAndWait('form_submit'),
    suite.clickAndWait( "//a[contains(text(),'Reply')]"),
    suite.clickAndWait('form_submit'),
    suite.verifyTextPresent('Post Text is required, please correct.'),
    suite.clickAndWait('form_submit'),
    suite.type('text','My Topic Text'),
    suite.clickAndWait('form_submit'),
    'Login as Sample Member',
    test_member_login,
    'Member adds topic',
    suite.open("/simpleforum"),
    suite.clickAndWait( "//a[contains(text(),'Add new topic')]"),
    suite.type('title','Member added Topic'),
    suite.type('text','Member added Topic Text'),
    suite.clickAndWait('form_submit'),
    )

return suite
