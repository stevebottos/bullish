import subprocess
import os

import wmi
import click


@click.command()
def start():
    _path = os.path.dirname(os.path.relpath(__file__))
    script_path = os.path.join("util", "alerts_process.py")
    full_script_path = os.path.join(_path, script_path)
    subprocess.Popen(f"python {full_script_path} {os.getpid()}", shell=True)


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

        if process.CommandLine and "alerts_subprocess.py" in process.CommandLine:
            print("alert process is currently running")
            return
        
    print("alert subprocess is not running")




