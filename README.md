# Automated_Download
This is the code for automating data download from ASF

# Usage
AutoDownloader.py should be run on a regular schedule with a valid username and password as command-line arguments

DownloadManager.py can be imported and used to maintain areas of interest

# Bugs/Issues

1. DownloadManager.modify_area() does not currently allow constraints to be removed (FIXED)

2. DownloadManager.new_area() and DownloadManager.modify_area() could stand to support more convenient forms of the begin= parameter than an integer timestamp (ask Roger what date/time form he'd most easily use) (FIXED)

3. Modifying, removing, and re-adding areas could be more worked out
    * modify_area(), polygon changed: downloads should be re-tested for intersection, as some will be irrelevant. New downloads for now-relevant products may need to be made
    * modify_area(), begin made earlier: new downloads need to be made that are between the new and previous beginning time
    * modify_area(), begin made later: should now-irrelevant files be reorganized in any way?
    * remove_area(): same as previous
    * add_area(), new area with same name as previously-removed area: should new files be stored with any old files that may remain from the previous instance?

4. AutoDownloader technically doesn't use the begin timestamp properly, as begin implies beginning of data collection, not earliest processing date

5. It may be useful to have the ability to specify several sets of constraints rather than just one, e.g. two collect from two different path/frame combinations


Notes:

arguments wanting

specify begin= "DDMMYYYY" 

additional kwargs for constraints:
-filetype (we'll use .RAW)
-beam mode (IW)
-direction
-path and frame filters:
    each area has its own combination
    all must be the same

Troublesome Fire

p 56 F 454 descending
//p 151 f 129 ascending

DEM: -106.344088 -104.968772, 40.0000000, 40.859412

date range: October 1 to December 12 2020


