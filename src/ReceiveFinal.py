import socket
# also I had to open the port on the rpi and on my computer
# for opening ports on linux (rpi) see https://raspberrypi.stackexchange.com/questions/69123/how-to-open-a-port
# for opening ports on windows see https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html
# for opening ports on macos see https://www.macworld.co.uk/how-to/how-open-specific-ports-in-os-x-1010-firewall-3616405/

def receiveRapFile(filename):
    s = socket.socket()
    host = socket.gethostbyname("192.168.10.23") # ip address of rpi
    port = 3333
    s.bind((host, port))
    s.listen(1)
    print(host)
    print("Ready to connect")
    conn, addr = s.accept()
    print("Connected")

    bpmB = conn.recv(64)
    bpm = int.from_bytes(bpmB, 'big')

    numB = 1024
    filenameA = "Accepted.txt"
    fileA = open(filenameA, 'rb')
    file_dataA = fileA.read()
    numkB = conn.recv(64)
    numkB = int.from_bytes(numkB, 'big')
    file_data = bytes(numB*numkB)
    for k in range(numkB):
        file_data[k*numB:((k+1)*numB)] = conn.recv(numB)
        print('%d/%d Received' % (k, numkB))
        conn.send(file_dataA)

    # filename = "audio.mp4"
    file = open(filename, 'wb')
    file.write(file_data)
    file.close()
    print("File has been received")
    return bpm

