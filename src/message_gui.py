import os
import sys
import subprocess
from pathlib import Path


MESSAGE_FILE_PATH = Path.cwd() / r'windows' / r'MessageBox.ps1'
IS_CLICKED = False

def handle_message_box():
    subprocess.run([f'./{MESSAGE_FILE_PATH}'])
    
if __name__ == "__main__":
    handle_message_box()