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
    outdata = []

    for data in indata:
        mac = data['mac']
        timestamp = data['timestamp']
        idtimestr = time.strftime('%Y%m%dT%H%M%S%z', timestamp)
        timestr = time.strftime('%Y-%m-%dT%H:%M:%S', timestamp)
        location = data['location']
        id = '{}_{}_{}'.format(mac, location, idtimestr)
        outdata.append({'id': id, 'device_address': mac, 'reader_name': location, 'read_time': timestr})

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

def aggregate_data(lines):
    # data1 = ['benwhite', 'c8:b3:a5:', 1457093877]
    # data2 = ['benwhite', 'c8:b3:a5:', 1457093878]
    # data3 = ['oltorf', 'c8:b3:a5:', 1457093924]
    # data4 = ['oltorf', 'c8:b3:a5:', 1457093923]
    # lines = [data1, data2, data3, data4]
    location_times = dict()
    device_loc_time = {}
    dev_loc_sequence = {}

    for datapoint in lines:
        location = datapoint['location']
        device = datapoint['mac']
        devtime = datapoint['epoch']

        # Update "device_loc_time" dictionary
        if (location, device) not in device_loc_time:
            device_loc_time[(location, device)] = list()
        device_loc_time[(location, device)].append(devtime)

        # Update "dev_loc_sequence" dictinonary
        if device not in dev_loc_sequence:
            dev_loc_sequence[device] = list()
        dev_loc_sequence[device].append((location, devtime))

    for device in dev_loc_sequence:
        # print("%s: %s" % (device, dev_loc_sequence[device]))
        dev_loc_sequence[device] = sorted(dev_loc_sequence[device], key=lambda x: x[1])
        # print("%s: %s" % (device, dev_loc_sequence[device]))

    # Create a dictionary of trip times
    trips = dict()
    for device, loc_times in dev_loc_sequence.items():
        start_loc = loc_times[0][0]
        start_time = max(device_loc_time[(start_loc, device)])
        end_loc = loc_times[-1][0]
        end_time = max(device_loc_time[(end_loc, device)])
        trips[device] = (
            device,
            start_time,
            'N' if start_loc == 'benwhite' else 'S',
            end_time - start_time,
        )
        print("%s: %s" % (device, trips[device]))


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('input', type=open, help='input data file')
    parser.add_argument('output', type=argparse.FileType('w'), help='debug output data file')
    parser.add_argument('--user', help='socrata user')
    parser.add_argument('--password', help='socrata password')
    args = parser.parse_args()

    creds = {'user': args.user, 'password': args.password}
    print(creds)

    # TODO Add multifile support

    # Get the location name from the filename eg /x/y/z/benwhite.log -> benwhite
    location = os.path.basename(args.input.name)
    location = location[:location.find('.')]

    indata = args.input.readlines()
    outdata = []

    for line in indata:
        mac, epoch = line.split()
        epoch = float(epoch)
        timestamp = time.localtime(epoch)
        # TODO lookup manufacturer from mac
        outdata.append({'location': location, 'mac': anonymize(mac), 'timestamp': timestamp, 'epoch':epoch})

    raw_data = generate_raw_dataset(outdata, args.output)
    result = upsert_data(creds, raw_data, 'eitg-njyb')
    if result : print(result)

    aggregate_data(outdata)

    # TODO Add other processing here


if __name__ == "__main__":
    main()