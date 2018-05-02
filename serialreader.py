import serial

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.5)

def readline():
    msg = ""
    while True:
        ch = port.read().decode()   
        if ch == '\r' or ch=='\n' or ch=='':
           if len(msg)>0:
               return msg
        msg += str(ch)
