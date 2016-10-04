# stupid scrapy makes it so hard to download files...
# so I just grabbed the urls for the videos
# and this script downloads them all
import requests
import json
from tqdm import tqdm
import os
import glob

scrapeDir = './scrapy/scrape_prez/'
with open(scrapeDir + 'config.json') as f:
    config = json.load(f)

mainFilePath = config['file_dir']

def download_file(url):
    local_filename = url.split('/')[-1]
    print 'downloading', local_filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    response = requests.head(testFile)
    fsize = int(response.headers['Content-Length']) # I think file size in bytes?
    with open(os.path.join('videos', local_filename), 'wb') as f: # could also use mainFilePath here
        for chunk in tqdm(r.iter_content(chunk_size=1024), total=fsize/1024): # I think chunk_size is in bytes?
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

# get latest output file
newest = max(glob.iglob(scrapeDir + '*.prez.json'), key=os.path.getctime)
with open(newest) as prez:
    weekly = json.load(prez)

# test downloading
testFile = weekly[0]['videoLink']
download_file(testFile)

# for w in weekly:
#     download_file(w['videoLink'])
