#!/usr/bin/env python

import subprocess
import sys

def install_requirements():
    print("Installing required packages...")
    requirements = [
        "Django==5.2.3",
        "psycopg2-binary==2.9.9",
        "Pillow==10.1.0",
        "python-dateutil==2.8.2",
        "pytz==2024.1",
        "openpyxl==3.1.2"
    ]

    for req in requirements:
        print(f"Installing {req}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"Successfully installed {req}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")

    print("\nAll packages installed. You should now be able to use all features of the application.")

if __name__ == "__main__":
    install_requirements()
