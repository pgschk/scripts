#!/usr/bin/python
#
# Apache VHOST Setup Script
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

import os,sys

apache_confdir = "/etc/apache2/sites-available/"
skel_dir = "/var/www/skel/"

f = open('/etc/passwd','r')
for line in f:
    parts = line.split(':')
    wname = parts[0]
    wid = parts[2]

f.close

wid = int(wid)+1
wnameid = int(wname[1:])
wnameid = wnameid+1
wnameid = str(wnameid)

while len(wnameid) < 4:
    wnameid = "0"+wnameid

wname = "w"+wnameid

vname = str(raw_input("Please enter the domain name of the new virtual host: "))
vhostcfg = """
<VirtualHost *:80>
        ServerAdmin admins@blafaselblub.net
        ServerName %s
        ServerAlias www.%s

        SuexecUserGroup %s %s
        AddHandler fcgid-script .php .php3 .php4 .php5 .php6 .phtml .phps

        DocumentRoot /var/www/%s/htdocs/
        <Directory />
                Options FollowSymLinks
                AllowOverride None
        </Directory>
        <Directory /var/www/%s/htdocs/>
                Options Indexes FollowSymLinks MultiViews +ExecCGI
                AllowOverride None
                Order allow,deny
                allow from all
                 FCGIWrapper /var/www/_fcgid/%s/php5-fcgi-starter .php
                 FCGIWrapper /var/www/_fcgid/%s/php5-fcgi-starter .php5
                 FCGIWrapper /var/www/_fcgid/%s/php5-fcgi-starter .phtml
                 FCGIWrapper /var/www/_fcgid/%s/php5-fcgi-starter .phps
        </Directory>

        ErrorLog /var/www/%s/log/error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog /var/www/%s/log/access.log combined
</VirtualHost>
""" % (vname,vname,wname,wname,wname,wname,wname,wname,wname,wname,wname,wname)

f = open("/var/www/_fcgid/php.ini.part1.tpl","r")
phpini = f.read()
phpini = phpini % (wname,wname)
f.close()

f = open("/var/www/_fcgid/php.ini.part2.tpl","r")
phpini2 = f.read()
phpini = phpini + phpini2
f.close()

f = open("/var/www/_fcgid/php5-fcgi-starter.tpl","r")
phpstarter = f.read()
phpstarter = phpstarter % wname
f.close()


f = open(apache_confdir + wname, "w")
f.write(vhostcfg)
f.close

vhostdir = "/var/www/" + wname
wconfdir = "/var/www/_fcgid/" + wname
os.system("mkdir -p " + wconfdir)

os.system("touch " + wconfdir + "/php.ini")
f = open(wconfdir + "/php.ini","w")
f.write(phpini)
f.close()

os.system("touch " + wconfdir + "/php5-fcgi-starter")
f = open(wconfdir + "/php5-fcgi-starter","w")
f.write(phpstarter)
f.close()


os.system("mkdir -p " + vhostdir + "/htdocs/")
os.system("mkdir -p " + vhostdir + "/tmp/")
os.system("mkdir -p " + vhostdir + "/log/")
os.system("addgroup --gid " + str(wid) + " " + wname)
os.system("adduser --disabled-login --uid=" + str(wid) + " --no-create-home --home=/var/www/" + wname + "/ --ingroup " + wname + " --gecos " + wname + " " + wname)
os.system("ln -s " + vhostdir + " /var/www/" + vname)
os.system("cp -R " + skel_dir + "* " + vhostdir + "/htdocs/")
os.system("chown " + wname + "." + wname + " -R " + vhostdir)
os.system("chown " + wname + "." + wname + " -R " + wconfdir)
os.system("chmod 0755 " + wconfdir + "/php5-fcgi-starter")
os.system("chmod 0755 -R " + vhostdir)
os.system("a2ensite " + wname)
os.system("invoke-rc.d apache2 reload")


