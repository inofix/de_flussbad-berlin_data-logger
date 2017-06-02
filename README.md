# de_flussbad-berlin_data-logger

Recieve sensor data in XML format from a data logger device deployed
on site. The data logger sends its data periodically over the mobile
network to a server using HTTPS-POST.

## Installation

* Read the script, it is only 40 lines of code..
* Rename the script if needed, set htaccess/credentials, etc...
* Copy the python script to the CGI-directory of your webserver.
* Configure the storage_path to point to a directory writeable to the webserver- (or CGI-)user.
