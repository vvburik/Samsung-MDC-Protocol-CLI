from base64 import encode
from encodings import utf_8
import socket
import struct

########FIND THIS CODE IN STACKOVERFLOW:  
def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """
     
    # Check macaddress format and try to compensate
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep,'')
    else:
        raise ValueError('Incorrect MAC address format')
         
         
    # Pad the synchronization stream
    data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()# + ('AA11FE010111').encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += struct.pack('B', int(data[i: i + 2], 16))

    # Broadcast it to the LAN
    #print(send_data)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(data, ('255.255.255.255',7))
