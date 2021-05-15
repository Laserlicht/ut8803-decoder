import cp2110
import threading
import time
import json

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
    if "raw_value" in data:
        print("Values: " + json.dumps(data, default=str))
    if "deviceid" in data:
        print("DeviceID: " +data["deviceid"])

buf = bytearray(b'')
dat = {}
def decode_data(data):
    global buf, dat
    for b in data:
        if bytes([b]) == b'\xab':
            if buf[:2] == b'\xab\xcd':
                if len(buf) == 21 and buf[2] == 0x12:
                    if buf[11] == 0: 
                        dat["raw_value"] = float(buf[6:11])
                    else:
                        dat["raw_value"] = float(buf[6:12])

                    dat["mode"] = buf[4]
                    dat["range"] = buf[5]
                    dat["ol"] = bool(buf[14] & 0b00000100)
                    dat["hold"] = bool(buf[14] & 0b00000001)
                    dat["rel"] = bool(buf[15] & 0b00000001)
                    dat["min"] = bool(buf[16] & 0b00000001)
                    dat["max"] = bool(buf[16] & 0b00000010)

                    dat["raw"] = buf
                    dat["raw_text"] = buf.decode("cp1252")

                    handle_data(dat)
                if len(buf) == 26 and buf[2] == 0x17:
                    dat["deviceid"] = buf[4:-2].decode("cp1252")

                    dat["raw"] = buf
                    dat["raw_text"] = buf.decode("cp1252")

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



def requestDeviceID():
    d.write(b'\xab\xcd\x04\x58\x00\x01\xd4')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionHold():
    d.write(b'\xab\xcd\x04\x46\x00\x01\xc2')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionBacklight():
    d.write(b'\xab\xcd\x04\x47\x00\x01\xc3')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionSelect():
    d.write(b'\xab\xcd\x04\x48\x00\x01\xc4')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionManualRange():
    d.write(b'\xab\xcd\x04\x49\x00\x01\xc5')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionAutoRange():
    d.write(b'\xab\xcd\x04\x4a\x00\x01\xc6')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionMinMax():
    d.write(b'\xab\xcd\x04\x4b\x00\x01\xc7')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionExitMinMax():
    d.write(b'\xab\xcd\x04\x4c\x00\x01\xc8')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionRel():
    d.write(b'\xab\xcd\x04\x4d\x00\x01\xc9')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionDVal():
    d.write(b'\xab\xcd\x04\x4e\x00\x01\xca')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionQVal():
    d.write(b'\xab\xcd\x04\x4f\x00\x01\xcb')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionRVal():
    d.write(b'\xab\xcd\x04\x51\x00\x01\xcd')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')

def actionExitDQR():
    d.write(b'\xab\xcd\x04\x50\x00\x01\xcc')
    d.write(b'\xab\xcd\x04\x5a\x00\x01\xd6')



thread = threading.Thread(target=read_from_port, args=(d,))
thread.start()

time.sleep(1)
requestDeviceID()

while True:
    time.sleep(5)
