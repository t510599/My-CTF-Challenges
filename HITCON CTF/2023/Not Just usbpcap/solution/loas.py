import sys

import tqdm
import scapy.utils

LOAS_SYNC = 0x2b7
LATM_HEADER = b"\x47\xfc\x00\x00"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: loas.py <pcap> <loas>")
        exit(1)

    pkts = scapy.utils.rdpcap(sys.argv[1])

    with open(sys.argv[2], "wb") as f:
        for i, pkt in tqdm.tqdm(enumerate(pkts), total=len(pkts)):
            data = bytes(pkt)
            payload = data[data.index(LATM_HEADER):]

            # append loas_header for each aac-latm frame
            loas_header = (LOAS_SYNC << 13) + (len(payload) & 0x1fff)
            f.write(loas_header.to_bytes(3, 'big'))
            f.write(payload)