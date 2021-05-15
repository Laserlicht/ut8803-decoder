#import json
  
#tmp = ""
#with open('mitschnitt.json',) as f:
#    data = json.load(f)

#    for i in data:
#        if i["_source"]["layers"]["usb"]["usb.dst"] == "host" and "usb.capdata" in i["_source"]["layers"]:
#            byte_hex = i["_source"]["layers"]["usb.capdata"].split(":")[1]
#            byte = bytes.fromhex(byte_hex)
#            tmp += byte.decode("cp1252")

#print(tmp)

import cp2110
import threading
import time

d = cp2110.CP2110Device()
d.set_uart_config(cp2110.UARTConfig(
    baud=9600,
    parity=cp2110.PARITY.NONE,
    flow_control=cp2110.FLOW_CONTROL.DISABLED,
    data_bits=cp2110.DATA_BITS.EIGHT,
    stop_bits=cp2110.STOP_BITS.SHORT))
d.enable_uart()



last_p = ""
#https://stackabuse.com/how-to-print-colored-text-in-python/
def colorize_print(p):
    global last_p
    for i in range(len(p)):
        if len(last_p) > i and last_p[i] != p[i]:
            print("\033[0;31;40m" + p[i], end='')
        else:
            print("\033[0;37;40m" + p[i], end='')
    print("")
    last_p = p



def handle_data(data):
    if "value" in data:
        print(data["value"])
    if "deviceid" in data:
        print(data["deviceid"])

buf = bytearray(b'')
dat = {}
def decode_data(data):
    global buf, dat
    for b in data:
        if bytes([b]) == b'\xab':
            if buf[:2] == b'\xab\xcd':
                if len(buf) == 21 and buf[2] == 0x12:
                    if buf[11] == 0: 
                        dat["value"] = float(buf[6:11])
                    else:
                        dat["value"] = float(buf[6:12])

                    dat["mode"] = buf[4]
                    dat["range"] = buf[5]

                    handle_data(dat)
                if len(buf) == 26 and buf[2] == 0x17:
                    dat["deviceid"] = buf[4:-2].decode("cp1252")

                    handle_data(dat)
                
                #Debug
                #colorize_print(buf.decode("cp1252") + "\t" + str(buf) + "\t" + str(measurement["value"]) + "\t" + str(measurement["mode"]) + "\t" + str(measurement["range"]))
            buf = bytearray(b'')
            dat = {}
        buf.append(b)

def read_from_port(dev):
    while True:
        rv = d.read(64)
        if len(rv) > 0:
            decode_data(rv)



thread = threading.Thread(target=read_from_port, args=(d,))
thread.start()

while True:
    time.sleep(5)
    d.write(b'\xab\xcd\x04\x58\x00\x01\xd4')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')
