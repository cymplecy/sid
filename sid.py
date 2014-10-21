#!/usr/bin/env python
#Original Code Martin Bateman 2013
#Modified by Simon Walters
#GPLv2 applies
#V0.54 28Oct13 for scratchgpio4
#V0.6 5Dec13 - change patterns to SID and OK and use os.system call to launch scratchgpio
#V0.7 28Dec13 - cope with plus version vs standard

import sys
from socket import *
import subprocess
#from subprocess import Popen, call
import shlex
import os
import sys
import time
import threading
import getopt
import shlex

class Blink(threading.Thread):

    def __init__(self, on,off):
        super(Blink, self).__init__()
        self.on = on
        self.off = off
        self.terminated = False
        self.toTerminate = False
        self.sequence = [1,2,1,2,1,2]

    def start(self):
        self.thread = threading.Thread(None, self.run, None, (), {})
        self.thread.start()
        


    def run(self):
        while self.toTerminate == False:
            #print self.sequence
            for i in range(len(self.sequence)):
                if self.sequence[i] == 0:
                    #print self.sequence[i]
                    os.system("echo 0 >/sys/class/leds/led0/brightness")
                    time.sleep(self.off )
                if self.sequence[i] == 1:
                    #print self.sequence[i]
                    os.system("echo 1 >/sys/class/leds/led0/brightness")
                    time.sleep(self.on )
                    os.system("echo 0 >/sys/class/leds/led0/brightness")
                    time.sleep(self.off )
                if self.sequence[i] == 2:
                    #print self.sequence[i]
                    os.system("echo 1 >/sys/class/leds/led0/brightness")
                    time.sleep(3 * self.on )
                    os.system("echo 0 >/sys/class/leds/led0/brightness")
                    time.sleep(self.off )
        self.terminated = True

    def stop(self):
        self.toTerminate = True
        while self.terminated == False:
            # Just wait
            time.sleep(0.01)
            
    def set_delays(self,on,off):
        self.on = on
        self.off = off

    def set_sequence(self,sequence):
        self.sequence = sequence
        
            



def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial
  
myserial = getserial()
print myserial
print myserial[-4:]

if __name__ == "__main__":
   timeout = '300'
   try:
      opts, args = getopt.getopt(sys.argv[1:],"ht:",["timeout="])
   except getopt.GetoptError:
      print 'sudo sid.py -t <timeout>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'sudo sid.py -t <timeout>'
         sys.exit()
      elif opt in ("-t", "--timeout"):
         timeout = arg
         timeout = timeout.strip()
   print 'Timeout is:', timeout


   
s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 50000))
s.settimeout(int(float(timeout)))

os.system("echo none >/sys/class/leds/led0/trigger")

blinkthread = Blink(0.2,0.2) 
blinkthread.set_sequence([1,1,1,0,0,0,1,1,0,0,0,2,1,1,0,0,0,0,0])
      
blinkthread.start()

    #blinkthread.join()
    
while 1:
    try:
        #print "try reading socket"
        os.system("echo 1 >/sys/class/leds/led0/brightness")
        
        data, wherefrom = s.recvfrom(1500, 0) # get the data from the socket

    except (KeyboardInterrupt, SystemExit):
        print "Program Ending - please wait a few secs"
        break
    except timeout:
        print "No data received: socket timeout"
        #print sys.exc_info()[0]
        break
    except:
        print "Unknown error occured with receiving data"
        break    

    data = data.lower()
    print (data + " " + repr(wherefrom[0]))

    if (data.find("start sid" + myserial[-4:]) != -1):
        os.system('sudo pkill -f scratchgpio')
        os.system('sudo python /home/pi/scratchgpio5/scratchgpio_handler5.py '+ str(repr(wherefrom[0])) +' standard &')
        #print shlex.split("""x-terminal-emulator -e 'bash -c "sudo python /home/pi/simplesi_scratch_handler/scratch_gpio_handler2.py """ + str(repr(wherefrom[0])) + """"'""")
        #process = subprocess.Popen(shlex.split("""x-terminal-emulator -e 'bash -c "sudo python /home/pi/scratchgpio4/scratchgpio_handler4.py """ + str(repr(wherefrom[0])) + """"'"""), stdout=subprocess.PIPE)
        print "stop blinking"
        # try:
            # blinkthread.stop()
            # print "blinking stopped"
        # except:
            # pass
        # print "restart blinking"
        blinkthread.set_sequence([2,2,2,0,0,0,2,1,2,0,0,0,0,0,0,0,0,0,0])
        #blinkthread.start()
        time.sleep(30)
        break
        
    if (data.find("start sidplus" + myserial[-4:]) != -1):
        os.system('sudo pkill -f scratchgpio')
        os.system('sudo python /home/pi/scratchgpio5/scratchgpio_handler5.py '+ str(repr(wherefrom[0])) +' &')
        #print shlex.split("""x-terminal-emulator -e 'bash -c "sudo python /home/pi/simplesi_scratch_handler/scratch_gpio_handler2.py """ + str(repr(wherefrom[0])) + """"'""")
        #process = subprocess.Popen(shlex.split("""x-terminal-emulator -e 'bash -c "sudo python /home/pi/scratchgpio4/scratchgpio_handler4.py """ + str(repr(wherefrom[0])) + """"'"""), stdout=subprocess.PIPE)
        print "stop blinking"
        # try:
            # blinkthread.stop()
            # print "blinking stopped"
        # except:
            # pass
        # print "restart blinking"
        blinkthread.set_sequence([2,2,2,0,0,0,2,1,2,0,0,0,0,0,0,0,0,0,0])
        #blinkthread.start()
        time.sleep(30)
        break        


try:
    blinkthread.stop()
except:
    pass
time.sleep(1)
os.system("echo 0 >/sys/class/leds/led0/brightness")
time.sleep(1)
os.system("echo mmc0 >/sys/class/leds/led0/trigger")
s.close()
sys.exit()
