#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

import socket

# 本模块负责抽象化SOCKET通信

class GxxGmTcpSrv:

    def __init__(self):
        self.srv_socket = 0

    def initialize(self, listen_ip, listen_port):
        self.srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.srv_socket == 0:
            return -1

        socket_address = (str(listen_ip), int(listen_port))
        self.srv_socket.bind(socket_address)
        self.srv_socket.listen(5)

        return 0

    def start(self):
        cli_socket, cli_addr = self.srv_socket.accept()
