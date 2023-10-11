# Automated_Download
This is the code for automating data download from ASF

# Usage
AutoDownloader.py should be run on a regular schedule with a valid username and password as command-line arguments

DownloadManager.py can be imported and used to maintain areas of interest

# Bugs/Issues

1. DownloadManager.modify_area() does not currently allow constraints to be removed

2. DownloadManager.new_area() and DownloadManager.modify_area() could stand to support more convenient forms of the begin= parameter than an integer timestamp (ask Roger what date/time form he'd most easily use)

3. Modifying, removing, and re-adding areas could be more worked out
    * modify_area(), polygon changed: downloads should be re-tested for intersection, as some will be irrelevant. New downloads for now-relevant products may need to be made
    * modify_area(), begin made earlier: new downloads need to be made that are between the new and previous beginning time
    * modify_area(), begin made later: should now-irrelevant files be reorganized in any way?
    * remove_area(): same as previous
    * add_area(), new area with same name as previously-removed area: should new files be stored with any old files that may remain from the previous instance?

4. AutoDownloader technically doesn't use the begin timestamp properly, as begin implies beginning of data collection, not earliest processing date