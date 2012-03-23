import sys
import WeoGeoAPI

# define globals for authentication
if len(sys.argv) > 3:
    LIBRARY, USERNAME, PASSWORD = sys.argv[1],sys.argv[2],sys.argv[3]
else:
    LIBRARY, USERNAME, PASSWORD = ("YOUR-LIBRARY-SUBDOMAIN.weogeo.com",
                                   "YOUR-LIBRARY-USERNAME",
                                   "YOUR-LIBRARY-PASSWORD")

# instantiate the weosession and connect
weos = WeoGeoAPI.weoSession(LIBRARY, USERNAME, PASSWORD)
if not weos.connect():
    print "Couldn't connect with the credentials provided."
    sys.exit()

http_response, groups_dict = weos.getGroups("JSON")
print "="*20,"\n","Group Name,ID","\n","="*20
for item in groups_dict["items"]:
    print "%s,%s" % (item["name"], item["id"])
print "="*20,"\n"
    
http_response, roles_dict = weos.getRoles("JSON")
print "="*20,"\n","Role Name,ID","\n","="*20
for item in roles_dict["items"]:
    print "%s,%s" % (item["name"], item["id"])
print "="*20,"\n"
    
http_response, datasets_dict = weos.getDatasets("JSON")
print "="*20,"\n","Dataset Name,token","\n","="*20
for item in datasets_dict["items"]:
    print "%s,%s" % (item["name"], item["token"])
print "="*20,"\n"

http_response, users_dict = weos.getLibraryUsers("JSON")
print "="*20,"\n","user, email","\n","="*20
for item in users_dict["items"]:
    print "%s,%s" % (item["user"]["username"], item["user"]["email_id"])
print "="*20,"\n"

    