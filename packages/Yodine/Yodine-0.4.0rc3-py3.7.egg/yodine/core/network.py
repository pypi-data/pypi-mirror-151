from .entity import Manager, Component, Entity
from .vector import Vector
from .advjson import json_adv_dump, json_adv_load
from typing import Callable

import time
import uuid
import socket
import trio
import pyglet
import struct
import io


class MultiplayerError(Exception):
    pass


class MultiplayerProtocolError(MultiplayerError):
    pass


class MultiplayerUserError(MultiplayerError):
    pass


class InsufficientData(Exception):
    pass


class NetMessage:
    value_types = {}
    net_types = {}

    @classmethod
    def value_type(cls, vtype):
        cls.net_types[vtype.net_type] = vtype

        if vtype.value_type is not None:
            cls.value_types[vtype.value_type] = vtype

        return vtype

    def __init__(self, manager: Manager, kind, *args):
        self.manager = manager
        self.kind = bytes(kind)
        self.args = [type(self).value_to_net(val) for val in args]

    def header(self):
        kind = self.kind
        return struct.pack(">H", len(kind)) + kind

    @classmethod
    def value_to_net(cls, val):
        return cls.value_types[type(val)](val)

    @classmethod
    def encode_value(cls, val):
        section = val.encode()
        struct.pack(">IH", len(section), len(val.net_type)) + val.net_type + section

    @classmethod
    def decode_value(cls, manager: Manager, stream):
        def safe_read(size):
            res = data.read(size)

            if len(res) != size:
                raise InsufficientData

            return res

        d = stream.read(6)

        if d == b"":
            return None

        elif len(d) != 6:
            raise InsufficientData

        sec_size, ntype_size = struct.unpack(">IH", d)

        ntype = safe_read(ntype_size)
        sec = safe_read(sec_size)

        return cls.net_types[ntype].decode(manager, sec)

    def body(self):
        data = b""
        sects = 0

        for arg in self.args:
            data += self.encode_value(arg)
            sects += 1

        return struct.pack(">H", sects) + data

    def encode(self):
        return self.header() + self.body() + bytes([0, 0])

    def __len__(self):
        return len(self.encode())

    def __iter__(self):
        for arg in self.args:
            yield arg.content(self.manager)

    def __getitem__(self, i):
        return self.args[i].content(self.manager)

    @classmethod
    def decode(cls, manager: Manager, data, ind: int = 0):
        if ind < 0:
            ind = len(data) - ind

        data = io.BytesIO(data)

        if ind > 0:
            data.read(ind)

        def safe_read(size):
            res = data.read(size)

            if len(res) != size:
                raise InsufficientData

            return res

        (hdr_size,) = struct.unpack(">H", safe_read(2))
        kind = data.read(hdr_size)

        (sect_num,) = struct.unpack(">H", safe_read(2))
        args = []

        for _ in range(sect_num):
            args.append(cls.decode_value(manager, data))

        return NetMessage(manager, kind, *args), data.read()


class NetValue:
    net_format = b""
    value_type = None

    def __init__(self, val):
        self.val = val

    def content(self, manager: "Manager"):
        return self.val

    def encode(self):
        return struct.pack(self.net_format, self.val)

    @classmethod
    def decode(cls, manager: "Manager", data):
        return cls(struct.unpack(cls.net_format, data)[0])


@NetMessage.value_type
class NetInt(NetValue):
    net_type = b"INT"
    net_format = ">l"
    value_type = int


@NetMessage.value_type
class NetUInt(NetValue):
    net_type = b"UINT"
    net_format = ">L"


@NetMessage.value_type
class NetFloat(NetValue):
    net_type = b"FLOAT"
    net_format = ">d"
    value_type = float


@NetMessage.value_type
class NetString(NetValue):
    net_type = b"STR"
    value_type = str

    def encode(self):
        return self.val.encode("utf-8")

    @classmethod
    def decode(cls, manager: "Manager", data):
        return NetString(data.decode("utf-8"))


