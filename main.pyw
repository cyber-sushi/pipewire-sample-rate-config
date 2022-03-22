#!/usr/bin/env python

import tkinter as tk
from shutil import copyfile
from os import remove, rename, mkdir
from os.path import isfile, expanduser


class File(object):
    def __init__(self):
        self.user = expanduser('~')
        self.FILE = f"{self.user}/.config/pipewire/pipewire.conf"
        self.SAMPLE_RATES = (44100, 48000, 88200, 96000)
        self.current = None
        self.error = False
        self.check()
        self.window = Window(self)
        self.window.mainloop()

    def check(self):
        if not isfile(self.FILE):
            try:
                mkdir(f"{self.user}/.config/pipewire")
            except FileExistsError:
                pass
            pipewire_etc = "/etc/pipewire/pipewire.conf"
            pipewire_usr = "/usr/share/pipewire/pipewire.conf"
            if isfile(pipewire_etc):
                copyfile(pipewire_etc, self.FILE)
                self.remove_hash()
            elif isfile(pipewire_usr):
                copyfile(pipewire_usr, self.FILE)
                self.remove_hash()
            else:
                self.error = True

    def read(self):
        with open(self.FILE, "r") as file:
            lines_list = file.read().splitlines()
            for line in lines_list:
                if "default.clock.rate" in line.split(" "):
                    return int(line.split(" ")[-1])

    def change(self, value):
        with open(self.FILE, "r") as file:
            lines_list = file.read().splitlines()
            for line in lines_list:
                split_line = line.split(" ")
                if "default.clock.rate" in split_line:
                    new_file = open(f"{self.user}/.config/pipewire/pipewire.conf.tmp", "a")
                    for i in range(len(lines_list)):
                        new_line = lines_list[i]
                        if "default.clock.rate" in new_line.split(" "):
                            new_line = f"     default.clock.rate          = {value}"
                        new_file.write(new_line + "\n")
                    new_file.close()
                    remove(self.FILE)
                    rename(f"{self.user}/.config/pipewire/pipewire.conf.tmp", self.FILE)
        self.window.change_message(f"Current sample rate:\n{self.read()}")

    def remove_hash(self):
        with open(self.FILE, "r") as file:
            lines_list = file.read().splitlines()
            for line in lines_list:
                split_line = line.split(" ")
                if "default.clock.rate" in split_line:
                    break
                elif "#default.clock.rate" in split_line:
                    new_file = open(f"{self.user}/.config/pipewire/pipewire.conf.tmp", "a")
                    for i in range(len(lines_list)):
                        new_line = lines_list[i]
                        if new_line == "    #default.clock.rate          = 48000":
                            new_line = "     default.clock.rate          = 48000"
                        new_file.write(new_line + "\n")
                    new_file.close()
                    remove(self.FILE)
                    rename(f"{self.user}/.config/pipewire/pipewire.conf.tmp", self.FILE)


class Window(tk.Tk):
    def __init__(self, file):
        tk.Tk.__init__(self)

        self.title("Pipewire Sample Rate Settings")
        self.geometry("420x200")
        self["bg"] = "#2E3440"
        self.resizable(False, False)

        self.message = tk.Label(master=self, text=f"Current sample rate:\n{file.read()}", fg="#ECEFF4", bg="#2E3440")
        self.message.pack(side=tk.TOP, pady=30)
        self.layout = tk.Frame(master=self, bg="#2E3440")
        self.layout.pack(side=tk.BOTTOM, pady=30)
        for i in file.SAMPLE_RATES:
            button = tk.Button(master=self.layout, text=str(i), fg="#ECEFF4", bg="#2E3440", cursor="hand2",
                               command=lambda x=i: file.change(x))
            if file.error is True:
                button.config(state="disabled")
            button.pack(side=tk.LEFT, padx=10)
        if file.error is True:
            self.change_message("No Pipewire config file found in your system.")

    def change_message(self, message):
        self.message.config(text=message)
        self.update()


if __name__ == "__main__":
    app = File()
