# SFLvault - Secure networked password store and credentials manager.
#
# Copyright (C) 2016 Savoir-faire Linux inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import logging.config

from . import SFLvaultServer

def main():
    parser = argparse.ArgumentParser(description="Launch the SFLVault server")
    parser.add_argument('config_file', nargs='?', default=None, help="INI config file")
    args = parser.parse_args()
    if args.config_file:
        logging.config.fileConfig(args.config_file)
    server = SFLvaultServer(args.config_file)
    server.start_server()

if __name__ == '__main__':
    main()
