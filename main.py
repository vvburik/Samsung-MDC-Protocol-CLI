import socket
from scapy.all import *
from subprocess import Popen, PIPE
import argparse
import commands
from wol import wake_on_lan

pwr_on = [commands.header, commands.power_command, commands.id_all, commands.data_lenght, commands.power_command_on]
pwr_off = [commands.header, commands.power_command, commands.id_all, commands.data_lenght, commands.power_command_off]
switch_to_DP = [commands.header, commands.input_source_command, commands.id_all, commands.data_lenght, commands.DisplayPort]
swittch_to_Hdmi = [commands.header, commands.input_source_command, commands.id_all, commands.data_lenght, commands.Hdmi]

parser = argparse.ArgumentParser()
parser.add_argument('ip', type=str, help='Device Ip')
parser.add_argument('-port', default=1515, help='Default Samsung MDC Port is 1515')
parser.add_argument('-p', type=str, help='Power (On, Off), (-p on or -p off)')
parser.add_argument('-i', type=str, help='Input option, DP or HDMI, (-i dp or -i hdmi)')
parsed = parser.parse_args()

#ip = parsed.p

########## checksum calculate:
def checksum(command):
    cmd = command[1:] #cut header
    sum = 0
    #print(cmd)
    for i in cmd:
        #print (i)
        sum += int(i, 16)
    sum %= 256 #sum = sum % 256
    chksum = hex(sum)[2:]
    return chksum
#########

########## make command to send:
def makecommand (data, sum):
    str_command = ' '
    str_command = str_command.join(data) + ' ' + sum
    return bytes.fromhex(str_command)
##########

if str(parsed.p).lower().strip() == 'on':
    wol = str(input("Using Wake On Lan ? y or n ")).lower().strip()
    if wol == 'y':
        mac = getmacbyip(parsed.ip)
        print(mac)
        wake_on_lan(mac)
        print('Wake On Lan')
    elif wol == 'n':
        p_on = makecommand(pwr_on, checksum(pwr_on))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((parsed.ip, parsed.port))
        s.send(p_on)
        s.close()
elif str(parsed.p).lower().strip() == 'off':
    p_off = makecommand(pwr_off, checksum(pwr_off))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(parsed.ip, parsed.port)
    s.send(p_off)
    s.close()


