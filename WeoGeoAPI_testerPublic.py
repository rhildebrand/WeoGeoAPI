from WeoGeoAPI import *

# test job, fill out the fields in order to successfully test job submission
testJob = { 'job' : {} }
testJob['job']['dataset_token'] = ''
testJob['job']['cart'] = ''                              
testJob['job']['content_license_acceptance'] = '1'           # must be '1' otherwise job will not be accepted
testJob['job']['parameters'] = {}
testJob['job']['parameters']['job_geocrop'] = ''
testJob['job']['parameters']['job_north'] = ''
testJob['job']['parameters']['job_south'] = ''
testJob['job']['parameters']['job_east'] = ''
testJob['job']['parameters']['job_west'] = ''
testJob['job']['parameters']['job_layers'] = ''
testJob['job']['parameters']['job_datum_projection'] = ''
testJob['job']['parameters']['job_spatial_resolution'] = ''
testJob['job']['parameters']['job_file_format'] = ''

testPriceRequest = { 'job' : {} }
testPriceRequest['job']['dataset_token'] = ''
testPriceRequest['job']['north']  = ''
testPriceRequest['job']['south']  = ''
testPriceRequest['job']['east']   = ''
testPriceRequest['job']['west']   = ''
testPriceRequest['job']['layers'] = ''

# set the variables below in order to test the API
testHost     = ''
testUsername = ''
testPassword = ''
testEmail    = ''

datasetToken = ''
jobToken     = ''

testLicenseName = ''
testLicenseFile = ''

# set to true the tests that should be performed
testDatasets    = False
testEvents      = False
testGroups      = False
testJobs        = False
testLibraryInfo = False
testLicenses    = False
testReport      = False
testRoles       = False 

weos = weoSession( testHost, testUsername, testPassword )

weos.connect()
print weos
print ''

# dataset test functions
if testDatasets:
    a, b = weos.getDataset( datasetToken )
    print b['token']
    a, b = weos.getDataset( datasetToken, formats.WEO )
    print b.getTagContent( 'token' )
    a, b = weos.getDataset( datasetToken, formats.XML )
    print b.getTagContent( 'token' )
    a, b = weos.getDatasets()
    print b['items'][0]['token']
    a, b = weos.getDatasets( formats.WEO )
    print b.getTagContent( 'dataset/token' )
    a, b = weos.getDatasets( formats.XML )
    print b.getTagContent( 'dataset/token' )
    upX = "<dataset><tags>api-update-test-weo-raw</tags></dataset>"
    a, b = weos.updateDataset( datasetToken, str(upX), formats.WEO )
    print a
    upX = weoXML.weoXML( "<dataset><tags>api-update-test-weo-object</tags></dataset>" )
    a, b = weos.updateDataset( datasetToken, upX, formats.WEO )
    print a
    upX = "<dataset><tags>api-update-test-xml-raw</tags></dataset>"
    a, b = weos.updateDataset( datasetToken, str(upX), formats.XML )
    print a
    upX = weoXML.weoXML( "<dataset><tags>api-update-test-xml-object</tags></dataset>" )
    a, b = weos.updateDataset( datasetToken, upX, formats.XML )
    print a
    upJ = { "dataset" : { "tags" : "api-update-test-json-raw" } }
    a, b = weos.updateDataset( datasetToken, json.dumps(upJ) )
    print a
    upJ = { "dataset" : { "tags" : "api-update-test-json-object" } }
    a, b = weos.updateDataset( datasetToken, upJ )
    print a
    a, b = weos.getTokens( 2 )
    print b
# dataset test functions end

# event test functions
if testEvents:
    a, b = weos.createDatasetEvent( datasetToken, 'info', 'test API subject - dataset', 'test API body - dataset' )
    print b['subject']
    a, b = weos.createDatasetEvent( datasetToken, 'warning', 'test API subject - dataset', 'test API body - dataset', formats.XML )
    print b.getTagContent( 'subject' )
    a, b = weos.createJobEvent( jobToken, 'info', 'test API subject - job', 'test API body - job' )
    print b['subject']
    a, b = weos.createJobEvent( jobToken, 'warning', 'test API subject - job', 'test API body - job', formats.XML )
    print b.getTagContent( 'subject' )
    a, b = weos.getDatasetEvents( datasetToken )
    dEventID = b['items'][0]['id']
    print dEventID
    a, b = weos.getDatasetEvents( datasetToken, formats.XML )
    print b.getTagContent( 'event/id' )
    a, b = weos.getJobEvents( jobToken )
    jEventID = b['items'][0]['id']
    print jEventID
    a, b = weos.getJobEvents( jobToken, formats.XML )
    print b.getTagContent( 'event/id' )
    a, b = weos.getDatasetEvent( datasetToken, dEventID )
    print b['subject']
    a, b = weos.getDatasetEvent( datasetToken, dEventID, formats.XML )
    print b.getTagContent( 'subject' )
    a, b = weos.getJobEvent( jobToken, jEventID )
    print b['subject']
    a, b = weos.getJobEvent( jobToken, jEventID, formats.XML )
    print b.getTagContent( 'subject' )
