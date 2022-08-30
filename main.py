import tkinter as tk
from tkinter import ttk, PhotoImage
import time
import threading

BK =  "#25283b"
BKD = "#1e202f"
TXT = "#c0caf5"
TXTD = "#6e749b"
FONT = "Hack Nerd Font"
WORK = 60*25
SBREAK = 60*5
LBREAK = 60*30

class Pomodoro:

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("mkapomo")
        self.win.geometry('600x300')
        self.win.resizable(False, False)
        self.win.config(bg=BK)
        self.win.tk.call('wm', 'iconphoto', self.win._w, tk.PhotoImage(file="icon.png"))

        #title
        self.titlelab = tk.Label(text="mkapomo", bg=BK, fg=TXT, font=(FONT, 32))
        self.titlelab.place(relx=0.35, rely=0.05)

        #timer
        self.timerlab = tk.Label(self.win, text="25:00", bg=BKD, fg=TXT, font=(FONT, 84), padx=10, pady=10)
        self.timerlab.place(relx=0.25, rely=0.25)

        #buttons
        self.startbut = tk.Button(self.win, text="start", padx=10, pady=10, font=(FONT, 18), command=self.start_threaded)
        self.startbut.place(relx= 0.2, rely=0.75)

        self.pausebut = tk.Button(self.win, text="pause", padx=10, pady=10, font=(FONT, 18), command=self.pause)
        self.pausebut.place(relx= 0.4, rely=0.75)

        self.resetbut = tk.Button(self.win, text="reset", padx=10, pady=10, font=(FONT, 18), command=self.reset)
        self.resetbut.place(relx= 0.6, rely=0.75)
        
        #labels
        self.countlab = tk.Label(self.win, text="pomodoros: 0", font=(FONT, 18), bg=BK, fg=TXT)
        self.countlab.place(relx= 0.75, rely=0.35)

        self.phaselab = tk.Label(self.win, text="phase: work", font=(FONT, 18), bg=BK, fg=TXT)
        self.phaselab.place(relx= 0.75, rely=0.45)

        #opts
        self.skipped = False
        self.stopped = False
        self.phase = 0
        self.pomodoros = 0
        self.curr = 0
        self.unpaused = False

        self.win.mainloop()

    def start(self):
        if self.stopped == True:
            self.stopped = False
            self.unpaused = True
        else:
            self.unpaused = False
        self.skipped = False
        ph = self.phase
        
        if ph == 0:
            if not self.unpaused:
                self.curr = WORK
            
            while self.curr > 0 and not self.stopped:
                mins, secs = divmod(self.curr, 60)

                self.timerlab.config(text=f"{mins:02d}:{secs:02d}")
                self.win.update()
                time.sleep(1)
                self.curr -= 1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.countlab.config(text=f"pomodorors: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.curr = 0
                    self.phase = 2
                    self.phaselab.config(text="phase: l break")
                    self.start()
                else:
                    self.curr = 0
                    self.phase = 1
                    self.phaselab.config(text="phase: s break")
                    self.start()

        elif ph == 1:
            if not self.unpaused:
                self.curr = SBREAK
            
            while self.curr > 0 and not self.stopped:
                mins, secs = divmod(self.curr, 60)

                self.timerlab.config(text=f"{mins:02d}:{secs:02d}")
                self.win.update()
                time.sleep(1)
                self.curr -= 1

            if not self.stopped or self.skipped:
                self.curr = 0
                self.phase = 0
                self.phaselab.config(text="phase: work")
                self.start()

        elif ph == 2:
            if not self.unpaused:
                self.curr = LBREAK

            while self.curr > 0 and not self.stopped:
                mins, secs = divmod(self.curr, 60)

                self.timerlab.config(text=f"{mins:02d}:{secs:02d}")
                self.win.update()
                time.sleep(1)
                self.curr -= 1

            if not self.stopped or self.skipped:
                self.phase = 0
                self.phaselab.config(text="phase:work")
                self.start()
        else:
            raise Exception("Invalid timer phase")

    def reset(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.timerlab.config(text="25:00")
        self.phaselab.config(text="phase: work")
        self.countlab.config(text="pomodoros: "+'0')
        self.phase = 0
        self.curr = WORK
        self.unpaused = False

    def start_threaded(self):
        t = threading.Thread(target=self.start)
        t.start()
    
    def pause(self):
        self.stopped = True


Pomodoro()
