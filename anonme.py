#!/usr/bin/python3

from optparse import OptionParser
import socket
import http.client as httplib
import urllib.parse as urlparse
import socks
import random
import time
import os
import sys


user_agents = [
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; )',
'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.8.1.18) Gecko/20081029 Firefox/2.0.0.18',
'Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.00',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.26.2 (KHTML, like Gecko) Version/3.2 Safari/525.26.12',
'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Avant Browser; Avant Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
'Opera/9.51 (Macintosh; Intel Mac OS X; U; en)',
'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.2.1; MultiZilla v1.1.32 final) Gecko/20021130',
]

TOR_SERVER = "127.0.0.1"
TOR_PORT = 9050

headers = {
'Accept' : '*/*',
}

def load_configs():
    parser = OptionParser()
    parser.add_option("-r", "--referrer", action="store", dest="referrer",
                      type="string", help="use this Referrer")
    parser.add_option("-u", "--useragent", action="store", dest="useragent", 
                      type="string", help="use this User Agent")
    parser.add_option("-c", "--connect", action="store", dest="site", 
                      type="string", help="Connection string i.e. www.x.org/b.txt)")                      
    parser.add_option("-z", "--randomize", action="store_true",
                      dest="random", default=False,
                      help="Choose a random User Agent")
    
    (opts, args) = parser.parse_args()
    
    if opts.site == None:
        parser.print_help()
        parser.error("You must supply a connection string!")
        
    if opts.referrer != None:
        headers['Referrer'] = opts.referrer
        
    if opts.useragent != None:
        headers['User-Agent'] = opts.useragent
    elif opts.random:
        random.seed(time.time())
        headers['User-Agent'] = random.choice(user_agents)
    else:
        headers['User-Agent'] = user_agents[0]
    
    return opts


def persist_file(url, data):
    outfile = url.hostname + os.sep + os.path.basename(opts.site)
    
    if not os.path.isdir(url.hostname):
        os.mkdir(url.hostname)
       
    FILE = open(outfile, "wb")
    FILE.write(data)
    FILE.close()
    
    print(f"[!] Persisted {len(data)} bytes to {outfile}  [!]")


def establish_tor_socks():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, TOR_SERVER, TOR_PORT)
    socket.socket = socks.socksocket
    

def main():
    opts = load_configs()
    
    #Set TOR as default
    establish_tor_socks()
   
    if not opts.site.lower().startswith('http://'):
        opts.site = 'http://' + opts.site
        
    url = urlparse.urlsplit(opts.site)
        
    print("Hostname: %s" % (url.hostname))
    print("Path: %s" % (url.path))
    print("Headers: %s" % (headers))
    
    try:
        conn = httplib.HTTPConnection(url.hostname)
        conn.request('GET', url.path, None, headers)
        data = conn.getresponse().read()

    except:
        print("[*] Failed to connect. Are you connected to the internet? [*]")
        print("[!] Terminating anonme.. [!]")
        sys.exit()
    
    if len(data) == 0:
        print ("[!] Response with zero bytes. You may have to try again later... [!]")
        print("[!] Terminating anonme... [!]")
        sys.exit()

    persist_file(url, data)

if __name__ == '__main__':
    main()
