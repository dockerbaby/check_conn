#!/usr/bin/env python
"""
check_conn -  https://github.com/dockerbaby/check_conn

A little application to check network connectivity to a host on a particular port.
"""

import sys
import socket
import logging
from argparse import ArgumentParser

def parse_args(argv):
    ####################################################################################
    # 
    #  parse_args - a function to parse command line arguments to check_conn.py
    #
    #  input:   list      - argument vector or list of arguments
    #  output:  Namespace - a dictionary of name-value pairs representing command line arguments 
    #

    parser = ArgumentParser(add_help=False)
    parser.add_argument('hostname', nargs='?', type=str)
    parser.add_argument("-p", "--port", nargs='?', dest="port")
    args, unknown = parser.parse_known_args(argv[1:])
    return args 

        
def check_conn(hostname, port):
    ####################################################################################
    #
    #  check_conn - a function to test network connectivity to a host and port combination
    #
    #  input:   hostname, port
    #  output:  int
    #

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    try:
        result = sock.connect_ex((hostname, int(port)))
        sock.shutdown(socket.SHUT_RDWR)
    except:
        result = 1
    finally:
        sock.close()

    return result


def main(argv):
    ####################################################################################
    #
    #  main - main function of check_conn.py;  takes an argument vector representing 
    #         command-line arguments and returns an integer indicating the result of 
    #         a network connection attempt, along with a text status message
    #
    #       Return codes:
    #           
    #            0 = Success (OK)
    #            1 = Failure (FAIL)
    #
    #  input:   argument vector or list
    #  output:  int (0,1), status message (OK, FAIL)
    #
     
    # Get args
    try:
        args = parse_args(argv)
        result = 0
    except:
        result = 1

    # Check connection
    if result == 0 and args.port is not None and args.hostname is not None and args.port.isdigit():
        try:
            result = check_conn(args.hostname,int(args.port))
        except:
            result = 1
    else:
        result = 1

    # Report
    if result == 0:
        print "OK"
    else:
        result = 1
        print "FAIL"

    return result
    
if __name__ == '__main__':
    sys.exit(main(sys.argv))
