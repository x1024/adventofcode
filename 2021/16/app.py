#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import queue
import binascii

TYPE_LITERAL = 4
TYPE_SUM = 0
TYPE_PRODUCT = 1
TYPE_MIN = 2
TYPE_MAX = 3
TYPE_GREATER_THAN = 5
TYPE_LESS_THAN = 6
TYPE_EQUAL_TO = 7


def hex2bin(string):
    return bin(int(string, 16))[2:].zfill(len(string) * 4)


def parse(packet):
    version = int(packet[:3], 2)
    type = int(packet[3:6], 2)
    result = { 'version': version, 'type': type }

    if type == TYPE_LITERAL:
        packet_length = 6
        value = []
        while True:
            chunk = packet[packet_length:packet_length+5]
            value.append(chunk[1:])
            packet_length += 5
            if chunk[0] == '0':
                break
        result['value'] = int(''.join(value), 2)
    else:
        length_type_id = int(packet[6], 2)
        sub_packets = []
        if length_type_id == 0:
            length = int(packet[7:7+15], 2)
            packet_length = 7 + 15 + length
            i = 7 + 15
            while i < packet_length:
                sub_packet = parse(packet[i:])
                i += sub_packet['packet_length']
                sub_packets.append(sub_packet)
        else:
            num_packets = int(packet[7:7+11], 2)
            packet_length = 7+11
            for _ in range(num_packets):
                sub_packet = parse(packet[packet_length:])
                packet_length += sub_packet['packet_length']
                sub_packets.append(sub_packet)
        result['sub_packets'] = sub_packets
    result['packet_length'] = packet_length
    return result


def checksum(data):
    result = data['version']
    if 'sub_packets' in data:
        result += sum(checksum(packet) for packet in data['sub_packets'])
    return result


def easy(data):
    return checksum(parse(hex2bin(data)))


def evaluate(data):
    t = data['type']
    if t == TYPE_LITERAL: return data['value']
    values = [evaluate(packet) for packet in data['sub_packets']]
    
    if t == TYPE_SUM: return sum(values)
    if t == TYPE_PRODUCT: return reduce((lambda a, b: a*b), values, 1)
    if t == TYPE_MIN: return min(values)
    if t == TYPE_MAX: return max(values)
    if t == TYPE_GREATER_THAN: return int(values[0] > values[1])
    if t == TYPE_LESS_THAN: return int(values[0] < values[1])
    if t == TYPE_EQUAL_TO: return int(values[0] == values[1])


def hard(data):
    return evaluate(parse(hex2bin(data)))


def test():
    data = '''
    '''
    assert hex2bin('D2FE28' ) == '110100101111111000101000'
    assert hex2bin('38006F45291200') == '00111000000000000110111101000101001010010001001000000000'
    assert parse(hex2bin('D2FE28')) == { 'packet_length': 21, 'type': 4, 'version': 6, 'value': 2021 }
    assert parse(hex2bin('EE00D40C823060')) == {
            'version': 7,
            'type': 3,
            'sub_packets': [
                {'packet_length': 11, 'version': 2, 'type': 4, 'value': 1},
                {'packet_length': 11, 'version': 4, 'type': 4, 'value': 2},
                { 'packet_length': 11, 'version': 1, 'type': 4, 'value': 3}
            ],
            'packet_length': 51,
        }

    assert parse(hex2bin('38006F45291200')) == {
            'version': 1,
            'type': 6,
            'packet_length': 49,
            'sub_packets': [
                {'packet_length': 11, 'version': 6, 'type': 4, 'value': 10},
                { 'packet_length': 16, 'version': 2, 'type': 4, 'value': 20}
            ]
        }

    assert easy('8A004A801A8002F478') == 16
    assert easy('620080001611562C8802118E34') == 12
    assert easy('C0015000016115A2E0802F182340') == 23
    assert easy('A0016C880162017C3686B18A3D4780') == 31

    assert hard('C200B40A82') == 3
    assert hard('04005AC33890') == 54
    assert hard('880086C3E88112') == 7
    assert hard('CE00C43D881120') == 9
    assert hard('D8005AC2A8F0') == 1
    assert hard('F600BC2D8F') == 0
    assert hard('9C005AC2F8F0') == 0
    assert hard('9C0141080250320F1802104A08') == 1


def main():
    test()
    data = open('in.txt').read()
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()
