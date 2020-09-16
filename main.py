import socket
import time
from dns.exception import DNSException
import dns.resolver
from retry import retry

resolver = dns.resolver.Resolver()
resolver.timeout = 1
resolver.lifetime = 1

hostnames = ['www.google.com', 'serverless.com', 'paraiba.cloud.apisuite.io', 'parazinho.cloud.apisuie.io']


def check_hostnames():
    for hostname in hostnames:
        try:
            print("Trying to resolve {hostname}....".format(hostname=hostname))
            if check_hostname(hostname):
                print("{hostname} was found".format(hostname=hostname))
            else:
                print("{hostname} not published yet".format(hostname=hostname))
        except socket.error:
            print("Exiting...")
            return False
    return True


@retry(socket.error, tries=3, delay=2)
def check_hostname(hostname):
    time_limit = 600
    start = time.time()
    while time.time() - start < time_limit:
        try:
            socket.gethostbyname(hostname)
            return True
        except socket.error:
            raise


@retry(DNSException, tries=3, delay=2)
def check_hostname_with_resolver(hostname):
    try:
        resolver.resolve(hostname, 'A')
        return True
    except DNSException:
        raise


def check_hostnames_with_resolver():
    for hostname in hostnames:
        try:
            print("Trying to resolve {hostname}....".format(hostname=hostname))
            if check_hostname_with_resolver(hostname):
                print("{hostname} was found".format(hostname=hostname))
            else:
                print("{hostname} not published yet".format(hostname=hostname))
        except DNSException:
            print("Exiting...")
            return False
    return True


if __name__ == '__main__':
    check_hostnames()
