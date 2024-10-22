#!/usr/bin/python3

import sys
import signal


def print_msg(dict_sc, total_file_size):
    """
    Method to print metrics
    Args:
        dict_sc: dict of status codes
        total_file_size: total of the file sizes
    """
    print("File size: {}".format(total_file_size))
    for key, val in sorted(dict_sc.items()):
        if val > 0:
            print("{}: {}".format(key, val))


def signal_handler(sig, frame):
    """Handles keyboard interrupt (CTRL + C) and prints the results"""
    print_msg(dict_sc, total_file_size)
    sys.exit(0)


# Initialize variables
total_file_size = 0
counter = 0
dict_sc = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}

# Register signal handler for CTRL + C
signal.signal(signal.SIGINT, signal_handler)

try:
    # Process stdin line by line
    for line in sys.stdin:
        try:
            # Parse the line
            parsed_line = line.split()
            file_size = int(parsed_line[-1])  # Last element: file size
            status_code = int(parsed_line[-2])  # Second-to-last element: status code

            # Update total file size
            total_file_size += file_size

            # Update status code count if valid
            if status_code in dict_sc:
                dict_sc[status_code] += 1

            # Increase the line counter
            counter += 1

            # Print stats every 10 lines
            if counter % 10 == 0:
                print_msg(dict_sc, total_file_size)

        except (ValueError, IndexError):
            # Skip line if parsing fails
            continue

finally:
    # Print remaining data when done or on keyboard interrupt
    print_msg(dict_sc, total_file_size)
