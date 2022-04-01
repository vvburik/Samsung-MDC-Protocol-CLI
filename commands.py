header = 'AA'
id_all = 'FE'

ACK_CODE = ord('A')  # 0x41 65
NAK_CODE = ord('N')  # 0x4E 78

power_command = '11' #0x11
power_command_on = '01' #0x01
power_command_off = '00' #0x00

input_source_command = '14'
DisplayPort = '25'
Hdmi = '21'

data_lenght = '01' #0x01



#switch_to_DP = bytes.fromhex('AA 14 FE 01 25 38')
#pwr_on = bytes.fromhex('AA 11 FE 01 01 11')