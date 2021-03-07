import time
import os
import argparse 

import bullish 

def start_process(parent_process_pid):
    with open("C:/Users/HP/_projects/bullish/pid.txt", "w+") as f:
        f.write(str(parent_process_pid)+","+str(os.getpid()))

    for i in range(60):
        with open("C:/Users/HP/_projects/bullish/test.txt", "a+") as f:
            f.write(f"{os.getpid()}, {i}\n")
            time.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('parent')
    args = parser.parse_args()
    start_process(args.parent)
