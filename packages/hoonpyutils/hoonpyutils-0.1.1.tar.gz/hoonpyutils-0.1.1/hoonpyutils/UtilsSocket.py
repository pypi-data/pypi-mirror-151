#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import socket
import time
import json
import traceback
import signal
from . import UtilsCommon as utils

basename = os.path.basename(__file__)
try:
    import psutil
except Exception as e:
    print(" @ Warning: psutil import error in {} - {}".format(basename, str(e)))


class Server:
    def __init__(self, ini=None):
        self.name       = None
        self.acronym    = None
        self.ip         = None
        self.port       = None
        self.listen_num = None

        if ini:
            self.init_ini(ini)

    def init_ini(self, ini):

        self.ip = ini['ip']
        self.port = int(ini['port'])
        try:
            self.name = ini['name']
        except KeyError:
            self.name = 'anonymous'
        try:
            self.acronym = ini['acronym']
        except KeyError:
            self.acronym = 'am'
        try:
            self.listen_num = int(ini['listen_num'])
        except KeyError:
            self.listen_num = 5


def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # noinspection PyBroadException
        try:
            s.bind((ip, port))
            return False
        except Exception:
            return True


def kill_process(port, name="", logger=None):
    for proc in psutil.process_iter():
        try:
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == port:
                    # noinspection PyBroadException
                    try:
                        proc.send_signal(signal.SIGTERM)
                        proc.send_signal(signal.SIGKILL)
                    except Exception as e:
                        print(e)
                    if logger:
                        logger.info(" > Killed the process {} using {:d} port\n".format(name, port))
                    time.sleep(1)
        except psutil.AccessDenied as ad:
            print(ad)
        except psutil.ZombieProcess as zp:
            print(zp)
        except Exception as e:
            print(e)


