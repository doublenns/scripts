#!/usr/bin/env python3

import boto3
import json
import datetime
import sys
import os
import errno


# To-do:
# 1) Check to make sure aws api keys are configured prior to beginning script
# 2) Start using setup_args to determine file location
# 3) Archive old backups into compressed tarballs instead of txt files
#   * Use logrotate? Get rid of manually adding time-stamps to files??
# 4) Have option to display in either JSON or CSV (chart)
# 5) Ability to download older files
# 6) Prune older files
#   * More than 60 days, maybe only keep weekly backups


# Parsed args aren't used yet.
def setup_args():
    '''
    Funtion builds parsing object to pass to main function.
    '''
    parser = argparse.ArgumentParser()
    home = os.path.expanduser('~')
    backup_dir = home + "/route53-backup"

    parser.add_argument("-d", "--dir", "--directory", type=str.lower,
                        default=backup_dir,
                        help="Provide the directory where the output files of this script will be saved")
    return parser


def build_json_obj(json_string):
    '''
    Function to build JSON objects from AWS API output
    '''
    json_dump = json.dumps(json_string)
    json_obj = json.loads(json_dump)
    return json_obj


def mkdir_p(path):
    '''
    Function to mimic  POSIX `mkdir -p` functionality
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def backup_route53(today, json_record_dir, json_zone_dir):
    '''
    Function that does the actual backing up of Route53 state
    '''

    # Build connection to account's Route53 service
    route53 = boto3.client("route53")
    # Grab list of all the Hosted Zones and create JSON object
    hosted_zones_list = route53.list_hosted_zones()
    hosted_zones = hosted_zones_list["HostedZones"]

    while True:
        if hosted_zones_list["IsTruncated"]:
            next_marker = hosted_zones_list["NextMarker"]
            hosted_zones_list = route53.list_hosted_zones(Marker=next_marker)
            hosted_zones = hosted_zones + hosted_zones_list["HostedZones"]
        else:
            break

    hosted_zones_json = build_json_obj(hosted_zones)
    # Dump all hosted zones info to file on disk in JSON format
    with open(json_zone_dir + "hosted_zones-" + today + ".txt", "w") as hz_file:
        json.dump(hosted_zones_json, hz_file, indent=4)

    # Dump all records of each hosted zone into separate files
    for hosted_zone in hosted_zones:
        name = hosted_zone["Name"]
        iden = hosted_zone["Id"]
        record_set = route53.list_resource_record_sets(HostedZoneId=iden)
        resource_records = record_set["ResourceRecordSets"]

        while True:
            if record_set["IsTruncated"]:
                next_record_name = record_set["NextRecordName"]
                next_record_type = record_set["NextRecordType"]
                record_set = route53.list_resource_record_sets(HostedZoneId=iden,
                                                                StartRecordName = next_record_name,
                                                                StartRecordType = next_record_type)
                resource_records = resource_records + record_set["ResourceRecordSets"]
            else:
                break

        with open(json_record_dir + name + today + ".txt", "w") as rs_file:
            json.dump(resource_records, rs_file, indent=4)


def main():
    '''
    Script's main function
    '''

    # Build directory structure for backup files to sit within
    # Date object in form of yyyy-mm-dd, converted to string so can append to file names
    today = str(datetime.date.today())
    home = os.path.expanduser('~')
    backup_dir = home + "/route53-backup"
    json_record_dir = backup_dir + "/record_sets-" + today + "/json/"
    csv_record_dir = backup_dir + "/record_sets-" + today + "/csv/"
    json_zone_dir = backup_dir + "/hosted_zones" + "/json/"
    csv_zone_dir = backup_dir + "/hosted_zones" + "/csv/"
    for directory in json_record_dir, csv_record_dir, json_zone_dir, csv_zone_dir:
        mkdir_p(directory)


    backup_route53(today, json_record_dir, json_zone_dir)


if __name__ == "__main__":
    main()


sys.exit(0)

