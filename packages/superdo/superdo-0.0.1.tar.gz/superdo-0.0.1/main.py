import time, socket, os, math, random
from datetime import datetime

def ctime():
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return f'Current Time Is: {current_time}.'
def wait(numOfSeconds):
  return time.wait(numOfSeconds)
def cmd(commandName):
  return os.system(commandName)
def file(fileName2, extension2):
  return cmd(f'touch {fileName2}.{extension2}')
def ip():
  hostname = socket.gethostname()
  ip_addr = socket.gethostbyname(hostname)
  return ip_addr
def libs():
  return cmd('pip3 freeze >> requirements.txt')
def mpower(Number, Power):
  return Number ** Power
def pipget(PackageName):
  return cmd(f'pip3 install {PackageName}')
def mfact(Number):
  return math.factorial(Number)
def mvalue(Num1, Num2):
  if Num1 > Num2:
    return Num1
  elif Num1<Num2:
    return Num2
  elif Num1 == Num2:
    return 'Same.'
def rannum(Start, End):
  return random.randint(Start, End)