@NetMessage.value_type
class NetBytes(NetValue):
    net_type = b"BYTES"

    def encode(self):
        return self.val

    @classmethod
    def decode(cls, manager: "Manager", data):
        return NetBytes(data)


@NetMessage.value_type
class NetVector:
    net_type = b"VECT"
    value_type = Vector

    def __init__(self, v: Vector):
        self.vector = v

    def content(self, manager: "Manager"):
        return self.vector

    def encode(self):
        return struct.pack(">dd", self.vector.x, self.vector.y)

    @classmethod
    def decode(cls, manager: "Manager", data):
        return NetVector(Vector(*struct.unpack(">dd", data)))


@NetMessage.value_type
class NetComponent:
    net_type = b"COMP"
    value_type = Component

    def __init__(self, comp: Component):
        self.comp = comp

    def content(self, manager: "Manager"):
        return self.comp

    def encode(self):
        return sum(
            (
                NetMessage.encode_value(NetMessage.value_to_net(v))
                for v in (self.comp.entity, self.comp.name, self.comp.value)
            ),
            b"",
        )

    @classmethod
    def decode(cls, manager: "Manager", data):
        stream = io.BytesIO(data)

        entity = NetMessage.decode_value(manager, stream).content(client)
        name = NetMessage.decode_value(manager, stream).content(client)
        cval = NetMessage.decode_value(manager, stream).content(client)

        # load component
        if name in entity:
            comp = entity[name]
            comp.force_set(cval)

        else:
            comp = entity.create_component(name, cval, net=True)

        return NetComponent(comp)


@NetMessage.value_type
class NetEntity:
    net_type = b"ENT"
    value_type = Entity

    def __init__(self, entity: Entity):
        self.entity = entity

    def content(self, manager: "Manager"):
        return self.entity

    def encode(self):
        return self.entity.id.encode("utf-8")

    @classmethod
    def decode(cls, manager: "Manager", data):
        return NetEntity(manager.find_entity(data.decode("utf-8")))


class NetGlobal:
    net_format = b""
    value_type = None

    def __init__(self, _=None):
        pass

    def encode(self):
        return b""

    @classmethod
    def decode(cls, manager: "Manager", data):
        return cls()


@NetMessage.value_type
class NetWindow(NetGlobal):
    net_type = b"WIND"

    def content(self, manager: "Manager"):
        return manager.window


@NetMessage.value_type
class NetList:
    net_type = b"LIST"
    net_format = b""
    value_type = list

    def __init__(self, l: list):
        self.l = l

    def content(self, manager: "Manager"):
        return [a.content(manager) for a in self.l]

    def encode(self):
        return sum((NetMessage.encode_value(v) for v in self.l), b"")

    @classmethod
    def decode(cls, manager: "Manager", data):
        stream = io.BytesIO(data)
        res = []

        while True:
            v = NetMessage.decode_value(manager, stream)

            if not v:
                return NetList(res)

            res.append(v)


@NetMessage.value_type
class NetTuple(NetList):
    net_type = b"TUP"
    net_format = b""
    value_type = tuple

    def __init__(self, l: tuple):
        self.l = list(l)

    def content(self, manager: "Manager"):
        return tuple([a.content(manager) for a in self.l])


@NetMessage.value_type
class NetDict(NetList):
    net_type = b"DIC"
    net_format = b""
    value_type = dict

    def __init__(self, l: dict):
        self.l = list(l.items())

    def content(self, manager: "Manager"):
        return dict(self.l)


