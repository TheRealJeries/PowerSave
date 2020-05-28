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
##                                                      add it to path to allow the script to work.
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

import os
import subprocess

## Change these variables as needed, machinename, username and password (in byte str) VERY IMPORTANT
sleep_time = "23:14" # Time has to be in this format
wake_time = "23:15" 
username = 'jeriesd1998'
password = 'password'
abs_path = os.path.abspath(os.getcwd()) # absolute path, needed for many situations

sleep_bat_filename = 'Sleep_Powersave.bat'
wake_bat_filename = 'Wake_Powersave.bat'
abs_path_sleep = abs_path + "\\" + sleep_bat_filename
abs_path_wake = abs_path + "\\" + wake_bat_filename


def create_sleep_bat_file():
        sleep_bat_file = open(sleep_bat_filename, 'w')  # Makes sure the .bat file for sleeping exists
        #sleep_bat_file.write('RUNDLL32.EXE powrprof.dll,SetSuspendState 0,1,0') # The command needed for sleep. Issues might arise if HIBERNATE mode is turned on, make sure it is off
        sleep_bat_file.write('psshutdown -d -t 0') # Make sure you have the psshutdown tool, rundll32.exe has a bug that didn't allow automatic wake up on my computer
        sleep_bat_file.close()


def create_wake_bat_file():
        script_name = '\\busy_script.py' ## This is a wake up script that keeps the CPU busy, a while loop with a sleep statement
        wake_bat_file = open(wake_bat_filename, 'w') # Makes sure .bat file for waking up exists 
        wake_bat_file.write('cmd.exe /c py -2 {}'.format(abs_path+script_name)) # Any non interactive command actually wakes up the computer, I chose a sound beep, could be cmd, anything
        #wake_bat_file.write('echo Hello')                                      # But I wrote a script that makes the CPU busy, basically a while true loop, to prevent the computer
                                                                                # from falling back asleep. TEST THIS FEATURE HEAVILY, make sure the work you need done happens.
        wake_bat_file.close()




# SCHTASKS is the Windows Task Scheduler command line interface.
# This command basically tells schtasks to create the task that executes the bat file
# /CREATE option creates the task, /F forces creation (whether task already exists or not), /TN (taskname), /RU username, /RP password, /SC is interval
# of repetition (I set it to daily) /TR is the sleep task in .BAT file format, absolute path needed.
#(which sleeps or wakes up the computer) every day at a specific time (see sleep_time/wake_time variables)
def create_sleep_task():
        create_command = 'SCHTASKS /CREATE /F /TN "Power Save" /RU {} /RP {} /SC DAILY /ST {} /TR {}'.format(username, password, sleep_time, abs_path_sleep) 
        output = subprocess.check_output(create_command)
        print(output.decode())

# Creates the wake up task
def create_wake_task():
        create_command = 'SCHTASKS /CREATE /F /RU {} /RP {} /TN "Wake from Power Save" /SC DAILY /ST {} /TR {}'.format(username, password, wake_time, abs_path_wake)
        output = subprocess.check_output(create_command)
        print(output.decode())


        # Unfortunately, there is no wake to run option from the command line, so I edit the XML manually in this for loop to add that option,
        # along with other options. I figured this out only by tweaking options in Windows Task Scheduler and exporting them to XML form.
        query_xml = 'SCHTASKS /QUERY /XML /TN "Wake from Power Save"'
        proc = subprocess.Popen(query_xml, stdout=subprocess.PIPE)

        wake_xml = open('Wake_Powersave.xml','w')
        in_settings = False
        for l in proc.stdout:
                line = l.decode().strip('\n')
                if ('<LogonType>' in line):
                        wake_xml.write('\t<LogonType>Password</LogonType>\n')
                elif ('</Settings>' in line):
                        in_settings = False
                elif ('<Settings>' in line or in_settings):
                        
                        
                        if (not in_settings):
                                in_settings = True ## Settings found by tweaking around manually with windows task scheduler.
                                wake_xml.write("""
        <Settings>
                <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
                <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
                <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
                <AllowHardTerminate>true</AllowHardTerminate>
                <StartWhenAvailable>true</StartWhenAvailable>
                <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
                <IdleSettings>
                        <StopOnIdleEnd>true</StopOnIdleEnd>
                        <RestartOnIdle>false</RestartOnIdle>
                </IdleSettings>
                <AllowStartOnDemand>true</AllowStartOnDemand>
                <Enabled>true</Enabled>
                <Hidden>false</Hidden>
                <RunOnlyIfIdle>false</RunOnlyIfIdle>
                <WakeToRun>true</WakeToRun>
                <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
                <Priority>7</Priority>
        </Settings>                                
                                            """)
                                
                elif (not in_settings):
                        wake_xml.write(line)

        proc.wait()
        wake_xml.close()

        # Now recreate the same task using the modified XML, biggest change is having Wake To Run option enabled.
        create_command = 'SCHTASKS /CREATE /F /RU {} /RP {} /TN "Wake from Power Save" /XML {} '.format(username, password, abs_path + '\Wake_Powersave.xml')
        output = subprocess.check_output(create_command)
        print(output.decode())

if __name__ == "__main__":
        create_sleep_bat_file()
        create_wake_bat_file()
        create_sleep_task()
        create_wake_task()




