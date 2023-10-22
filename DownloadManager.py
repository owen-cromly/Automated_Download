import json
import os.path
import sys
import time
import datetime


    
# global variable path
dm_path = os.path.join(os.path.dirname(__file__), "dm_meta.json")
# global variable dm_date_format
dm_date_format = '%d%m%Y'

def set_up(path_for_downloads: str = os.path.dirname(sys.argv[0]), folder_name: str = None, noFolder = False):
    ## determine if the thing is already set up
    if(os.path.exists(dm_path)):
        print("Download manager already set up; set_up() doing nothing. Call help() for help.")
        return
    ## create the path to the downloads directory
    if(folder_name):
        downloads_path = os.path.join(path_for_downloads, folder_name)
    else:
        if (path_for_downloads != os.path.dirname(sys.argv[0]) or noFolder):
            downloads_path = path_for_downloads
        else:
            downloads_path = os.path.join(path_for_downloads, "autodownloads")
    ## create uniform slashes
    downloads_path = downloads_path.replace('/', '\\')
    ## create directories for (static declared) meta_path and downloads_path
    os.makedirs(downloads_path, exist_ok=True)
    os.makedirs(os.path.dirname(dm_path), exist_ok=True)
    ## initialize dm_meta.json with proper structure
    data = {
        "downloads_directory": downloads_path,
        "areas": {},
        "area_example": {
            "Los Angeles": {
                "name": "Los Angeles",
                "polygon": "POLYGON((30 30, 30 40, 40 40, 40 30, 30 30))",
                "begin": 626244364,
                "last_download": 626244364,
                "constraints": {
                    "platform": "Sentinel-1"
                }
            }
        }
    }
    with open(dm_path, 'w') as file:
        json.dump(data, file, indent=4)
    print("download manager has automatically set up upon first import. You now have the folder 'autodownloads'. To rename or move this folder, use modify_destination(parent_directory: str, folder_name: str)")

    
def help():
    print("You called the .set_up() static method but DownloadManager believes it has already been set up because of the file \"dm_meta.json\". SOLUTIONS: remove this line of code if you are indeed set up, OR delete \"dm_meta.json\" from the directory in which DownloadManager.py is placed if it shouldn't be there, OR place DownloadManager.py into a subdirectory on its own")


def new_area(
        name: str = None,
        polygon: str = None, 
        dem: str = None,
        begin: str = None, 
        **kwargs
        ):
    if not (((polygon!=None) ^ (dem!=None)) and begin and name):
        raise Exception("newArea(): you must provide a WKT POLYGON kwarg 'polygon=', a timestamp kwarg 'begin=', and a string kwarg 'name='")
    if dem:
        polygon = demToPolygon(dem)
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
        if name in meta_dict["areas"]:
            raise Exception("Error: cannot add an area named \""+name+"\" when an area of that name has already been added")
        meta_dict["areas"][name] = {
            "name": name,
            "polygon": polygon,
            "begin": dateToTimestamp(begin),
            "last_download": dateToTimestamp(begin),
            "constraints": kwargs
        }
        # if start and end parameters are provided, convert them from date to timestamp
        if meta_dict["areas"][name].get("constraints", meta_dict).get("start", None):
            meta_dict["areas"][name]["constraints"]["start"] = dateToTimestamp(meta_dict["areas"][name]["constraints"]["start"])
        if meta_dict["areas"][name].get("constraints", meta_dict).get("end", None):
            meta_dict["areas"][name]["constraints"]["end"] = dateToTimestamp(meta_dict["areas"][name]["constraints"]["end"])
        # if flightDirection and frame are both provided and flightDirection is a list, ensure that frame is a list of the same length
        if meta_dict["areas"][name].get("constraints", meta_dict).get("flightDirection", None) and type(meta_dict["areas"][name]["constraints"]["flightDirection"])==list:
            if not (meta_dict["areas"][name].get("constraints", meta_dict).get("frame", None) and type(meta_dict["areas"][name]["constraints"]["frame"])==list and len(meta_dict["areas"][name]["constraints"]["frame"])==len(meta_dict["areas"][name]["constraints"]["flightDirection"])):
                raise Exception("area ["+name+"] not added. You cannot add a list of flightDirection if you do not have an equally-sized list of frame (the list feature is to provide the ability to store several path-frame combinations)")
    with open(dm_path, 'w') as meta:
        json.dump(meta_dict, meta, indent=4)
    os.makedirs(os.path.join(meta_dict["downloads_directory"], name), exist_ok = True)

def get_area(area: str):
    with open(dm_path, 'r') as file:
        try:
            return json.load(file)["areas"][area]
        except:
            return None

