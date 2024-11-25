import sys
import csv
import datetime

def main():
    if len(sys.argv) == 1:
        print("Error! - No Log File Specified!")
    try:
        #takes in CSV file without column headers (actual data starts on the first line
        file = open(sys.argv[1], "r")
    except:
        print("Error! - File Not Found!")
        return

    #known bad ports that computer communicates with
    bad_ports = {1337, 1338, 1339, 1340}
    # the IP addresses of the infected systems within the network
    infected_internal_ips = set()
    # IP addresses of the C2 servers the infected systems are communicating with as key and
    # total amount of data (in bytes) sent from internal systems to each of the malware C2 servers as value
    bad_c2_servers = {}
    #first connection
    first_time = -1

    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.reader(file)
        for row in reader:
            timestamp, srcip, dstip, srcport, dstport, bsent, brecv, btrans = row
            dstport = int(dstport)
            timestamp = int(timestamp)
            bsent = int(bsent)

            if dstport in bad_ports:
                if srcip not in infected_internal_ips:
                    infected_internal_ips.add(srcip)

                if dstip not in bad_c2_servers:
                    bad_c2_servers[dstip] = 0
                bad_c2_servers[dstip] += bsent

                if int(timestamp) < first_time or first_time == -1:
                    first_time = timestamp



    # name of source file
    print("Source File: " + sys.argv[1])
    #prints how many systems on the internal network are infected
    print(f"Systems Infected: {len(infected_internal_ips)}")
    # prints the IP addresses of the infected systems within the network
    infected_internal_ips = sorted(infected_internal_ips, key=lambda x: x[-3:])
    print(f"Infected System IPs: {infected_internal_ips}")
    print(f"C2 Servers: {len(bad_c2_servers)}")
    #sort the IP addresses of the C2 servers the infected systems are communicating with
    c2_servers = sorted(bad_c2_servers.keys())
    print(f"C2 Server IPs: {c2_servers}")
    # convert standard epoch value to Y:M:D H:M:S format
    first_time = datetime.datetime.fromtimestamp(first_time).strftime('%Y-%b-%d %H:%M:%S UTC')
    print(f"First C2 Connection: {first_time}")
    #sort C2 servers for formatting in num bytes sent descending order
    bad_c2_servers = sorted(bad_c2_servers.items(), key=lambda x: x[1], reverse=True)
    print(f"C2 Data Totals: {bad_c2_servers}")






if __name__ == "__main__":
    main()