class Client:
    def __init__(self, game: "..game.Game", server_addr):
        self.game = game
        self.manager = game.manager
        self.client = socket.create_connection(server_addr)
        self.client.setblocking(False)
        self.addr = server_addr
        self.players = {}
        self.events = []
        self.writes = []
        self.buffer = b""
        self.outbound = b""
        self.running = True
        self.emit_callbacks = {}

        self.average_latency = 0

    def send(self, command, *args):
        self._write(NetMessage(command, *args).encode())

    def emit(self, source, name, *args, **kwargs):
        broad_id = str(uuid.uuid4())
        self.send("BROADCAST", broad_id, source.id, name, args, kwargs)
        when_sent = time.time()

        def _inner(when_received, *args):
            if self.average_latency == 0:
                self.average_latency = when_received

            else:
                self.average_latency = (
                    when_received - when_sent + self.average_latency * 4
                ) / 5

        self.emit_callbacks[broad_id] = _inner

    def stop(self):
        self._write(b"LEAVE\n")
        self.client.close()

        self.running = False

    def process_writes(self):
        nw = []

        for when, data in self.writes:
            self.outbound += data

        self.writes = nw

    def _write(self, data):
        # self.outbound += data
        self.writes.append((time.time(), data))

    async def run(self):
        self.running = True
        self.buffer = b""

        commands = {}

        def command(name):
            def _decorator(func):
                commands[name.upper()] = func

                return func

            return _decorator

        self.ignore_events_until = 0

        @command("DELTA")
        def receive_delta(*changes):
            # print('Received changes!')

            for change in changes:
                args = change[1:]

                if change[0] == "set":
                    eid, cname, cval = args

                    if eid in self.manager:
                        self.manager[eid][cname] = cval

                elif change[0] == "mkc":
                    eid, cname, cval, ckind = args

                    if eid in self.manager:
                        self.manager[eid].create_component(cname, cval, ckind)

                elif change[0] == "del":
                    eid, cname = args

                    if eid in self.manage:
                        e = self.manager[eid]

                        if cname in e:
                            del e[cname]

                elif change[0] == "crt":
                    eid, level = args

                    if level is None:
                        e = self.manager.create_entity([], eid)

                    else:
                        e = self.manager.levels[level].create_entity([], eid)

                elif change[0] == "dsp":
                    (eid,) = args

                    if eid in self.manager:
                        self.manager[eid].remove()

                elif change[0] == "tsf":
                    eid, level = args

                    if eid in self.manager:
                        if level is None:
                            self.manager[eid].transfer(self.manager)

                        else:
                            self.manager[eid].transfer(self.manager.levels[level])

                elif change[0] == "clv":
                    (level,) = args

                    self.manager.change_level(level)

                elif change[0] == "nlv":
                    level, save = args

                    if level not in self.manager.levels:
                        self.manager.add_level_save(level, save)

            print(
                "{} changes at {}".format(len(changes), time.time()).ljust(40), end="\r"
            )

        # @command('EVENT')
        # def receive_broadcast_event(when, local, source, event_name, args, kwargs):
        #    if when <= self.ignore_events_until:
        #        return
        #
        #    if time.time() - when < 1 / 4:
        #        self.manager.emit_local(source, event_name, local, *args, **kwargs)
        #
        #    elif time.time() - when > 2:
        #        self.ignore_events_until = time.time()
        #        self.send('SNAPSHOT')

        @command("ERR")
        def got_error(code, err):
            category = str(code)[0]
            msg = "Status code {}: {}".format(code, err)

            if category == "1":
                raise MultiplayerProtocolError(msg)

            elif category == "2":
                raise MultiplayerUserError(msg)

            else:
                raise MultiplayerError(msg)

        @command("GOT_BROADCAST")
        def broadcast_acknowledged(b_id, *args):
            if b_id in self.emit_callbacks:
                self.emit_callbacks[b_id](*args)

        @command("INIT_LEVELS")
        def init_levels(start, *levels):
            del self.manager.levels
            self.manager.levels = {}

            for v in levels:
                lid = v["lid"]
                assert "deltas" in v

                self.manager.add_level_save(lid, v)

            self.manager.change_level(start)

            print("Received levels.")

        @command("INIT_ENTITIES")
        def init_entities(*entities):
            for e in self.manager:
                e.remove()

            for v in entities:
                eid = v["eid"]
                level = v.get("level", None)
                components = v["components"]

                if level:
                    e = self.manager.levels[level].create_entity(components, eid)

                else:
                    e = self.manager.create_entity(components, eid)

            print("Received {} entities.".format(len(entities)))

        @command("RNG")
        def set_rng_state(*state):
            self.game.random.setstate(state)
            print("Received RNG state.")

        async def _recv(data):
            self.buffer += data

            while self.buffer:
                try:
                    msg, self.buffer = NetMessage.decode(self.manager, self.buffer)

                except InsufficientData:
                    return

                cmd = msg.kind.decode("utf-8").upper()

                if cmd in commands:
                    commands[cmd](*msg)

        print("Joining...")
        self.send("JOIN", self.game.id, self.game.player_name)

        while self.events:
            e = self.events.pop(0)
            self.send_event(e)

        self.events = None

        async with trio.open_nursery() as nursery:
            while self.running:
                sleep_amount = 1 / 30
                data = b""

                try:
                    data = self.client.recv(8192)

                    if data == b"":
                        self.stop()
                        return

                    else:
                        nursery.start_soon(_recv, data)

                except ConnectionResetError:
                    self.stop()
                    return

                except BlockingIOError:
                    sleep_amount = 1 / 15

                self.process_writes()

                try:
                    sent = self.client.send(self.outbound)

                except BlockingIOError:
                    pass

                else:
                    self.outbound = self.outbound[sent:]

                    if self.outbound or len(data) == 8192:
                        sleep_amount = 1 / 60

                await trio.sleep(sleep_amount)

            self.outbound = b""


