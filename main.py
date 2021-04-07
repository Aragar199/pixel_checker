import csv
from progress.bar import Bar
import re
import requests
import os

'''function that extracts urls from the csv file and creates a key value pair of tactic_id: [urls]'''
def url_extract(abs_path):
    #create a dictionary to store tactic ids and urls
    stored_urls = {}
    #context manager to handle file access
    with open(abs_path) as csvfile:
        #read headers like a dictionary
        pixelfile = csv.DictReader(csvfile)
        #loop through each row, find all values within quotes starting with http using regex and create a list
        for row in pixelfile:
            pixel_list = re.findall(r'"(http.*?)"', row['impression_pixel_json'])
            #get the tactic id
            tactic_id = row['tactic_id']
            #associate the list of urls with the tactic id if the tactic id does not exist yet and skip over any empty
            #urls (for example if the url is [])
            if tactic_id not in stored_urls and pixel_list:
                #remove the extra \\ in the url to format correctly
                stored_urls[tactic_id] = [url.replace('\\', '') for url in pixel_list]
            #if the list is not empty
            elif pixel_list:
                for pixel in pixel_list:
                    #do no thing if the url is already in the list
                    if pixel not in stored_urls[tactic_id]:
                        #clean up and append to the list
                        stored_urls[tactic_id].append(pixel.replace('\\', ''))
    return stored_urls

'''function that orchestrates url firing and returns results'''
def pixel_check(tactic_pixels):
    #create an object to store the success, failures, and a list of tactic ids that will include the failed urls
    status_counter = {'OK': 0,
                   'Failed': 0,
                   'failed_tacticid': []}
    #create the session once for performance
    s = requests.Session()
    #use a progress bar so you know it is working
    with Bar('Processing...', max=len(tactic_pixels)) as bar:
        for tactic_id in tactic_pixels:
            bar.next()
            #loop through the urls per tactic id and fire
            for url in tactic_pixels[tactic_id]:
                #record success or failure
                if pixel_fire(s, url):
                    status_counter['OK'] += 1
                else:
                    status_counter['Failed'] += 1
                    status_counter['failed_tacticid'].append([tactic_id, url])
    return status_counter

'''function that fires each pixel and returns success or failure as boolean'''
def pixel_fire(session, pixel_url):
    #add dummy header in case the server is filtering by no header requests
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/81.0.4044.141 Safari/537.36"}
    #in case of error just try and catch, any exceptions are failures
    try:
        #use requests.head() from requests library to just check status code instead of full GET request to improve
        #response times and set timeout to something reasonable (default is 5 minutes and takes way too long)
        r = session.head(pixel_url, timeout=0.05, headers=headers)
        if r.status_code >= 200 < 400:
            return True
        elif r.status_code >= 400:
            return False
    except Exception:
        False


if __name__ == "__main__":
    #user inputs the abs file path to the csv we are ingesting and checks if correct
    user_input = input("Please enter absolute file path to csv file: \n")
    assert os.path.exists(user_input), "File path cannot be found at {}".format(user_input)
    #extract tactic_id:[urls]
    pixel_urls = url_extract(user_input)
    #fire pixels and record success
    http_status = pixel_check(pixel_urls)
    #print out results from the script
    for tactic_id, url in http_status['failed_tacticid']:
        print('Failed tactic id: {} | Failed url: {}'.format(tactic_id, url))
    print('Final Tally: \n Success = {}\n Failure = {}'.format(http_status['OK'], http_status['Failed']))