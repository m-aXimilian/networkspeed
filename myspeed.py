import speedtest
import json
import logging
import os, os.path
import time
from datetime import datetime

LOGDIR = "./speedlog"
RESDIR = "./speedres"

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)
    
logging.basicConfig(filename=LOGDIR + '/speed.log',level=logging.DEBUG)

logging.info('starting...')

if not os.path.exists(RESDIR):
    logging.debug('Created directory %s', RESDIR)
    os.makedirs(RESDIR)



class Tester:
    def __init__(self):
        self.server = []
        self.threads = None
        self.s = speedtest.Speedtest()
        self.s.get_best_server()
        logging.debug('Tester Class initialized')
    def download(self):
        self.s.download(threads=self.threads)
        logging.info('Collect Download speed info')
    def upload(self):
        self.s.upload(threads=self.threads)
        logging.info('Collect Upload speed info')
    def compose_results(self):
        self.res_dict = self.s.results.dict()
        logging.debug('Info Composed')

counter = 1
cTop = 2880
now = datetime.now()
tStamp = now.strftime("%Y/%m/%d, %H:%M:%S")

t = Tester()
t.download()
t.upload()
t.compose_results()
res_dict = t.res_dict
downStream = res_dict['download'] / 10e5
downStreamSum = downStream


upStream = res_dict['upload'] / 10e5
upStreamSum = upStream

printDict = {
    "Time": tStamp,
    "Unit": "Mbps",
    "DownloadMean": downStream,
    "DownloadRecent": downStream,
    "UploadMean": upStream,
    "UploadRecent": upStream
}

logging.info('entering loop')
while counter <= cTop:
    logging.debug('Entering iteration %d / %d at %s', counter, cTop, tStamp)

    downStreamMean = downStreamSum / counter
    upStreamMean = upStreamSum / counter

    t.download()
    t.upload()
    t.compose_results()
    res_dict = t.res_dict

    downStream = res_dict['download'] / 10e5
    upStream = res_dict['upload'] / 10e5
    
    now = datetime.now()
    tStamp = now.strftime("%Y/%m/%d, %H:%M:%S")

    printDict["Time"] = tStamp
    printDict["DownloadMean"] = downStreamMean
    printDict["DownloadRecent"] = downStream
    printDict["UploadMean"] = upStreamMean
    printDict["UploadRecent"] = upStream

    with open(RESDIR + '/downMean.json','w') as wd:
        json.dump(printDict, wd)
        logging.debug('Wrote value for iteration %d', counter)
        
    
    downStreamSum += downStream
    upStreamSum += upStream

    time.sleep(30)
    counter += 1
