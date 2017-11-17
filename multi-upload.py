#!/usr/bin/python
########################################################################
#
# upload.py:
# A simple script for the data-logger..
# TODO: This is a test implementation, for a stable version we
# need some solution for the pip installed lib, data input verification,
# header checks, and it would be nice to also support direct (form-less)
# uploads for our other sources.
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
import json
import re

# debug {{ #
#import cgitb
#cgitb.enable(display=0, logdir="/tmp/")
# debug }} #

def recalculate_akut(in_file_name):
    from openpyxl import load_workbook
    try:
        # get the data from file (no direct method found..)
        wb_in = load_workbook(in_file_name)

        # grab the active worksheet
        ws_in = wb_in.active

        measurements = []

        # the actual measurements start only here
        # as the information is hardcoded anyway, no need to
        # make anything configurable..
        for i in range(6, ws_in.max_row):

            measurement = {}

            measurement["analyse"] = ws_in.cell(row=i, column=1).value
            measurement["location"] = ws_in.cell(row=i, column=2).value
            measurement["lat"] = ws_in.cell(row=i, column=3).value
            measurement["long"] = ws_in.cell(row=i, column=4).value
            measurement["author"] = ws_in.cell(row=i, column=5).value
            measurement["timestamp"] = ws_in.cell(row=i, column=6).value

            for j in range(8, ws_in.max_column):

                vid = ws_in.cell(row=2, column=j).value
                if vid is not None:
                    measurement["id"] = vid
                    measurement["method"] = ws_in.cell(row=3, column=j).value
                    measurement["name"] = ws_in.cell(row=4, column=j).value
                    measurement["unit"] = ws_in.cell(row=5, column=j).value
                    measurement["value"] = ws_in.cell(row=i, column=j).value

                    measurements.append(measurement)

        # convert to json and just print
        return measurements

    except Exception:
        import traceback
        print(traceback.format_exc())

def store(storage_path, file_prefix='test', do_archive=False):
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

    data_file = storage_path + "/" + file_prefix + ".json"

    response = 'Content-Type: text/plain\n\n' + timestamp + '\n'

    try:
        data = cgi.FieldStorage()
        if data.has_key('filetype') and data.has_key('file'):

            if data['filetype'].value == 'xlsx_akut':
                tmp_file_name = storage_path + '/tmp.xlsx'
                with open(tmp_file_name, 'w') as of:
                    of.write(data['file'].value)
                m = recalculate_akut(tmp_file_name)
                with open(data_file, 'w') as of:
                    of.write(json.dumps(m))

#        file_content = data.value.__repr__()
#        json_content = json.loads(file_content)
#        output_content = json.dumps(json_content)
#        with open(data_file, "w") as of:
#            of.write(str(output_content))
        print response
    except:
        response += 'Please, try again!\n'
        print response

if __name__ == "__main__":

    store("/tmp/")

