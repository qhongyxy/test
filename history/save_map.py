from __future__ import division

import sys
import math
import random
import time
import json  # 导入 JSON 模块进行序列化和反序列化
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

TICKS_PER_SEC = 60
SECTOR_SIZE = 16
WALKING_SPEED = 5
FLYING_SPEED = 15
GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50
PLAYER_HEIGHT = 2

if sys.version_info[0] >= 3:
    xrange = range

def cube_vertices(x, y, z, n):
    return [
        x - n, y + n, z - n, x - n, y + n, z + n, x + n, y + n, z + n, x + n, y + n, z - n,
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n,
    ]

def tex_coord(x, y, n=4):
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

TEXTURE_PATH = 'texture.png'

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [
    (0, 1, 0),
    (0, -1, 0),
    (-1, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (0, 0, -1),
]

def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def sectorize(position):
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)

class Model(object):

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        self.world = {}
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = deque()
        self._initialize()
        self.entities = {}
        self.batch = pyglet.graphics.Batch()
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        # 初始化 camera_sector 属性
        self.camera_sector = None

    def change_sectors(self, before, after):
        if before != after:
            if before is not None:
                before.visible = False
            if after is not None:
                after.visible = True
                for e in after.entities:
                    self.entities[e].visible = True
            self.camera_sector = after


    def _initialize(self):
        n = 80
        s = 1
        y = 0
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                self.add_block((x, y - 2, z), GRASS, immediate=False)
                self.add_block((x, y - 3, z), STONE, immediate=False)
                if x in (-n, n) or z in (-n, n):
                    for dy in xrange(-2, 3):
                        self.add_block((x, y + dy, z), STONE, immediate=False)
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o)
            b = random.randint(-o, o)
            c = -1
            h = random.randint(1, 6)
            s = random.randint(4, 8)
            d = 1
            t = random.choice([BRICK, SAND])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (y - c) ** 2 + (z - b) ** 2 < (s + 1) ** 2:
                            self.add_block((x, y, z), t, immediate=False)
                s -= d
                d = 0

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                if self.world[key]:
                    return key
                previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None

    def exposed(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            self.show_block(position, texture)

    def remove_block(self, position, immediate=True):
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            self.hide_block(position)

    def show_block(self, position, texture):
        self.shown[position] = texture
        self._show_block(position, texture)

    def _show_block(self, position, texture):
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        self.batch.add(24, GL_QUADS, self.group,
                        ('v3f/static', vertex_data),
                        ('t2f/static', texture_data))

    def hide_block(self, position):
        del self.shown[position]
        self._hide_block(position)

    def _hide_block(self, position):
        self.batch.vertices[:] = [0] * len(self.batch.vertices)
        self.batch.tex_coords[:] = [0] * len(self.batch.tex_coords)

    def show_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, self.world[position])

    def hide_sector(self, sector):
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position)

    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 2
        for dx in xrange(-pad, pad + 1):
            for dy in [-1, 0, 1]:
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        for sector in after_set - before_set:
            self.show_sector(sector)
        for sector in before_set - after_set:
            self.hide_sector(sector)

    def process_queue(self):
        for _ in xrange(8):
            try:
                position, texture = self.queue.popleft()
            except IndexError:
                return
            self.add_block(position, texture, False)

    def process_entire_queue(self):
        while len(self.queue) > 0:
            self.process_queue()

    def enqueue(self, position, texture):
        self.queue.append((position, texture))

    def save_game_state(self, filename):  # 添加保存游戏状态的方法
        with open(filename, 'w') as f:
            json.dump(self.world, f)

    def load_game_state(self, filename):  # 添加加载游戏状态的方法
        with open(filename, 'r') as f:
            self.world = json.load(f)
        # 重新初始化显示和区块数据
        self.shown = {}
        self._shown = {}
        self.sectors = {}
        self.queue = deque()
        self._initialize()
        # 处理显示的队列，以确保重新加载的世界正确显示
        self.process_entire_queue()

class Player(object):

    def __init__(self, model, position=(0, 0, 0), rotation=(0, 0)):
        self.position = list(position)
        self.rotation = list(rotation)
        self.model = model
        self.dy = 0  # 添加dy属性，并初始化为0
    def mouse_motion(self, dx, dy):
        dx /= 8
        dy /= 8
        self.rotation[0] += dy
        self.rotation[1] -= dx
        self.rotation[0] = max(-90, min(90, self.rotation[0]))

    def update(self, dt, keys):
        speed = (WALKING_SPEED if keys[key.LSHIFT] or keys[key.RSHIFT] else FLYING_SPEED) * dt
        d = math.cos(math.radians(self.rotation[0]))
        x, y, z = self.position
        dx, dy, dz = speed * d * math.sin(math.radians(self.rotation[1])), speed * math.sin(math.radians(self.rotation[0])), speed * d * math.cos(math.radians(self.rotation[1]))
        if keys[key.W]:
            x, z = x - dx, z + dz
        if keys[key.S]:
            x, z = x + dx, z - dz
        if keys[key.A]:
            x, z = x + dz, z + dx
        if keys[key.D]:
            x, z = x - dz, z - dx
        if keys[key.SPACE]:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        if keys[key.LCTRL]:
            self.dy = -JUMP_SPEED
        self.dy -= GRAVITY * dt
        self.position[0] = x
        self.position[1] += self.dy * dt
        self.position[2] = z
        self.model.process_queue()
        self.model.change_sectors(self.model.camera_sector, sectorize(self.position))
        self.model.process_entire_queue()

class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.exclusive = False
        self.flying = False
        self.position = (0, 0, 0)
        self.rotation = (0, 0)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        self.model = Model()
        self.player = Player(self.model, position=(0, 10, 0))

    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            self.player.mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.set_exclusive_mouse(not self.exclusive)
        elif KEY == key.F:
            self.flying = not self.flying
        elif KEY == key.TAB:
            self.model.save_game_state("save.json")  # 按下 TAB 键保存游戏状态

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.model.batch.draw()

    def set3d(self):
        width, height = self.get_size()
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.player.rotation
        glRotatef(x, 1, 0, 0)
        glRotatef(y, 0, 1, 0)
        x, y, z = self.player.position
        glTranslatef(-x, -y, -z)

if __name__ == '__main__':
    window = Window(width=800, height=600, caption='Minecraft', resizable=True)
    pyglet.app.run()