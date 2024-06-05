#! /var/ossec/framework/python/bin/python3

from socket import socket, AF_UNIX, SOCK_STREAM
from struct import pack, unpack
from json import dumps, loads
from json.decoder import JSONDecodeError
from pathlib import Path
import os, datetime

db_folder = '/var/ossec/queue/db/'

def db_query(agent, query):
    WDB = '/var/ossec/queue/db/wdb'

    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.connect(WDB)

    msg = 'agent {0} sql {1}'.format(agent, query).encode()
    sock.send(pack("<I{0}s".format(len(msg)), len(msg), msg))

    length = unpack("<I", sock.recv(4))[0]
    return sock.recv(length).decode(errors='ignore')

def pretty(response):
    if response.startswith('ok '):
        try:
            data = loads(response[3:])
            return dumps(data, indent=4)
        except JSONDecodeError:
            return response[3:]
    else:
        return response

if __name__ == "__main__":

    log_file.write(f'{datetime.datetime.now()} - sca_db_cleaner: [INFO] SCA DB cleaner script started.{filename}\n')
    db_files = [pos_db for pos_db in os.listdir(db_folder) if pos_db.endswith('.db') and pos_db != 'global.db' and pos_db != '.template.db' and pos_db != '000.db']
    logfile = '/var/ossec/logs/sca_db_cleaner.log'
    for filename in db_files:
        print("Cleaning SCA last scans of AgentID: " + filename[0:len(filename)-3])
        response1 = db_query(filename[0:len(filename)-3], "DELETE FROM sca_scan_info;")
        response2 = db_query(filename[0:len(filename)-3], "DELETE FROM sca_check;")
        if Path(logfile).is_file():
            log_file = open(logfile, "a+")
        else:
            log_file = open(logfile, "w")
        if pretty(response1) == '[]':
            log_file.write(f'{datetime.datetime.now()} - sca_db_cleaner: [INFO] First sca table cleaned! Agent\'s file: {filename}\n')
        else:
            log_file.write(f'{datetime.datetime.now()} - sca_db_cleaner: [ERROR] Something went wrong! {response1} Agent\'s file: {filename}\n')
        if pretty(response2) == '[]':
            log_file.write(f'{datetime.datetime.now()} - sca_db_cleaner: [INFO] Second sca table cleaned! Agent\'s file: {filename}\n')
        else:
            log_file.write(f'{datetime.datetime.now()} - vd_db_cleaner: [ERROR] Something went wrong with the second table! {response2} Agent\'s file: {filename}\n')

