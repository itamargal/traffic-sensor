import argparse
import time
import json
import random

random.seed()
knownMacs = {}

def anonymize(mac):
    if mac in knownMacs:
        anon = knownMacs[mac]
    else:
        anon = str(random.random())
        knownMacs[mac] = anon
    return anon

def generateRawDataSet(indata, outfile):
    outdata=[]

    for data in indata:
        mac = data['mac']
        timestamp = data['timestamp']
        location = data['location']
        id = mac+'_'+location+'_'+time.strftime('%Y-%m-%dT%H:%M:%S%z',timestamp)
        outdata.append([id,location,mac,timestamp])

    json.dump(outdata, outfile)

def publishJson(json, datasetid):
    # TODO publish to socrata
    print( "publish something to ", datasetid)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('input', type=open, help="input data file")
    parser.add_argument('output', type=argparse.FileType('w'), help="output data file")
    args = parser.parse_args()

    location=args.input.name
    print(location)
    # TODO parse out just the location eg oltorf.log
    location="oltorf"

    indata = args.input.readlines()
    outdata = []

    for line in indata:
        mac, epoch = line.split()
        timestamp = time.localtime(float(epoch))
        #TODO lookup manufacturer from mac
        outdata.append({'location': location, 'mac': anonymize(mac), 'timestamp': timestamp})

    rawJson = generateRawDataSet(outdata, args.output)
    publishJson(rawJson, "rawset identifier")

    # TODO Add other processing here

if __name__ == "__main__":
    main()
