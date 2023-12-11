#made by Alyce Osbourne (https://github.com/AlyceOsbourne)

from tkinter import *
from tkinter import ttk
import subprocess
import sys

class Launcher(Tk):
    def __init__(self, app_path):
        super().__init__()
        self.title("Launcher")
        self.geometry("400x200")
        self.resizable(True, True)
        self.overrideredirect(True)        
        self.launch_button = ttk.Button(self, text="Launch", command=self.launch_app)
        self.launch_button.pack(side=TOP, pady=10)
        self.close_button = ttk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(side=BOTTOM, pady=10)
        self.app_path = app_path
        self.update()
        self.geometry("+%d+%d" % (self.winfo_screenwidth()/2 - self.winfo_width()/2,
                                  self.winfo_screenheight()/2 - self.winfo_height()/2))

    def launch_app(self):
        subprocess.Popen([sys.executable, self.app_path])
        self.destroy()

    def check_updates(self):
        pass
    
    def mainloop(self, n: int = 0) -> None:
        self.check_updates()
        super().mainloop(n)


if __name__ == "__main__":
    app = Launcher("GamePlusEditor/Main.py")
    app.mainloop()
