# obama_bot
Text to video speech (TTVS) trained on Obama's weekly addresses.

# Development pipeline

* Scrape weekly addresses and handle getting new ones each week.
  - scrapy or requests to get video links and transcriptions
  - use requests or bash to get videos

* Extract audio from videos

* Feed audio to IBM Bluemix (Watson) with api

* Crop videos so a consistent view of Obama's face is obtained.
  - use openCV
  - ignore video clips where Obama's face is not present

* Get words and times from IBM Watson (bluemix)
  - Prototype on one video
  - get lists of words and times
  - interpolate with transcripts from whitehouse.gov

* Train neural net on audio alone
  - audio signal and words as training data
  - 2D convolution for audio signal
  - kind of like guitar hero with single words supplied over the whole time the word is being spoken

* Train neural net on audio and video
  - 3D convolution on video

## Scrape transcripts and video links

I used scrapy, maybe requests is easier?  To scrape:

```bash
cd scrape-prez-vids/scrapy/scrape_prez
```

```bash
scrapy crawl prez -o "$(date +'%d-%m-%Y-%H%M')-output.prez.json"
```

To do some manual inspection of the results:

```bash
scrapy shell https://www.whitehouse.gov/briefing-room/weekly-address
```

### Scrapy bugs notes
I was trying to use scrapy with Python3 from Anaconda, but I was getting weird errors:
I had to do `conda uninstall icu` and `conda install -c conda-forge icu=56` because I was getting the error `ImportError: libicui18n.so.56: cannot open shared object file: No such file or directory ubuntu` when I tried to do `scrapy shell`.
Then I started getting something else like `cffi library '_openssl' has no function`, so I uninstalled scrapy from anaconda and installed it with the Python2 Ubuntu system distro, and it worked.  Go figure ¯\\_(ツ)_/¯.

## Download videos

Next up is downloading the videos.  The file `download_files.py` in the `scrapy-prez-vids` will do this.
Make sure you `pip install tqdm requests json`.

```bash
cd scrape-prez-vids
python download_files.py
```

## Extracting audio

Extract audio from files by running `extract_audio.py` in the `scrape-prez-vids` folder.  You will need to sign up for [IBM Bluemix](https://github.com/watson-developer-cloud/speech-to-text-nodejs) and set up and app (then get creds with `cf env <application-name>`), and I would store your password and username in your `~/.profile` config file or grab them dynamically with `cf env <application-name>`.  Then your credentials aren't on github, and you can get them dynamically in scripts.

## Cropping vids

Now we need to make sure we have a consistent picture of Barry's face for the neural net.  I used openCV face detection, so you will need to install that to run these scripts.

```bash

```
