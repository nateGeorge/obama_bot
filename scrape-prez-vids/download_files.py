# stupid scrapy makes it so hard to download files...
# so I just grabbed the urls for the videos
# and this script downloads them all
import requests
import json
from tqdm import tqdm
import os
import glob
import argparse as ap

parser = ap.ArgumentParser(description='Download Obamas weekly addresses')
parser.add_argument('-d', '--tqdm', default=False)
parser.add_argument('-t', '--test', default=False)

args = vars(parser.parse_args())
tqdm_on = args['tqdm']
is_test = args['test']

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
    # check if file is already fully downloaded, and skip this file if so
    vidPath = os.path.join('videos', local_filename)
    if os.path.exists(vidPath):
        if fsize == os.path.getsize(vidPath):
            print 'file already downloaded'
            return None

    with open(vidPath, 'wb') as f: # could also use mainFilePath here
        if tqdm_on:
            for chunk in tqdm(r.iter_content(chunk_size=1024), total=fsize/1024): # I think chunk_size is in bytes?
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        else:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

    return local_filename

# get latest output file
newest = max(glob.iglob(scrapeDir + '*.prez.json'), key=os.path.getctime)
with open(newest) as prez:
    weekly = json.load(prez)

# test downloading
if is_test:
    i = 0
    fn = None
    while fn is None:
        testFile = weekly[i]['videoLink']
        fn = download_file(testFile)
        i += 1
else:
    fns = []
    for w in weekly:
        fn = download_file(w['videoLink'])
        if fn is not None:
            fns.append(fn)
