import asyncio
import datetime
import os
import uuid
import logging

import qpack

from .protocol.package import *
from .version import __version__ as VERSION


class Client:

    def __init__(self, loop, hostname, port, client_type, token,
                 identity_file_path=None, heartbeat_interval=5,
                 client_version=VERSION):
        self.loop = loop
        self._hostname = hostname
        self._port = port
        self._heartbeat_interval = heartbeat_interval
        self._client_type = client_type
        self._client_version = client_version
        self._id = uuid.uuid4().hex
        if identity_file_path is not None:
            enodo_id = self.read_enodo_id(identity_file_path)
            if enodo_id is None or enodo_id == "":
                self.write_enodo_id(identity_file_path, self._id)
            else:
                self._id = enodo_id

        self._token = token
        self._messages = {}

        self._last_heartbeat_send = datetime.datetime.now()
        self._updates_on_heartbeat = []
        self._cbs = None
        self._handshake_data_cb = None
        self._sock = None
        self._running = True
        self._connected = False
        self._read_task = None

    async def setup(self, cbs=None, handshake_cb=None):
        await self._connect()

        self._cbs = cbs
        if cbs is None:
            self._cbs = {}
        if handshake_cb is not None:
            self._handshake_data_cb = handshake_cb

        await self._handshake()

    def read_enodo_id(self, path):
        enodo_id = os.getenv(f"ENODO_ID")
        if not (enodo_id is None or enodo_id == ""):
            return enodo_id
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            enodo_id = f.read()
        return enodo_id

    def write_enodo_id(self, path, enodo_id):
        with open(path, 'w') as f:
            f.write(enodo_id)
        return True

    async def _connect(self):
        while not self._connected and self._running:
            logging.info("Trying to connect")
            try:
                self._sock = await asyncio.open_connection(self._hostname,
                                                           self._port)
            except Exception as e:
                logging.warning(f"Cannot connect, {str(e)}")
                logging.info("Retrying in 5")
                await asyncio.sleep(5)
            else:
                logging.info("Connected")
                self._connected = True

    async def run(self):
        self._read_task = asyncio.Task(self._read_from_socket())
        while self._running:
            diff = datetime.datetime.now() - self._last_heartbeat_send
            if diff.total_seconds() > int(
                    self._heartbeat_interval):
                await self._send_heartbeat()
            await asyncio.sleep(1)

    async def close(self):
        logging.info('Closing the socket')
        self._running = False
        self._read_task.cancel()
        self._sock[1].close()

    async def _read_from_socket(self):
        while self._running:
            packet_type, packet_id, data = await read_packet(self._sock[0])

            if len(data):
                data = qpack.unpackb(data, decode='utf-8')

            if packet_type == 0:
                logging.warning("Connection lost, trying to reconnect")
                self._connected = False
                try:
                    await self.setup(self._cbs)
                except Exception as e:
                    logging.error('Error while trying to setup client')
                    logging.debug(f'Correspondig error: {str(e)}')
                    await asyncio.sleep(5)
            elif packet_type == HANDSHAKE_OK:
                logging.info(f'Hands shaked with hub')
            elif packet_type == HANDSHAKE_FAIL:
                logging.warning(f'Hub does not want to shake hands')
            elif packet_type == HEARTBEAT:
                logging.debug(f'Heartbeat back from hub')
            elif packet_type == RESPONSE_OK:
                logging.debug(f'Hub received update correctly')
            elif packet_type == UNKNOWN_CLIENT:
                logging.error(f'Hub does not recognize us')
                await self._handshake()
            else:
                if packet_type in self._cbs.keys():
                    await self._cbs.get(packet_type)(data)
                else:
                    logging.error(
                        f'Message type not implemented: {packet_type}')

    async def _send_message(self, length, message_type, data):
        header = create_header(length, message_type)

        logging.debug(f"Sending type: {message_type}")
        self._sock[1].write(header + data)

    async def send_message(self, body, message_type, use_qpack=True):
        if not self._connected:
            return False
        if use_qpack:
            body = qpack.packb(body)
        await self._send_message(len(body), message_type, body)

    async def _handshake(self):
        data = {
            'client_id': str(self._id),
            'client_type': self._client_type,
            'token': self._token,
            'version': self._client_version}
        if self._handshake_data_cb is not None:
            handshake_data = await self._handshake_data_cb()
            data = {**data, **handshake_data}
        data = qpack.packb(data)
        await self._send_message(len(data), HANDSHAKE, data)
        self._last_heartbeat_send = datetime.datetime.now()

    async def _send_heartbeat(self):
        logging.debug('Sending heartbeat to hub')
        id_encoded = qpack.packb(self._id)
        await self._send_message(len(id_encoded), HEARTBEAT, id_encoded)
        self._last_heartbeat_send = datetime.datetime.now()