# event test functions end

# groups test functions
if testGroups:
    a, b = weos.getGroups()
    groupID = b['items'][0]['id']
    print groupID
    a, b = weos.getGroups( formats.XML )
    print b.getTagContent( 'group/id' ).strip()
    a, b = weos.getGroup( groupID )
    print b['name']
    a, b = weos.getGroup( groupID, formats.XML )
    print b.getTagContent( 'name' )
    a, b = weos.createGroup( 'someNewGroupJSON' )
    newGroupIDJSON = b['id']
    print newGroupIDJSON
    a, b = weos.createGroup( 'someNewGroupXML', formats.XML )
    newGroupIDXML = b.getTagContent( 'id' )
    print newGroupIDXML
    a, b = weos.updateGroup( newGroupIDJSON, 'someNewGroupJSONUpdated' )
    print b['name']
    a, b = weos.updateGroup( newGroupIDXML, 'someNewGroupXMLUpdated', formats.XML )
    print b
    a, b = weos.deleteGroup( newGroupIDJSON )
    print a
    a, b = weos.deleteGroup( newGroupIDXML )
    print a
# groups test functions end

# job test functions
if testJobs:
    a, b = weos.getJobs()
    jobTokenJ = b['items'][0]['token']
    print jobTokenJ
    a, b = weos.getJobs( formats.XML, "page=2" )
    jobTokenX = b.getTagContent( 'job/token' )
    print jobTokenX
    a, b = weos.getJob( jobTokenJ )
    print b['token']
    a, b = weos.getJob( jobTokenX, formats.XML )
    print b.getTagContent( 'token' )
    a, b = weos.getJobsAcrossLibraries( formats.JSON )
    print b
    a, b = weos.getJobsAcrossLibraries( formats.JSON, "page=2" )
    print b
    a, b = weos.getJobsAcrossLibraries( formats.XML )
    print b
    a, b = weos.getJobsAcrossLibraries( formats.XML, "page=2" )
    print b
    a, b = weos.getJobsInCart( formats.JSON )
    print b
    a, b = weos.getJobsInCart( formats.XML )
    print b
    a, b = weos.getPrice( testPriceRequest )
    print b
    a, b = weos.getUnfulfilledJobs()
    print b['total_entries']
    a, b = weos.getUnfulfilledJobs( formats.XML )
    print b
    a, b = weos.createJob( testJob )
    print b
# job test functions end

# library info test functions
if testLibraryInfo:
    a, b = weos.getLibraryInfo()
    print b['subdomain']
    a, b = weos.getLibraryInfo( formats.XML )
    print b.getTagContent( 'subdomain' )
    a, b = weos.getLibraryUsers()
    print b['items'][0]['user']['username']
    userID = b['items'][0]['id']
    a,b = weos.getLibraryUsers( formats.XML )
    print b.getTagContent( 'library_user/id' )
    a, b = weos.getLibraryUser( userID )
    print b['status']
    a, b = weos.getLibraryUser( userID, formats.XML )
    print b.getTagContent( 'email' )
    a, b = weos.createLibraryUser( testEmail )
    newUserID = b['id']
    print newUserID
    a,b = weos.deleteLibraryUser( newUserID )
    print a
    a, b = weos.createLibraryUser( testEmail, formats.XML )
    newUserID = b.getTagContent( 'id' )
    print newUserID
    a, b = weos.deleteLibraryUser( newUserID )
    a, b = weos.updateLibraryUser( userID, 1 )
    print b
    a, b = weos.updateLibraryUser( userID, 1, formats.XML )
    print b
# library info test functions end

