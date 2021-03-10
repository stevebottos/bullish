import time
from datetime import datetime
import os
import argparse 

import bullish 

def write_information():
    with open("C:/Users/HP/_projects/bullish/test.txt", "a+") as f:
            f.write(f"{time.time()}")

def start_process(parent_process_pid):
    with open("C:/Users/HP/_projects/bullish/pid.txt", "w+") as f:
        f.write(str(parent_process_pid)+","+str(os.getpid()))

    while True:
        if datetime.now().hour == 23:
            write_information()
            seconds = 24 * 3600  # Just sleep until next midnight
            time.sleep(seconds)

        time.sleep(60*10)  # For the first time this is called

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('parent')
    args = parser.parse_args()
    start_process(args.parent)
