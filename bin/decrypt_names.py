#!/usr/bin/python
"""
This is a tool to decrypt file names in rclone logs.

Pass two files in, the first should be a crypt mapping generated by

rclone ls --crypt-show-mapping remote:path

The second should be a log file that you want the paths decrypted in.

Note that if the crypt mappings file is large it can take some time to
run.
"""

import re
import sys

# Crypt line
match_crypt = re.compile(r'NOTICE: (.*?): Encrypts to "(.*?)"$')

def read_crypt_map(mapping_file):
    """
    Read the crypt mapping file in, creating a dictionary of substitutions
    """
    mapping = {}
    with open(mapping_file) as fd:
        for line in fd:
            match = match_crypt.search(line)
            if match:
                plaintext, ciphertext = match.groups()
                plaintexts = plaintext.split("/")
                ciphertexts = ciphertext.split("/")
                for plain, cipher in zip(plaintexts, ciphertexts):
                    mapping[cipher] = plain
    return mapping

def map_log_file(crypt_map, log_file):
    """
    Substitute the crypt_map in the log file.

    This uses a straight forward O(N**2) algorithm.  I tried using
    regexps to speed it up but it made it slower!
    """
    with open(log_file) as fd:
        for line in fd:
            for cipher, plain in crypt_map.iteritems():
                line = line.replace(cipher, plain)
            sys.stdout.write(line)

def main():
    if len(sys.argv) < 3:
        print "Syntax: %s <crypt-mapping-file> <log-file>" % sys.argv[0]
        raise SystemExit(1)
    mapping_file, log_file = sys.argv[1:]
    crypt_map = read_crypt_map(mapping_file)
    map_log_file(crypt_map, log_file)

if __name__ == "__main__":
    main()
