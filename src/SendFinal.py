import socket
import numpy as np
# also I had to open the port on the rpi and on my computer
# for opening ports on linux (rpi) see https://raspberrypi.stackexchange.com/questions/69123/how-to-open-a-port
# for opening ports on windows see https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html
# for opening ports on macos see https://www.macworld.co.uk/how-to/how-open-specific-ports-in-os-x-1010-firewall-3616405/

def sendRPI(filename):
    s = socket.socket()
    host = socket.gethostbyname("192.168.1.7") # ip address of rpi
    port = 3333
    s.connect((host, port))
    print("Connected")

    filename_s = filename.split('_')
    for i in range(len(filename_s)):
        if 'bpm' in filename_s[i]:
            temp = filename_s[i].split('=')
            bpm = int(temp[-1])

    bpmB = bpm.to_bytes(64, 'big')
    s.send(bpmB)

    ## Send file after connecting
    numB = 1024
    # filename = "TTSRap.mp4"
    filenameA = "Accepted.txt"
    file = open(filename, 'rb')
    file_data = file.read()
    lengthB = len(file_data)
    numkB = int(np.ceil(lengthB/numB))
    numkB_inB = numkB.to_bytes(64, 'big')
    s.send(numkB_inB)
    for k in range(numkB):
        if (k+1)*numB < lengthB:
            data = file_data[k*numB:((k+1)*numB)]
        else:
            data = file_data[k*numB:lengthB]

        s.send(data)
        print("%d/%d Sent" % (k, numkB))
        fileA = open(filenameA, 'wb')
        file_dataA = s.recv(1024)
        fileA.write(file_dataA)
        fileA.close()
        print("%d/%d Accepted" % (k, numkB))

    print("File has been sent")