class Server(object):
    def emit(self, source, event_name, *args, **kwargs):
        for sess in self.clients.keys():
            self.send(sess, "EVENT", self.game.id, source, event_name, args, kwargs)

    def send(self, session, command, *args):
        self._write(session, NetMessage(command, *args).encode())

    def send_deltas(self):
        self.last_t = time.time()

        if self.change_accum:
            for s in self.players.keys():
                # for chg in self.change_accum:
                #    print('delta sent:   ', *chg)

                self.send(s, "DELTA", *self.change_accum)

            self.change_accum = []

    def __init__(self, game: "..game.Game", port: int, player_type: str = "player"):
        self.game = game
        self.manager = game.manager
        self.player_names = set()
        self.clients = {}
        self.players = {}
        self.outbound = {}
        self.writes = {}
        self.locals = {}
        self.change_accum = []
        self.port = int(port)
        self.player_type = player_type
        self.running = False

        self.buffer = ""

    def _write(self, s, data):
        self.writes[s].append((time.time(), data))

    async def accept(self, client: socket.socket, address):
        client.setblocking(0)

        session = str(uuid.uuid4())
        self.outbound[session] = b""
        self.writes[session] = []

        self.players[session] = None
        self.clients[session] = None

        commands = {}

        def _write(data):
            self._write(session, data)

        def error(*args):
            self.send(session, "ERR", *args)

        print("New client connected from:", ":".join(str(x) for x in address))

        async def _recv(data):
            _recv.buffer += data

            while True:
                try:
                    msg, _recv.buffer = NetMessage.decode(self.manager, _recv.buffer)

                except InsufficientData:
                    return

                cmd = msg.kind.decode("utf-8").upper().strip()
                commands[cmd](*msg)

        _recv.buffer = ""

        def command(target_name: str):
            def _decorator(func: Callable):
                commands[target_name] = func
                return func

            return _decorator

        def send_entities():
            loaded = []

            for entity in self.manager:
                comp = [
                    (
                        comp.name,
                        comp.value,
                        type(comp).__name__ if type(comp) is not Component else None,
                    )
                    for comp in entity.get_components()
                ]

                e = {"eid": entity.id, "components": comp}

                if entity.level is not self.manager:
                    e["level"] = entity.level.id

                loaded.append(e)

            self.send(session, "INIT_ENTITIES", *loaded)
            print("Sent entities")

        @command("join")
        def on_join(local_id, name):
            if self.players[session]:
                print("/!\ Already joined:", name)
                error(201, "already joined")

            elif name in self.player_names:
                print("/!\ Name taken:", name)
                error(203, "name taken")

            else:
                p = None

                for e in self.manager:
                    if e.has("name", "localplayer") and e["name"].value == name:
                        p = e
                        p["localplayer"] = local_id
                        break

                lvls = []

                for lid, level in self.manager.levels.items():
                    lvls.append({"lid": lid, "deltas": level.deltas})

                self.send(session, "INIT_LEVELS", self.manager.current_level.id, *lvls)
                send_entities()
                self.send(session, "RNG", *self.game.random.getstate())

                if not p:
                    lvl = self.manager.current_level

                    if not lvl:
                        lvl = self.manager

                    print("Creating player...")
                    p = lvl.create_templated_entity(
                        self.player_type, [("name", name), ("localplayer", local_id)]
                    )

                eid = p.id

                self.players[session] = p
                self.locals[session] = local_id

                print("Joined:", name, "(local: {}, id: {})".format(local_id, eid))

                # Force resending deltas
                if time.time() - self.last_t > update_interval:
                    self.send_deltas()

        @command("snapshot")
        def on_request_snapshot():
            if session in self.players:
                send_entities()

        @command("leave")
        def on_leave():
            if self.players[session] is None:
                error(
                    202,
                    "tried to leave a game the client is already not connected to",
                    "You're just like the kid who's not invited to the party, but comes anyway, and takes a dump in the pool just for the reactions.",
                )
                print("/!\ Not in the game", address)

            else:
                print("Left:", self.players[session]["name"].value)
                self.players[session].remove()

        @command("broadcast")
        def on_event(broadcast_id, source, event_name, args, kwargs):
            local = self.locals[session]

            for sess in self.clients.keys():
                if sess != session:
                    self.send(
                        sess,
                        "EVENT",
                        time.time(),
                        local,
                        source,
                        event_name,
                        args,
                        kwargs,
                    )

            if source not in self.manager.all_entity_ids():
                error(204, "no such entity")

            self.manager.emit_local(
                self.manager[source], event_name, local, *args, **kwargs
            )
            self.send(session, "GOT_BROADCAST", broadcast_id, time.time())

        update_interval = 1 / 12
        self.last_t = time.time()

        async with trio.open_nursery() as nursery:
            while self.running:
                sleep_amount = 1 / 30
                data = b""

                try:
                    data = client.recv(8192)

                    if data == b"":
                        del self.clients[session]

                        if session in self.players:
                            del self.players[session]
                        if session in self.locals:
                            del self.locals[session]

                        return

                    else:
                        nursery.start_soon(_recv, data)

                except (ConnectionResetError, BrokenPipeError):
                    del self.clients[session]

                    if session in self.players:
                        del self.players[session]
                    if session in self.locals:
                        del self.locals[session]

                    return

                except BlockingIOError:
                    sleep_amount = 1 / 20

                if time.time() - self.last_t > update_interval:
                    self.send_deltas()

                self.process_writes(session)

                try:
                    sent = client.send(self.outbound[session])

                except (ConnectionResetError, BrokenPipeError):
                    del self.clients[session]

                    if session in self.players:
                        del self.players[session]
                    if session in self.locals:
                        del self.locals[session]

                    return

                except BlockingIOError:
                    pass

                else:
                    self.outbound[session] = self.outbound[session][sent:]

                    if self.outbound or len(data) == 8192:
                        sleep_amount = 1 / 60

                await trio.sleep(sleep_amount)

    async def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)

        self.running = True

        async with trio.open_nursery() as nursery:
            while self.running:
                try:
                    (conn, addr) = self.socket.accept()

                except BlockingIOError:
                    pass

                else:
                    nursery.start_soon(self.accept, conn, addr)

                await trio.sleep(0.5)

        self.clients = {}

    def stop(self):
        self.running = False
        self.socket.close()

        for s in self.clients.values():
            if s:
                s.close()

    def process_writes(self, s):
        nw = []

        for when, data in self.writes[s]:
            # if time.time() - when > 5:
            #    continue

            self.outbound[s] += data

        self.writes[s] = nw
