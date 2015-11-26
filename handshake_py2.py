#Original Code Martin Bateman 2013
#Modified by Simon Walters
#GPLv2 applies
#Main Computer End running Scratch
#V0.3 28Nov13
#V0.4 18Dec13 - Handle plus version
#V0.5 add in ping 169.254.64.64

import sys 
import time
import socket
#from tkinter import * # lower case T for Python 3 on Apple Mac
from Tkinter import * # upper case T for Python 2 on PC
import os

def onSend():

    #Function that's invoked when button pressed
    if var.get() == 1:
        message = "Start SIDplus" + entry_box.get()
    else:
        message = "Start SID" + entry_box.get()
    b.configure(state='disabled')
    for i in range(0,10):
        progress.set("Sending ("+str(i + 1)+" of 10):"+message+"..." )
        master.update_idletasks()
        time.sleep(1)
        s.sendto(message, ('<broadcast>', 50000)) # Python 2 version
        #s.sendto(message.encode(), ('<broadcast>', 50000)) # Python 3 version
        progress.set("Sending ("+str(i + 1)+" of 10):"+message+"   " )
        master.update_idletasks()
        time.sleep(1)
    progress.set("Finished")
    time.sleep(2)
    #sys.exit(0)
    b.configure(state='active')
    #s.close()
    master.update_idletasks()

def pingTask():
    pingsend = os.popen('ping 169.254.64.64 -n 1')
    pingread = pingsend.readlines()
    msLine = pingread[-1].strip()
    #ping.set(msLine)
    if "100% loss" not in msLine:
        ping.set("PI connected directly")
        
    else:
        ping.set("")
    #print msLine
    #print msLine.splot(' = ')[-1]
    master.after(500,pingTask)  # reschedule event in 2 seconds

   

master = Tk()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 0)) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

progress = StringVar()
var = IntVar()
ping = StringVar()
    
master.title('Find a Raspberry Pi Scratch Interface Device')
#Add instruction label
text_label=Label(master,text='Enter the Pi Serial Number (Last 4 digits)')
text_label.pack(padx=10,pady=10)

#Add a data entry box
entry_box = Entry(master)
entry_box.pack()

#Add a label for progress
msgLabel=Label(master,textvariable=progress)
msgLabel.pack()
#Add a label for ping
pingLabel=Label(master,textvariable=ping)
pingLabel.pack()
ping.set("No direct connection to pi")

#Make data entry box default position for data entry
entry_box.focus_set()

#Add Button to initiate connection process
b = Button(master, text="Connect", width=10, command=onSend)
b.pack()

#Make the Connect button be default action for Return key
master.bind('<Return>', (lambda e, b=b: b.invoke())) 


c = Checkbutton(master, text="Plus", variable=var)
c.pack()

#self.buttonBox.setdefault('OK')
#  parent.bind('<Return>', self._processReturnKey)
#  parent.focus_set()



master.after(100,pingTask)
mainloop()