# license test functions
if testLicenses:
    a, b = weos.getLicenses()
    licenseIDJSON = b['items'][1]['id']
    print licenseIDJSON
    a, b = weos.getLicenses( formats.XML )
    licenseIDXML = b.getTagsContent( 'license/id' )[1]
    print licenseIDXML
    a, b = weos.getLicense( licenseIDJSON )
    print b['name']
    a, b = weos.getLicense( licenseIDXML, formats.XML )
    print b.getTagContent( 'name' )
    a, b = weos.toggleLicenseVisibility( licenseIDXML )
    print a
    a, b = weos.toggleLicenseVisibility( licenseIDXML )
    print a
    a, b = weos.toggleLicenseVisibility( licenseIDJSON )
    print a
    a, b = weos.toggleLicenseVisibility( licenseIDJSON )
    print a
    # following tests commented out since license creation should not be tested carelessly
    # a, b = weos.createLicense( testLicenseName, testLicenseFile )
    # newLicenseIdJSON = b['id']
    # print newLicenseIdJSON
    # a, b = weos.createLicense( testLicenseName, testLicenseFile, formats.XML )
    # newLicenseIdXML = b.getTagContent( 'id' )
    # print newLicenseIdXML
    # a,b = weos.replaceLicense( newLicenseIdJSON, newLicenseIdXML )
    # print a
# license test functions end

# report test functions
if testReport:
    a, b = weos.getReport( 'datasets' )
    print a
    a, b = weos.getReport( 'datasets', formats.XML )
    print a
    a, b = weos.getReport( 'datasets', formats.CSV )
    print a
    a, b = weos.getReport( 'datasets', formats.PDF )
    print a
    a, b = weos.getReport( 'all_transactions' )
    print a
    a, b = weos.getReport( 'all_transactions', formats.XML )
    print a
    a, b = weos.getReport( 'all_transactions', formats.CSV )
    print a
    a, b = weos.getReport( 'all_transactions', formats.PDF )
    print a
    a, b = weos.getReport( 'charges' )
    print a
    a, b = weos.getReport( 'charges', formats.XML )
    print a
    a, b = weos.getReport( 'charges', formats.CSV )
    print a
    a, b = weos.getReport( 'charges', formats.PDF )
    print a
    a, b = weos.getReport( 'orders' )
    print a
    a, b = weos.getReport( 'orders', formats.XML )
    print a
    a, b = weos.getReport( 'orders', formats.CSV )
    print a
    a, b = weos.getReport( 'orders', formats.PDF )
    print a
    a, b = weos.getReport( 'library_users' )
    print a
    a, b = weos.getReport( 'library_users', formats.XML )
    print a
    a, b = weos.getReport( 'library_users', formats.CSV )
    print a
    a, b = weos.getReport( 'library_users', formats.PDF )
    print a
    a, b = weos.getReport( 'roles' )
    print a
    a, b = weos.getReport( 'roles', formats.XML )
    print a
    a, b = weos.getReport( 'roles', formats.CSV )
    print a
    a, b = weos.getReport( 'roles', formats.PDF )
    print a
    a, b = weos.getReport( 'groups' )
    print a
    a, b = weos.getReport( 'groups', formats.XML )
    print a
    a, b = weos.getReport( 'groups', formats.CSV )
    print a
    a, b = weos.getReport( 'groups', formats.PDF )
    print a

# report test functions end

# roles test functions
if testRoles:
    a, b = weos.getRoles()
    print b['items'][0]['name']
    a, b = weos.getRoles( formats.XML )
    print b.getTagContent( 'role/name' )
    a, b = weos.createRole( 'someNewRoleJSON', True )
    newRoleIDJSON = b['id']
    print newRoleIDJSON
    a, b = weos.createRole( 'someNewRoleXML', False, formats.XML )
    newRoleIDXML = b.getTagContent( 'id' )
    print newRoleIDXML
    a, b = weos.getRole( newRoleIDJSON )
    print b['name']
    a, b = weos.getRole( newRoleIDXML, formats.XML )
    print b.getTagContent( 'name' )
    a, b = weos.updateRole( newRoleIDJSON, canAccessAll = False, rtype = formats.JSON )
    print b['name']
    a, b = weos.updateRole( newRoleIDXML, canAccessAll = True, rtype = formats.XML )
    print a
    a, b = weos.deleteRole( newRoleIDJSON )
    print a
    a, b = weos.deleteRole( newRoleIDXML )
    print a
# roles test functions end 
