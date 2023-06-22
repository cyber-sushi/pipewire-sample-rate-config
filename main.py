#!/usr/bin/env python

import tkinter as tk
import subprocess


class Application(object):
    def __init__(self):
        self.SAMPLE_RATES = (44100, 48000, 88200, 96000)
        self.BUFFER_SIZES = (32, 64, 128, 256, 512, 1024)
        self.window = Window(self)
        self.window.mainloop()

    def read(self, prop):
        setting = subprocess.check_output(f"pw-metadata -n settings 0 clock.force-{prop}", shell=True)
        value = setting.decode("UTF-8").split("value:'")[1].split("' type:")[0]
        return value

    def change(self, value, prop):
        subprocess.run(f"pw-metadata -n settings 0 clock.force-{prop} {value}", shell=True)
        if prop == "rate":
            self.window.message.config(text=f"Current sample rate: {self.read(prop)}")
        elif prop == "quantum":
            self.window.message2.config(text=f"Current buffer size: {self.read(prop)}")
        self.window.update()


class Window(tk.Tk):
    def __init__(self, file):
        super().__init__()

        self.title("Pipewire Sample Rate Settings")
        self.geometry("500x200")
        self["bg"] = "#2E3440"
        self.resizable(False, False)

        self.message = tk.Label(master=self, text=f"Current sample rate: {file.read('rate')}", fg="#ECEFF4", bg="#2E3440")
        self.message.pack(side=tk.TOP, pady=10)
        self.layout = tk.Frame(master=self, bg="#2E3440")
        self.layout.pack(side=tk.TOP, pady=10)
        for i in file.SAMPLE_RATES:
            button = tk.Button(master=self.layout, text=str(i), fg="#ECEFF4", bg="#2E3440", cursor="hand2", borderwidth=2, bd=2, relief=tk.RAISED, activebackground="#434C5E", activeforeground="#ECEFF4",
                               command=lambda x=i: file.change(x, "rate"))
            button.pack(side=tk.LEFT, padx=10)
        self.message2 = tk.Label(master=self, text=f"Current buffer size: {file.read('quantum')}", fg="#ECEFF4", bg="#2E3440")
        self.message2.pack(side=tk.TOP, pady=10)
        self.layout2 = tk.Frame(master=self, bg="#2E3440")
        self.layout2.pack(side=tk.TOP, pady=10)
        for i in file.BUFFER_SIZES:
            button = tk.Button(master=self.layout2, text=str(i), fg="#ECEFF4", bg="#2E3440", cursor="hand2", borderwidth=2, bd=2, relief=tk.RAISED, activebackground="#434C5E", activeforeground="#ECEFF4",
                               command=lambda x=i: file.change(x, "quantum"))
            button.pack(side=tk.LEFT, padx=10)


if __name__ == "__main__":
    app = Application()
