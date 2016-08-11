# -*- coding: utf-8 -*-

import json
import logging
import threading
import urllib.parse
from gi.repository import GObject, Peas
from os import stat, makedirs, remove, listdir
from dateutil.parser import parse
from os.path import exists, join
from datetime import datetime
from time import time


class StarterPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'LastMoment'

    object = GObject.property (type = GObject.Object)

    def __init__ (self):
        GObject.Object.__init__ (self)
        # logging.basicConfig(level=logging.DEBUG)

    def do_deactivate (self):
        self._totem = None
        logging.info("Last-Moment disabled")

    def do_activate (self):
        self._totem = self.object

        self._totem.connect('file-closed', self.file_closed)
        self._totem.get_main_window().connect('destroy', self.file_closed)
        self._totem.connect('file-has-played', self.file_played)
        self._totem.connect('file-opened', self.file_opened)

        folder = self.plugin_info.get_data_dir() + "/savedTimes"

        if not exists(folder):
            makedirs(folder)
        else:
            self.check_last_clean()

        logging.info("Last-Moment enabled")

    def file_closed(self, to):
        self.t.cancel()

    def file_opened(self, to, path):
        threading.Timer(0.5, self.restore_time).start()

    def file_played(self, to, path):
        threading.Timer(5, self.set_interval(self.save_time, 3))

    def save_time(self):
        # Saves a json file with the inode number and time
        data = {}
        data['time'] = self.get_time()

        id = self.get_inode()
        file = self.plugin_info.get_data_dir() + "/savedTimes/" + str(id) + ".json"

        with open(file, 'w') as outfile:
            json.dump(data, outfile)
            logging.info("Saved time " + str(data['time']))

    def restore_time(self):
        ## Finds if a vide have a time file and restores it
        id = self.get_inode()
        file = self.plugin_info.get_data_dir() + "/savedTimes/" + str(id) + ".json"

        if (exists(file)):

            with open(file) as data_file:
                data = json.load(data_file)
                self.set_time(data['time'])
                logging.info("Restoring to " + str(data['time']))
                return True
        else:
            logging.info("No file found")
            return False

    def get_time(self):
        if (self._totem.get_property('seekable')):
            return self._totem.get_property('current-time')
        else:
            return False

    def set_time(self, time):
        if (self._totem.get_property('seekable')):
            logging.info("Go to " + str(time))
            self._totem.seek_time(time, False)
        else:
            return False

    def get_inode(self):
        url = self._totem.get_property('current-mrl')
        url = url.replace("file://", "")
        url = urllib.parse.unquote(url)
        return stat(url).st_ino

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()

        self.t = threading.Timer(sec, func_wrapper)
        self.t.start()
        return self.t

    def check_last_clean(self):
        # Checks if is time to delete older files
        file = self.plugin_info.get_data_dir() + "/lastCheck.json"

        if (exists(file)):

            with open(file) as data_file:
                data = json.load(data_file)
                lastCheck = data['lastCheck']
                logging.info("Last check " + lastCheck)

                today = datetime.now()
                if ((today-parse(lastCheck)).days) > 15:
                    self.clean_old()
                    self.set_last_clean()

                return True
        else:
            logging.info("Thre is not lastCheck.json file")
            self.set_last_clean()
            return False

    def set_last_clean(self):
        # Creates a file with the last delete check
        data = {}
        data['lastCheck'] = str(datetime.now())

        file = self.plugin_info.get_data_dir() + "/lastCheck.json"

        with open(file, 'w') as outfile:
            json.dump(data, outfile)
            logging.info("Saving last check time")

    def clean_old(self):
        # Erase older files than 30 days
        path = self.plugin_info.get_data_dir() + "/savedTimes/"

        for f in listdir(path):
            if (stat(join(path,f)).st_mtime < time() - (30 * 86400)):
                logging.info("Removing " + f)
                remove(join(path, f))
