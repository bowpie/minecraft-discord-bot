from subprocess import PIPE, Popen
from requests import get
import os, time
from threading import Thread

class MinecraftServer():
    def __init__(self, svpath, minram='2048M', maxram='3072M'):
        self.svpath = svpath
        self.pathcmd = f'powershell.exe java -Xmx{maxram} -Xms{minram} -jar "' + f'\"{self.svpath}\"\"' + ' nogui'
        self.process = None
        self.lineBuffer = []
       
    def start(self):
        if self.process is None:
            os.chdir('\\'.join(self.svpath.split('\\')[0:2]))
            self.process = Popen(self.pathcmd, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)

            #run the reader thread
            t = Thread(target=self.reader, args=(self.process.stdout, self.lineBuffer))
            t.daemon=True
            t.start()
            #run the command input threads so that the owner can write commands
            t2 = Thread(target=self.get_input)
            t2.daemon = True
            t2.start()

            return "Server has started."
        else:
            return "Server already running."

    def status(self):
        if self.process == None:
            return "Server is closed."
        else:
            return "Server is open."

    
    def command(self, cmd, args = ''):
        if(self.process is not None):
            self.lineBuffer.clear()
            if args != '':
                cmd = cmd + ' ' + args + '\n'
            else:
                cmd = cmd + '\n'

            self.process.stdin.write(cmd)
            self.process.stdin.flush()
            time.sleep(1)
            #STOPPING THE SERVER
            if "stop" in cmd:
                time.sleep(1)
                self.process = None
                os.system("cls")
                return "Stopping Minecraft Server"
            else:
                return self.lineBuffer
        else:
            return ["Server is not running."]

    def get_input(self):
        while self.process is not None:
            cmd = input()
            if cmd.startswith('/'):
                self.command(cmd)
        
    def reader(self,f,buffer):
        while self.process is not None:
            line=f.readline()
            print(line, end="")
            if line:
                buffer.append(line)
            
    @staticmethod
    def ip():
        ip_var = get('https://api.ipify.org').text
        while len(ip_var) > 20:
            ip_var = get('https://api.ipify.org').text
            time.sleep(1)
        
        return ip_var



if __name__ == "__main__":
    pass
    



