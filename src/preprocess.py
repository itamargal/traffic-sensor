import argparse
import time
import json
import os
import random
import requests

random.seed()
known_macs = {}
known_vendors = {'cached': 0}  # keep track of caching metrics


def anonymize(mac):
    if mac in known_macs:
        anon = known_macs[mac]
    else:
        anon = str(random.getrandbits(32))
        known_macs[mac] = anon
    return anon


def generate_raw_dataset(indata):
    outdata = []

    for data in indata:
        mac = data['mac']
        timestamp = data['timestamp']
        idtimestr = time.strftime('%Y%m%dT%H%M%S%z', timestamp)
        timestr = time.strftime('%Y-%m-%dT%H:%M:%S', timestamp)
        location = data['location']
        ident = '{}_{}_{}'.format(mac, location, idtimestr)
        outdata.append({'id': ident, 'device_address': mac, 'reader_name': location, 'read_time': timestr})

    return outdata


# TODO Modified from transportation-data-publishing/socrata_helpers.py - import for reuse?
def upsert_data(creds, payload, resource):
    print('upsert open data ' + resource)

    if creds['user'] is not None and creds['password'] is not None:
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
            'N' if start_loc == 'benwhite' else 'S',  # TODO replace with something more robust
            end_time - start_time,
        )
        print("%s: %s" % (device, trips[device]))


def get_mac_manufacturer(mac):
    # TODO This could be a lot faster with a local lookup
    # Just need the first 3 segments (xx:xx:xx) for vendor lookup
    vendor_mac = mac[:8]
    if vendor_mac in known_vendors:
        vendor = known_vendors[vendor_mac]
        cached_lookups = known_vendors['cached']
        cached_lookups += 1
        known_vendors['cached'] = cached_lookups
    else:
        url = 'http://macvendors.co/api/vendorname/{}'.format(mac[:8])
        try:
            res = requests.get(url)
            vendor = res.text
        except requests.exceptions.HTTPError as e:
            print('Error in vendor lookup: {}'.format(e.strerror))
            vendor = 'Not available'
        known_vendors[vendor_mac] = vendor

    return vendor


def read_file(file, lookup_manufacturer):
    # Get the location name from the filename eg /x/y/z/benwhite.log -> benwhite
    filename = os.path.basename(file.name)
    location = filename[:filename.find('.')]

    indata = file.readlines()
    outdata = []

    for line in indata:
        mac, epoch = line.split()
        epoch = float(epoch)
        timestamp = time.localtime(epoch)

        if lookup_manufacturer:
            manufacturer = get_mac_manufacturer(mac)
        else:
            manufacturer = 'Not available'
        outdata.append({'location': location, 'mac': anonymize(mac), 'timestamp': timestamp, 'epoch': epoch,
                        'manufacturer': manufacturer})

    return outdata


def write_debug_json(directory, filename, data):
    if directory is not None and os.path.exists(directory) and os.path.isdir(directory):
        with open(os.path.join(directory, filename), 'w') as outfile:
            json.dump(data, outfile)


def read_all_files(directory, lookup_manufacturer):
    alldata = []
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            with open(os.path.join(directory, filename), 'r') as file:
                alldata = alldata + read_file(file, lookup_manufacturer)
            continue
        else:
            continue
    return alldata


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument('directory', help='input data directory')
    parser.add_argument('--debug_directory', help='debug output data directory')
    parser.add_argument('--user', help='socrata user')
    parser.add_argument('--password', help='socrata password')
    parser.add_argument('--manufacturer', action='store_true', help='lookup manufacturers (warning, this is SLOW)')
    args = parser.parse_args()

    creds = {'user': args.user, 'password': args.password}

    if os.path.exists(args.directory) and os.path.isdir(args.directory):
        alldata = read_all_files(args.directory, args.manufacturer)

        raw_data = generate_raw_dataset(alldata)
        write_debug_json(args.debug_directory, 'raw.json', raw_data)
        result = upsert_data(creds, raw_data, 'eitg-njyb')
        if result:
            print(result)

        if args.manufacturer:
            print('unique vendors: {} cached: {}'.format(len(known_vendors)-1, known_vendors['cached']))

        aggregate_data(alldata)

        # TODO Add other processing here
    else:
        print("{} is not a directory or does not exist".format(args.directory))

if __name__ == "__main__":
    main()
