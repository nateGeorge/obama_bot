# obama_bot
Text to video speech (TTVS) trained on Obama's weekly addresses.

# Development pipeline

* Scrape weekly addresses and handle getting new ones each week.
  - scrapy or requests to get video links and transcriptions
  - use requests or bash to get videos

* Crop videos so a consistent view of Obama's face is obtained.
  - use openCV
  - ignore video clips where Obama's face is not present

* Extract audio from videos

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

Next up is downloading the videos.
