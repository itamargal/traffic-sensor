import argparse
import time
import json
import os
import random
import requests

random.seed()
known_macs = {}

def anonymize(mac):
    if mac in known_macs:
        anon = known_macs[mac]
    else:
        anon = str(random.getrandbits(32))
        known_macs[mac] = anon
    return anon

def generate_raw_dataset(indata, outfile):
    outdata=[]

    for data in indata:
        mac = data['mac']
        timestamp = data['timestamp']
        idtimestr = time.strftime('%Y%m%dT%H%M%S%z',timestamp)
        timestr = time.strftime('%Y-%m-%dT%H:%M:%S',timestamp)
        location = data['location']
        id = '{}_{}_{}'.format(mac, location, idtimestr)
        outdata.append({'id':id,'device_address':mac,'reader_name':location,'read_time':timestr})

    # TODO turn off debug data dump
    json.dump(outdata, outfile)

    return outdata

# TODO Taken from transportation-data-publishing/socrata_helpers.py - import for reuse?
def upsert_data(creds, payload, resource):
    print('upsert open data ' + resource)

    if creds['user'] != None and creds['password'] != None:
        url = 'https://data.austintexas.gov/resource/{}.json'.format(resource)

        try:
            auth = (creds['user'], creds['password'])
            json_data = json.dumps(payload)
            res = requests.post(url, data=json_data, auth=auth, verify=False)

        except requests.exceptions.HTTPError as e:
            raise e

        return res.json()
    else:
        print('Skipping upload due to incomplete credentials')

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('input', type=open, help='input data file')
    parser.add_argument('output', type=argparse.FileType('w'), help='debug output data file')
    parser.add_argument('--user', help='socrata user')
    parser.add_argument('--password', help='socrata password')
    args = parser.parse_args()

    creds = {'user':args.user, 'password':args.password}
    print(creds)

    # TODO Add multifile support

    # Get the location name from the filename eg /x/y/z/benwhite.log -> benwhite
    location=os.path.basename(args.input.name)
    location=location[:location.find('.')]

    indata = args.input.readlines()
    outdata = []

    for line in indata:
        mac, epoch = line.split()
        timestamp = time.localtime(float(epoch))
        #TODO lookup manufacturer from mac
        outdata.append({'location': location, 'mac': anonymize(mac), 'timestamp': timestamp})

    raw_data = generate_raw_dataset(outdata, args.output)
    result = upsert_data(creds, raw_data, 'eitg-njyb')
    print(result)

    # TODO Add other processing here

if __name__ == "__main__":
    main()