def get_server_socket(ip, port, logger=utils.get_stdout_logger(), server_name='', listen_num=5):
    logger.info(" # Getting server socket...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    # logger.info(server_address)
    # check = check_port(ip, port, logger=logger)
    # logger.info(check)
    # if check:
    if check_port(ip, port):  # , logger=logger):
        logger.info(" # Port, {:d}, was already taken. "
                    "The process using {:d} will be killed first.".format(port, port))
        kill_process(port, name=server_name)
        time.sleep(2)

    logger.info(" # Starting up \"{}\" SERVER on {}:{:d}...".format(server_name, ip, port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    sock.listen(listen_num)

    return sock


def send_data_via_socket(ip, port, data_to,
                         show_send_dat_=False,
                         show_recv_dat_=False,
                         prefix=" #",
                         recv_=True,
                         timeout_val=60.,
                         logger=utils.get_stdout_logger()):

    data_to_enc = data_to.encode('utf-8') if isinstance(data_to, str) else data_to
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_val)
    server_address = (ip, port)

    if logger:
        logger.info(prefix + " Connecting socket to {} port {:d}...".format(server_address[0], server_address[1]))
    try:
        sock.connect(server_address)
    except Exception as e:
        if logger:
            logger.error(e)
        return False, None

    data_from = None
    try:
        sock.sendall(data_to_enc)
        if show_send_dat_ and logger is not None:
            logger.info(prefix + " Sent data ({:d}) : {}".format(len(data_to), data_to))

        if recv_:
            data_from = recv_all(sock, prefix=prefix, logger=None).decode('utf-8')
            if not data_from:
                if logger:
                    logger.error(prefix + " Failed to received")
                return False, None
            if show_recv_dat_ and logger is not None:
                logger.info(prefix + " Received data ({:d}) :  {}".format(len(data_from), data_from))

    except Exception as e:
        if logger:
            logger.error(e)
        return False, data_from
    finally:
        if logger:
            logger.info(prefix + " Closing socket.")
        sock.close()
        return True, data_from


def handle_command_request(sock, func=None, response_=True, logger=utils.get_stdout_logger()):
    logger.info('')
    logger.info(' # Waiting for a connection...')

    con, client_address = sock.accept()
    logger.info(" # Connected with {} at {}.".format(client_address, utils.get_datetime()[:-3]))

    ret_ = True
    sent_msg = ''
    dict_dat = {}
    try:
        str_dat = recv_all(con, recv_buf_size=4092, logger=None).decode('utf-8')
        logger.info(" # Received {:d} bytes.".format(len(str_dat)))
        # logger.info(" # Received: \"{}\"".format(str_dat))
        if utils.is_json(str_dat):
            dict_dat = json.loads(str_dat)
            cmd = dict_dat['cmd'].lower()
            if cmd == 'check':
                logger.info(" # Received \"check\" command")
                sent_msg = '{"state":"healthy"}'
            elif cmd == 'stop':
                logger.info(" # Received \"stop\" command")
                sent_msg = '{"state":"Bye"}'
                ret_ = False
            elif cmd == 'run':
                if func:
                    stt_time = time.time()
                    resp = func(dict_dat['request'], logger=logger)
                    proc_time = time.time() - stt_time
                else:
                    resp, proc_time = None, 0
                sent_msg = json.dumps({"state": "Done", "response": resp, "proc_time": proc_time})
            else:
                logger.error(" @ Invalid command, {}.".format(cmd))
                sent_msg = '{"state":"Invalid"}'
        else:
            sent_msg = '{"state":"Not json"}'
    except Exception as e:
        logger.error(str(e) + "\n" + traceback.format_exc())
        sent_msg = '{"state":"' + str(e) + '"}'

    finally:
        if response_:
            con.sendall(sent_msg.encode('utf-8'))
            logger.info(" # Sent: {:d} bytes, {}".format(len(sent_msg), sent_msg))
        con.close()

    return ret_, dict_dat, sent_msg


def recv_all(con, recv_buf_size=1024, timeout_val=60,
             data_len_list=None, prefix=" # recv_all #", logger=utils.get_stdout_logger()):
    byte_data = b''
    while True:
        try:
            con.settimeout(timeout_val)
            part = con.recv(recv_buf_size)
            if logger:
                logger.info("{} {:d} : {}".format(prefix, len(part), str(part)))
                pass
            if len(part) > 0:
                byte_data += part
                if utils.is_json(byte_data):
                    break
                if data_len_list:
                    try:
                        if data_len_list.index(len(byte_data)) >= 0:
                            if logger:
                                logger.info("{} Total packet length is {:d}".format(prefix, len(byte_data)))
                                pass
                            return byte_data
                    except ValueError:
                        pass
            else:
                break
        except Exception as err:
            if logger:
                logger.error(str(err) + "\n" + traceback.format_exc())
            break

    return byte_data


def run_command_server(server,
                       func=None,
                       response_=True,
                       logger=utils.get_stdout_logger()):

    sock = get_server_socket(server.ip, server.port,
                             logger=logger,
                             server_name=server.name,
                             listen_num=server.listen_num)

    while True:
        try:
            ret, _, _ = handle_command_request(sock, func=func, response_=response_, logger=logger)
            if not ret:
                break
        except Exception as e:
            logger.error(" # handle_command_request.exception : {}".format(e))
            try:
                sock.close()
            except Exception as c_e:
                logger.error(" # close.exception : {}".format(c_e))
            try:
                sock = get_server_socket(server.ip,
                                         server.port,
                                         logger=logger,
                                         server_name=server.name,
                                         listen_num=server.listen_num)
            except Exception as s_e:
                logger.error(" # get_server_socket.exception : {}".format(s_e))


def send_run_request_and_recv_response(ip,
                                       port,
                                       request,
                                       show_send_dat_=True,
                                       show_recv_dat_=True,
                                       exit_=False,
                                       prefix="",
                                       recv_=True,
                                       logger=utils.get_stdout_logger()):

    send_dat = {"cmd": "run", "request": request}
    ret, recv_dat = send_data_via_socket(ip, port, json.dumps(send_dat),
                                         show_send_dat_=show_send_dat_,
                                         show_recv_dat_=show_recv_dat_,
                                         prefix=prefix,
                                         recv_=recv_,
                                         logger=logger)

    if not ret:
        logger.error(" @ Error in process request and response method : Socket failed. port={}".format(port))
        if exit_:
            sys.exit(1)
        else:
            return None, None

    if recv_:
        assert (recv_dat is not None)

        try:
            recv_dict = json.loads(recv_dat)
        except Exception as e:
            logger.error("{} @ Error: load json : {}".format(prefix, e))
            if exit_:
                sys.exit(1)
            else:
                return None, None

        if not ('state' in recv_dict and 'response' in recv_dict and 'proc_time' in recv_dict):
            logger.error("{} @ Error: unknown format of response, {}".format(prefix, str(recv_dict)))
            return None, None

        if not recv_dict['state'] == "Done":
            logger.error("{} @ Error: state is {}.".format(prefix, recv_dict['state']))
            if exit_:
                sys.exit(1)
            else:
                return None, None

        return recv_dict['response'], recv_dict['proc_time']

    else:
        return recv_dat, None


def send_request_and_recv_response(ip,
                                   port,
                                   request_data,
                                   show_send_dat_=True,
                                   show_recv_dat_=True,
                                   exit_=False,
                                   prefix="",
                                   recv_=True,
                                   timeout_val=60.,
                                   logger=utils.get_stdout_logger()):

    ret, recv_dat = send_data_via_socket(ip, port, json.dumps(request_data),
                                         show_send_dat_=show_send_dat_,
                                         show_recv_dat_=show_recv_dat_,
                                         prefix=prefix,
                                         recv_=recv_,
                                         timeout_val=timeout_val,
                                         logger=logger)
    if not ret:
        logger.error(" @ Error in process request and response method : Socket failed. port={}".format(port))
        if exit_:
            sys.exit(1)
        else:
            return None

    if recv_:
        assert (recv_dat is not None)

        try:
            return json.loads(recv_dat)
        except Exception as e:
            logger.error("{} @ Error: load json : {}".format(prefix, e))
            if exit_:
                sys.exit(1)
            else:
                return None
    else:
        return None
