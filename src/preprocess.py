import argparse
import time
import json
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
        location = data['location']
        id = mac+'_'+location+'_'+time.strftime('%Y-%m-%dT%H:%M:%S%z',timestamp)
        outdata.append([id,location,mac,timestamp])

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

    location=args.input.name
    print(location)
    # TODO parse out just the location eg oltorf.log
    location='oltorf'

    indata = args.input.readlines()
    outdata = []

    for line in indata:
        mac, epoch = line.split()
        timestamp = time.localtime(float(epoch))
        #TODO lookup manufacturer from mac
        outdata.append({'location': location, 'mac': anonymize(mac), 'timestamp': timestamp})

    raw_data = generate_raw_dataset(outdata, args.output)
    upsert_data(creds, raw_data, 'eitg-njyb')

    # TODO Add other processing here

if __name__ == "__main__":
    main()