def modify_area(
        areaname: str,
        name: str = None,
        polygon: str = None,
        dem: list = None,
        begin: int = None,
        **kwargs
        ):
    if not ((name or polygon or dem or begin or kwargs) and not(polygon and dem)):
        print("Warning: you called modify_area() but did not provide any update information, nothing was done")
        return
        #raise Exception("newArea(): you must provide a WKT POLYGON kwarg 'polygon=', a timestamp kwarg 'begin=', and a string kwarg 'name='")
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
    if name:
        # rename the destination subfolder, the name in areas, and the name in areas[area]
        os.rename(os.path.join(meta_dict["downloads_directory"], meta_dict["areas"][areaname]["name"]), os.path.join(meta_dict["downloads_directory"], name))
        meta_dict["areas"][areaname]["name"] = name
        meta_dict["areas"][name] = meta_dict["areas"].pop(areaname)
    if polygon:
        meta_dict["areas"][name]["polygon"] = polygon
    if begin:
        meta_dict["areas"][name]["begin"] = begin
    if kwargs:
        # place all kwargs in constraints, delete those specified as None
        for k, v in kwargs.items():
            if v:
                meta_dict["areas"][name]["constraints"][k] = v
            else:
                del meta_dict["areas"][name]["constraints"][k]
        # convert start and end times from dm_date_format to the proper int timestamp format
        if kwargs.get("start", None):
            meta_dict["areas"][name]["constraints"]["start"] = dateToTimestamp(kwargs["start"])
        if kwargs.get("end", None):
            meta_dict["areas"][name]["constraints"]["end"] = dateToTimestamp(kwargs["end"])
    with open(dm_path, 'w') as meta:
        json.dump(meta_dict, meta, indent=4)

def remove_area(name):
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
    if(name in meta_dict["areas"]):
        del meta_dict["areas"][name]
        with open(dm_path, 'w') as meta:
            json.dump(meta_dict, meta, indent=4)
        if not os.listdir(os.path.join(meta_dict["downloads_directory"], name)):
            os.rmdir(os.path.join(meta_dict["downloads_directory"], name))

def get_destination(area: str):
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
        if not area:
            return meta_dict["downloads_directory"]
        return os.path.join(meta_dict["downloads_directory"], area)
    
def get_areas():
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
        return meta_dict["areas"]

def modify_destination(parent_directory: str = None, folder_name: str = None):
    ## load the data
    with open(dm_path, 'r') as meta:
        meta_dict = json.load(meta)
    ## decide the name of the new directory
    os.path.join(os.path.dirname(sys.argv[0]), )
    if parent_directory is not None:
        if folder_name:
            if(os.path.isabs(parent_directory)):
                newdir = os.path.join(parent_directory, folder_name)
            else:
                newdir = os.path.join(os.path.dirname(sys.argv[0]), parent_directory, folder_name)
        else:
            if(os.path.isabs(parent_directory)):
                newdir = os.path.join(parent_directory, os.path.basename(meta_dict["downloads_directory"]))
            else:
                newdir = os.path.join(os.path.dirname(sys.argv[0]), parent_directory, os.path.basename(meta_dict["downloads_directory"]))
    elif folder_name:
        newdir = os.path.join(os.path.dirname(meta_dict["downloads_directory"]), folder_name)
    else:
        return
    newdir = newdir.replace('/', '\\')
    ## make sure the parent directory exists, create it if needed
    os.makedirs(os.path.dirname(newdir), exist_ok=True)
    ## move the actual directory (this will result in an error and stop the function before any harm is done if the new directory is poorly formed)
    os.rename(meta_dict["downloads_directory"], newdir)
    ## now that the directory has successfully been moved, change the name in meta and write to the file
    meta_dict["downloads_directory"] = newdir
    with open(dm_path, 'w') as meta:
        json.dump(meta_dict, meta, indent=4)
    
def success(name: str, timestamp: int):
    # load the data
    with open(dm_path, 'r') as file:
        meta = json.load(file)
    if name in meta["areas"]:
        if timestamp >= meta["areas"][name]["last_download"] and timestamp <= int(time.time()):
            meta["areas"][name]["last_download"] = timestamp
            with open(dm_path, 'w') as file:
                json.dump(meta, file, indent=4)
        else:
            raise Exception("success() called with an invalid timestamp")
    else:
        raise Exception("success() called with an invalid area name")

if not (os.path.exists(dm_path)):
    set_up()

def dateToTimestamp(date: str):
    return int(datetime.datetime.strptime(date, dm_date_format).timestamp())
    
def timestampToDate(timestamp: int):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime(dm_date_format)

def demToPolygon(list: list):
    return "POLYGON(("+str(list[0])+" "+str(list[2])+", "+str(list[0])+" "+str(list[3])+", "+str(list[1])+" "+str(list[3])+", "+str(list[1])+" "+str(list[2])+", "+str(list[0])+" "+str(list[2])+"))"
