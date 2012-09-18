#!/bin/bash
#
# Backup Script wrapper for duplicity and misc
#
# Copyright (c) 2011 Philipp Geschke
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
####################################


# add what you need
bdirs=( "/etc" "/root" )


dpkg --get-selections > /etc/dpkg-selections


date=`date +%d`
hostn=`hostname`

# duplicity encryption psk
PASSPHRASE=''
export PASSPHRASE

# FTP server password
FTP_PASSWORD=''
export FTP_PASSWORD

for bdir in "${bdirs[@]}"
do
    bdirlog=${bdir//\//\-}
    if [ $date = 14 ]; then
        duplicity full /$bdir ftp://<user@hostname>/$hostn/$bdir >>/var/log/duplicity-$hostn$bdirlog.log
        result=$?
    else
        duplicity incremental /$bdir ftp://<user@hostname>/$hostn/$bdir >>/var/log/duplicity-$hostn$bdirlog.log
        result=$?
    fi
    if [ ! $result -eq 0 ]; then
        mail root -s "Error on nightly backup job on `hostname --fqdn`" < /var/log/duplicity-$hostn$bdirlog.log
    fi
done

unset PASSPHRASE
unset FTP_PASSWORD

