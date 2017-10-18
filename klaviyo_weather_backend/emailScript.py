import requests
import sys
url="http://localhost:8000/klaviyo-weather/api/sendEmail"

timezone_list=["EST","EDT","AST","ADT","CST","CDT","MST","MDT","PST","PDT","AKST","AKDT","HST","HDT"]
def sendEmail(timezone=None):
    if timezone is None:
        response=requests.post(url)
        print response.content
    else:
        response=requests.post(url,data={"timezone":timezone})
        print response.content

print "Usage: Timezone can be passed a parameter"
print "Passing without timezone with send email to all the user in the database"
if(len(sys.argv)==2):
    if(sys.argv[1] in timezone_list):
        sendEmail(sys.argv[1])
    else:
        print "Pass Timezone values as on these values"+str(timezone_list)
else:
    sendEmail()