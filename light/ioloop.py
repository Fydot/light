#!/usr/bin/env python
# coding: utf8
import socket
import select


fd_events = {}
epoll = select.epoll()


def create_server_sock(host, port, backlog=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind((host, port))
    sock.listen(backlog)
    return sock


def run(app):
    server_sock = create_server_sock(app.host, app.port, backlog=app.backlog)
    epoll.register(server_sock, select.EPOLLIN | select.EPOLLOUT)
    while True:
        events = epoll.poll()
        for fd, event in events:
            if fd == server_sock.fileno():
                client_sock, addr = server_sock.accept()
                epoll,register(client, select.EPOLLIN | select.EPOLLOUT | select.EPOLLHUP)
                fd_events[client_sock.fileno()] = app
