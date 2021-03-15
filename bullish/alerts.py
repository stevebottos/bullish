import subprocess
import os
import sys 

import wmi
import click


@click.command()
def start():
    _path = os.path.dirname(os.path.relpath(__file__))
    script_path = os.path.join("util", "alerts_process.py")
    full_script_path = os.path.join(_path, script_path)

    # TODO: Figure out how to get the process to keep running until stopped on other os types
    if sys.platform == "win32":
        subprocess.Popen(f"pythonw {full_script_path} {os.getpid()}")
    else:
        print("Alerts supported for this OS type yet")


@click.command()
def stop():
    f = wmi.WMI()
    for process in f.Win32_Process():

        if process.CommandLine and "alerts_process.py" in process.CommandLine:
            process.Terminate()
            print("alerts_process.py terminated")    
            return
    

@click.command()
def check():
    print("checking...")
    f = wmi.WMI()
    for process in f.Win32_Process():

        if process.CommandLine and "alerts_process.py" in process.CommandLine:
            print("alert process is currently running")
            return
        
    print("alert subprocess is not running")




