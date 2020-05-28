# PowerSave: Compatible for python 2 and 3
# By: Jeries Dababneh, email: Jeriesd1998@gmail.com, github: https://github.com/TheRealJeries

# This program illustrates automating powersaving, in cases where you need your windows computer to stop working at certain times, and start working at others. 
# SCHTASKS is the command line utility to interact with Windows Task Scheduler. Windows Task Scheduler allows us to make the computer go to sleep, and wake up at specific times 
# Write SCHTASKS /? in command line to see how it works.
# The functionality provided in this file is dependent on having administrative access, and power settings allowing wake timers, and minimal to no default sleep available.
# Variables username, password, wake_time, sleep_time are to be modified as needed. It is important to have administrative access, as well as have a password set.
# If a password is not set, windows will often not allow this script to run for security reasons.
# If a password is not set for reasons that we have a lot of instruments to remember, I suggest using the same username and password, but atleast have something, and with admin
# privileges.

## !!!!!! PLEASE READ !!!!!!:
## 1- Admin Privileges, Username and password availability; to allow manipulating task scheduling
## 2- RUNDLL32 vs PSSHUTDOWN : the built in RUNDLL32 command has a bug in it that does not allow automatic wake up, so using the tool PSSHUTDOWN 
##                                                      even though it is a windows sysinternals tool, it is not installed by default, but is essential
##                                                      for automatic wake up to work. Please download it and
##                                                      add it to path to allow the script to work. Make sure it is in your path,
##                                                      on my system I added it to C:\Windows\System32
## 3- Read/Write/Execute permissions in directory and efficiency: To be fully automatic, I made the script write the .BAT files, and write and edit .XML task file,
##                                                      however, this is not a requirement, this is ONLY to take work off the users hands. You can write the .BAT files permanently
##                                                      as well as the .XML file, and schedule using the Windows Task Scheduler to avoid repetition of steps. However, this script's
##                                                      goal is automating power saving. A few wasted CPU cycles are not as important as saving power for 12 hours or so.
## 4- Power options: Make sure that power options for your computer are compatible with what we are trying to do. If you have your computer automatically sleeping with
##                                                      some sort of power saving / default option auto sleep, it might mess up the cycles of this program.
## 5- System dependency: Please be aware that this might vary from system to system and is very hardware oriented. Some systems have High Precision Event Timers disabled
##                                                      some enabled, and others don't even have them, and discrepancies like these COULD affect the way this script works.
##                                                      Also, hibernate might cause issues if you try to use RUNDLL32.
## 6- The wake up script:  With testing, simply echo'ing "Hello World" with the "Wake To Run" option would wake up the computer, however, with no
##                                                      key strokes or mouse moving, my laptop seemed to go back to sleep. HOWEVER, if you run a task, ALSO with
##                                                      "Wake to Run" option enabled, but this task is a busy script, (I tried an infinite while loop in python)
##                                                      it seemed that my computer did not go back to sleep. This is completely dependent on YOUR needs and goals
##  FINALLY: Integrate this program into YOUR goals. Change the Wake Up .BAT file to perform the task you need your computer
##           to perform, hopefully a CPU intensive one. Change the USERNAME, PASSWORD, AND SLEEP AND WAKE TIMES to what you need  them to be.
##           Make sure this does exactly what you need it to do. I suggest testing it for a few days before completely relying on it.
