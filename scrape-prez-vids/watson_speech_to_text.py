import requests
import os
import json

API_ENDPOINT = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
API_DEFAULT_PARAMS = {
    'continuous': True,
    'timestamps': True,
    'word_confidence': True,
    'profanity_filter': False,
    'word_alternatives_threshold': 0.4
}

API_DEFAULT_HEADERS = {
    'content-type': 'audio/wav'
}



def speech_to_text_api_call(audio_filename, username, password):
    with open(audio_filename, 'rb') as a_file:
        http_response = requests.post(API_ENDPOINT,
                      auth=(username, password),
                      data=a_file,
                      params=API_DEFAULT_PARAMS,
                      headers=API_DEFAULT_HEADERS,
                      stream=False)
        return http_response

if __name__ == "__main__":
    testFile = 'videos/20161001_Weekly_Address_HD.wav'
    uname = os.environ['BLUEMIX_UNAME']
    passwd = os.environ['BLUEMIX_PASS']
    response = speech_to_text_api_call(testFile, uname, passwd)
    speechJson = json.loads(response.content) # keys are [u'results', u'result_index']
    timestamps = [] # list of [word, starttime, endtime], i.e. [u'a', 188.62, 188.87]
    for i in range(len(speechJson['results'])):
        timestamps.extend(speechJson['results'][i]['alternatives'][0]['timestamps'])
