"""
This script runs the RasaHost application using a development server.
"""

import os
current_dir = os.path.dirname(os.path.realpath(__file__))

from RasaHost import host
host.set_data_path(os.path.join(current_dir, "data"))

if __name__ == '__main__':    
    host.run()