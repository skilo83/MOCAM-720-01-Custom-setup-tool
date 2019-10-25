# MOCAM 720-01 Custom setup tool v1.0

import sys
import socket

def subCypher(ssid, passwd):
    #The wifi credentials must be encoded with this cypher or the camera will reject them
    #as of version 1.0 this list is incomplete and does not yet contain special chars
    #so ssid's containing special chars will not work with this script just yet.
    decodedChars = {'a':'e',
                    'b':'f',
                    'c':'g',
                    'd':'h',
                    'e':'i',
                    'f':'j',
                    'g':'k',
                    'h':'l',
                    'i':'m',
                    'j':'n',
                    'k':'o',
                    'l':'p',
                    'm':'q',
                    'n':'r',
                    'o':'s',
                    'p':'t',
                    'q':'u',
                    'r':'v',
                    's':'w',
                    't':'x',
                    'u':'y',
                    'v':'z',
                    'w':'{',
                    'x':'|',
                    'y':'}',
                    'z':'~',
                    'A':'E',
                    'B':'F',
                    'C':'G',
                    'D':'H',
                    'E':'I',
                    'F':'J',
                    'G':'K',
                    'H':'L',
                    'I':'M',
                    'J':'N',
                    'K':'O',
                    'L':'P',
                    'M':'Q',
                    'N':'R',
                    'O':'S',
                    'P':'T',
                    'Q':'U',
                    'R':'V',
                    'S':'W',
                    'T':'X',
                    'U':'Y',
                    'V':'Z',
                    'W':'{',
                    'X':'|',
                    'Y':'}',
                    'Z':'~',
                    '0':'4',
                    '1':'5',
                    '2':'6',
                    '3':'7',
                    '4':'8',
                    '5':'9',
                    '6':':',
                    '7':';',
                    '8':'<',
                    '9':'=',
                    ' ':'$',
                    '-':'1'}

    newStrList = []
    for c in ssid:
        for k, v in decodedChars.items():
            if c is k:
                newStrList.append(v)
                
    ENCODED_WIFI_SSID = ''.join(newStrList)
    
    newStrList = []
    for c in passwd:
        for k, v in decodedChars.items():
            if c is k:
                newStrList.append(v)
                
    ENCODED_WIFI_PASSWORD = ''.join(newStrList)

    return ENCODED_WIFI_SSID, ENCODED_WIFI_PASSWORD

def send_command(commandToSend):
    OTA_SERVER_URL = "nothing"
    GATEWAY_URL = "nothing"
    SIGNALING_URL = "nothing"
    WIFI_PASSWORD = "nothing"
    WIFI_SSID = "nothing"
    if commandToSend == "1":
        cnum = 1
    if commandToSend == "2":
        cnum = 2
    if commandToSend == "3":
        print("Enter cloud URLs to send.\n")
        OTA_SERVER_URL = str(input("OTA server URL: "))
        GATEWAY_URL = str(input("Gateway URL: "))
        SIGNALING_URL = str(input("Signaling URL: "))
        cnum = 3
    if commandToSend == "4":
        print ("Enter information to connect the MOCAM 720-01 to your WiFi network\n")
        RAW_SSID = str(input("WiFi SSID: "))
        RAW_PASSWORD = str(input("WiFi Password: "))
        WIFI_SSID, WIFI_PASSWORD = subCypher(RAW_SSID, RAW_PASSWORD)
        cnum = 4

    GET_DEVICE_ID = "{\"req\":\"get device id\"}"
    LIST_WIFI = "{\"req\":\"list wifi\"}"
    SET_CLOUD_URLS = "{\"req\":\"set cloud urls\",\"otaServerUrl\":\"" + OTA_SERVER_URL + "\",\"gatewayUrl\":\"" + GATEWAY_URL + "\",\"signalingUrl\":\"" + SIGNALING_URL + "\"}"
    SET_WIFI = "{\"req\":\"set wifi\",\"ssid\":\"" + WIFI_SSID + "\",\"password\":\"" + WIFI_PASSWORD + "\"}"

    try:
        print("Enter your cameras IP address here or press enter to use the default.\n")
        TCP_IP = str(input("Camera IP Address: "))
        if not TCP_IP:
            TCP_IP = "192.168.8.1"
        TCP_PORT = 5053
        BUFFER_SIZE = 9000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        if cnum == 1:
            s.send((GET_DEVICE_ID.encode("utf-8")))
        elif cnum == 2:
            s.send((LIST_WIFI.encode("utf-8")))
        elif cnum == 3:
            s.send((SET_CLOUD_URLS.encode("utf-8")))
        elif cnum == 4:
            s.send((SET_WIFI.encode("utf-8")))
        data = s.recv(BUFFER_SIZE).decode()
        print("Camera response: " + data + "\n")
        s.close()
        sys.exit(0)
    except Exception as e:
        s.close()
        sys.exit(str(e))

def main():
    HELP_INFO = """Options:\n
        1 = get device id\n
        2 = list wifi networks\n
        3 = set cloud urls\n
        4 = connect to wifi network"""
    if len(sys.argv) != 2:
        sys.exit("\nUsage: " + str(sys.argv[0]) + ' <option> ' + '\n' + '\n' + HELP_INFO)
    elif sys.argv[1] == "1":
        send_command("1")
    elif sys.argv[1] == "2":
        send_command("2")
    elif sys.argv[1] == "3":
        send_command("3")
    elif sys.argv[1] == "4":
        send_command("4")
    else:
        sys.exit("\nUsage: " + str(sys.argv[0]) + ' <option> ' + '\n' + '\n' + HELP_INFO)
        

if __name__ == "__main__":
    main()