from distutils.command.config import config
from pickle import NONE
import socket
from scapy.all import *
from subprocess import Popen, PIPE
import argparse
import configparser
import os
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

def create_config_file (file):
    config = configparser.ConfigParser()
    config.add_section('Device')
    config.set('Device', str(parsed.ip), str(getmacbyip(parsed.ip)))
    #config.set('Device', 's-box', '0')
    #config.set('Device', 'ip', str(parsed.ip))
    #config.set('Device', 'mac', str(getmacbyip(parsed.ip)))
    with open(file, 'w') as configfile:
        config.write(configfile)

def read_file (file):
    if not os.path.exists(file):
        create_config_file(file)
    elif os.path.exists(file):
        l = []
        with open(file, 'r') as f:
            for L in f:
                l.append(L)
            f.close()
        if len(l) == 0:
            config = configparser.ConfigParser()
            #config.read(file)
            config.add_section('Device')
            config.set('Device', str(parsed.ip), str(getmacbyip(parsed.ip)))
            with open(file, 'w') as configfile:
                config.write(configfile)
        elif len(l) != 0:
            config = configparser.ConfigParser()
            config.read(file)
            config.set('Device', str(parsed.ip), str(getmacbyip(parsed.ip)))
            with open(file, 'w') as configfile:
                config.write(configfile)

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

if str(parsed.i).lower().strip() == 'dp':
    p_dp = makecommand(switch_to_DP, checksum(switch_to_DP))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(parsed.ip, parsed.port)
    s.send(p_dp)
    s.close()
elif str(parsed.i).lower().strip() == 'hdmi':
    p_hdmi = makecommand(swittch_to_Hdmi, checksum(swittch_to_Hdmi))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(parsed.ip, parsed.port)
    s.send(p_hdmi)
    s.close()

if __name__ == "__main__":
    file = "Devices.ini"
    read_file(file)