import asf_search as asf
import DownloadManager as dm
import time
import datetime as dt
from sys import argv



areas = dm.get_areas()
for area in areas:
    # create the string timestamp for processingDate
    processingDate = str(dt.datetime.utcfromtimestamp(areas[area]["last_download"])).replace(" ", "T")#conversionList[0]+"T"+conversionList[1]
    # if 12 days have passed, request new data
    now = int(time.time())
    if((now-areas[area]["last_download"])>1036000):
        results = asf.search(intersectsWith=areas[area]['polygon'], processingDate=processingDate, **areas[area]["constraints"], maxResults=2)
        # download all urls
        #urls = [res.properties["url"] for res in results]
        for res in results:
            res.download(path=dm.get_destination(area), session=asf.ASFSession().auth_with_creds(username=argv[1], password=argv[2]))
        dm.success(area, now)











#words = {"Three": 3, "Four": 4}
######### print(str(areas[area]["name"])+": \nresults = asf.search(intersectsWith=\""+str(areas[area]["polygon"])+"\", processingDate="+str(dt.datetime.utcfromtimestamp(areas[area]["last_download"]))+", **"+str(areas[area]["constraints"])+")")
#print(mix(one=1, **{}))
