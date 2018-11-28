# -*- coding: utf-8 -*-
# @Time : 2018/11/28 14:53
# @Author : "Lance"
# @Email : lance_adela.@163.com
# @File : shutdown.py
import socket
import struct
import time

from django.http import HttpResponse


def wake_up(request, mac='DC-4A-3E-78-3E-0A'):
    MAC_ADD = mac
    BROADCAST = "192.168.0.255"
    if len(MAC_ADD) != 17:
        raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
    mac_address = MAC_ADD.replace("-", '')
    if mac_address != 12:
        raise ValueError("MAC address should be right")
    data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
    send_data = b''

    # 把原始数据转换为16进制字节数组，
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])
    print(send_data)

    # 通过socket广播出去，为避免失败，间隔广播三次
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        print("Done")
        return HttpResponse()
    except Exception as e:
        print(e)
        return HttpResponse()
