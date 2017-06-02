#!/usr/bin/python
########################################################################
#
# upload.py:
# A simple script for the data-logger..
#
########################################################################
#
#  This is Free Software; feel free to redistribute and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  Copyright 2017, Michael Lustenberger <mic@inofix.ch>
#
########################################################################

import os
import cgi
import datetime
import re

# remove try/catch for debugging..
# debug {{ #
#import cgitb
#cgitb.enable(display=0, logdir="/tmp/")
# debug }} #

def store(storage_path, do_archive):
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

    data_file = storage_path + "sensor-data-latest.xml"
    data_archive = storage_path + "sensor-data-" + timestamp + ".xml"

    response = 'Content-Type: application/xml;charset=iso-8859-1\n\n' + \
            '<?xml version="1.0" encoding="iso-8859-1"?>\n' + \
            '<Response responseTime="' + timestamp + '" hascmds="false">\n'

    data = cgi.FieldStorage()
    try:
        file_content = data.value.__repr__()
        file_content = file_content.strip("'")
        file_content = file_content.strip('"')
        file_content = re.sub("\\\\r", "", file_content)
        file_content = re.sub("\\\\n", "\n", file_content)
        with open(data_file, "w") as of:
            of.write(file_content)
        if do_archive:
            with open(data_archive, "w") as of:
            of.write(file_content)
        response += ' <Ack status="OK"></Ack>\n' + '</Response>\n'
        print response
    except:
        response += ' <Ack status="FAIL">Error</Ack>\n' + '</Response>\n'
        print response

if __name__ == "__main__":

    store("/tmp", False)

