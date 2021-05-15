# UT8802 / UT8803 Protocol

## Requirements

Required PIP packages: pycp2110

Required packages (ubuntu): libhidapi-hidraw0 or libhidapi-libusb0

## WireShark-Filter
### Outgoing
```
usb.transfer_type == 0x1 && usb.endpoint_address.direction == 0
```

## Reverse engineered protocol

### Common
* Start Sequence = \xab \xcd
* Last Byte = Checksum + Offset

### Send

#### Connect / SerialNr
abcd04580001d4

abcd045a0001d6

**Response:**
abcd1700303337344646313635343639353537383738313605d7

last Byte = Checksum - 5
**Device ID:**
0374FF16546955787816

#### Hold
abcd04460001c2

abcd045a0001d6

#### Backlight
abcd04470001c3

abcd045a0001d6

#### Select
abcd04480001c4

abcd045a0001d6

#### ManualRange
abcd04490001c5

abcd045a0001d6

#### AutoRange
abcd044a0001c6

abcd045a0001d6

#### Min/Max
abcd044b0001c7

abcd045a0001d6

#### Exit Min/Max
abcd044c0001c8

abcd045a0001d6

#### Rel
abcd044d0001c9

abcd045a0001d6

#### D Value
abcd044e0001ca

abcd045a0001d6

#### Q Value
abcd044f0001cb

abcd045a0001d6

#### R Value
abcd04510001cd

abcd045a0001d6

#### Exit DQR
abcd04500001cc

abcd045a0001d6

### Receive

#### Bytes
| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \xab | \xcd | \x12 | \x02 | Mode | Range | Sign (+/-) | Value (7-11) | | | | Value 5. or NULL | 13 | 14 | Hold / O.L. | REL | Flags Min/Max | 18 | 19 | 20 | Checksum |

#### Hold / O.L.
| Bits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 1 | 2 | 3 | 4 | O.L. | 6 | HOLD | 

#### Rel
| Bits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | REL | 

#### Flags Min/Max
| Bits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 0 | 1 | 2 | 3 | 4 | 5 | MAX | MIN | 

#### Modes
| Value | Mode |
| --- | --- |
| 0 | Voltage AC |
| 1 | Voltage DC |
| 2 | Current µA AC |
| 3 | Current mA AC |
| 4 | Current A AC |
| 5 | Current µA DC |
| 6 | Current mA DC |
| 7 | Current A DC |
| 8 | Resistance |
| 9 | Continuity buzzer |
| 10 | Diode |
| 11 | Impendance |
| 12 | Impendance (Q) |
| 13 | Impendance (R) |
| 14 | Capacitance |
| 15 | Capacitance (D) |
| 16 | Capacitance (R) |
| 17 | hfe |
| 18 | scr |
| 19 | Temperature °C |
| 20 | Temperature °F |
| 21 | Frequency |
| 22 | Duty cycle |

#### Ranges
| Value | Bits | Voltage | Resistance | Capacitance | Capacitance (R) | Impendance | Impendance (R) | Frequency | Duty cycle | Current (µA) | Current (mA) | Current (A) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 0011<span style="color:red">0000</span> | 000.0mV | 000.0Ω | 0.000nF | | 000.0µH | | 000.0Hz | 000.0% | 000.0µA | 00.00mA | 00.00A |
| 49 | 0011<span style="color:red">0001</span> | 0.000V | 0.000kΩ | 00.00nF | | 0.000mH | | 0.000kHz | 000.0% | 0000µA | 000.0mA | |
| 50 | 0011<span style="color:red">0010</span> | 00.00V | 00.00kΩ | 000.0nF | 0.000kΩ | 00.00mH | 0.000kΩ | 00.00kHz | 000.0% | | | |
| 51 | 0011<span style="color:red">0011</span> | 000.0V | 000.0kΩ | 0.000mF | 00.00kΩ | 000.0mH | | 000.0kHz | | | | |
| 52 | 0011<span style="color:red">0100</span> | 0000V | 0.000MΩ | 00.00mF | 0.000MkΩ| 0.000H | 000.0MkΩ | 0.000MHz | | | | |
| 53 | 0011<span style="color:red">0101</span> | | 00.00MΩ |  | | 00.00H | | 00.00Mhz | | | | |
| 54 | 0011<span style="color:red">0110</span> | | | 000.0mF | | | | | | | | |

#### Checksum
Bytewise sum of Byte 0..19 minus 4

Example:
```python
a = bytearray(b"\xab\xcd\x12\x02\x061+000.00002640\x048")
for b in a[:-1]:
    print(b)
print()
print(a[-1]+4) # Last Byte +4
print(sum(a[:-1]) & 0xFF) #Bytewise add with overflow
```
