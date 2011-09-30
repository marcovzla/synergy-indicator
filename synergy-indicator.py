#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Marco Antonio Valenzuela Escárcega
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import glob
import signal
import socket
import subprocess

import gtk
import appindicator


ICON_FILE = '/usr/share/icons/synergy-indicator.png'
PROFILES_DIR = os.path.expanduser('~/.synergy-indicator')


class SynergyIndicator(object):
    def __init__(self):
        self.conf = None
        self.server_running = False
        self.client_running = False
        
        self.indicator = appindicator.Indicator(
            'synergy-indicator', ICON_FILE,
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_attention_icon('indicator-messages-new')
        
        # display the hostname
        # it may be useful when configuring the clients
        hostname_status = gtk.MenuItem('Hostname: %s' % socket.gethostname())
        hostname_status.set_sensitive(False)

        # display the profile currently in use
        # or nothing if the default configuration is in use (~/.synergy.conf)
        self.profile_status = gtk.MenuItem()
        self.profile_status.set_sensitive(False)

        # display if the server is running
        self.server_status = gtk.MenuItem('Server is running')
        self.server_status.set_sensitive(False)

        # menuitem to start and stop the server
        self.server_item = gtk.MenuItem('Start Synergy Server')
        self.server_item.connect('activate', self.toggle_server)

        # submenu of profiles
        self.profiles_item = gtk.MenuItem('Profiles')
        submenu = gtk.Menu()
        # default means no profile in use
        default = gtk.RadioMenuItem(label='default')
        default.set_active(True)
        default.connect('activate', self.select_profile)
        submenu.append(default)
        submenu.append(gtk.SeparatorMenuItem())
        # include all profiles from PROFILES_DIR
        for p in glob.glob(os.path.join(PROFILES_DIR, '*.conf')):
            name = os.path.splitext(os.path.basename(p))[0]
            item = gtk.RadioMenuItem(group=default, label=name)
            item.connect('activate', self.select_profile)
            submenu.append(item)
        self.profiles_item.set_submenu(submenu)

        # menuitem to quit
        quit_item = gtk.MenuItem('Quit')
        quit_item.connect('activate', self.quit)

        # build menu
        menu = gtk.Menu()
        menu.append(hostname_status)
        menu.append(self.profile_status)
        menu.append(self.server_status)
        menu.append(gtk.SeparatorMenuItem())
        menu.append(self.server_item)
        menu.append(gtk.SeparatorMenuItem())
        menu.append(self.profiles_item)
        menu.append(gtk.SeparatorMenuItem())
        menu.append(quit_item)
        menu.show_all()

        # hide profile and server status
        self.profile_status.hide()
        self.server_status.hide()

        self.indicator.set_menu(menu)

    def main(self):
        gtk.main()

    def start_server(self):
        args = ['synergys']
        if self.conf:
            args += ['-c', self.conf]
        subprocess.call(args)
        self.server_running = True
        self.server_status.show()
        self.server_item.set_label('Stop Synergy Server')
        
    def stop_server(self):
        kill('synergys')
        self.server_running = False
        self.server_status.hide()
        self.server_item.set_label('Start Synergy Server')

    def restart_server(self):
        if self.server_running:
            self.stop_server()
            self.start_server()

    def select_profile(self, widget):
        self.conf = None
        for m in widget.get_group():
            label = m.get_label()
            if m.active and label != 'default':
                self.conf = os.path.join(PROFILES_DIR, '%s.conf' % label)
                self.restart_server()
                self.profile_status.set_label('Profile: %s' % label)
                self.profile_status.show()
                return
        self.profile_status.hide()
            
    def toggle_server(self, widget):
        if self.server_running:
            self.stop_server()
        else:
            self.start_server()

    def quit(self, widget):
        self.stop_server()
        gtk.main_quit()



def kill(pattern):
    """Kill processes matched by ``pattern``."""
    return subprocess.call(['pkill', '-9', pattern])



if __name__ == '__main__':
    indicator = SynergyIndicator()
    indicator.main()
