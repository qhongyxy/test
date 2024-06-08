from __future__ import division
import json
import sys
import math
import random
import time
# from OpenGL.GL import *
# from OpenGL.GLU import *
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
TICKS_PER_SEC = 60

# 用于简化方块加载的扇区大小。
SECTOR_SIZE = 16    # 方块大小
WALKING_SPEED = 5   # 走路速度
FLYING_SPEED = 15   # 飞行速度

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # 大约一个方块的高度。
# 推导出计算跳跃速度的公式，首先解
#    v_t = v_0 + a * t
# 计算达到最大高度时的时间，其中 a 是由重力引起的加速度， v_t = 0。这给出：
#    t = - v_0 / a
# 使用 t 和期望的 MAX_JUMP_HEIGHT 解出 v_0（跳跃速度）在
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

if sys.version_info[0] >= 3:
    xrange = range
def cube_vertices(x, y, z, n):
    """ 返回位置为 x、y、z 大小为 2*n 的立方体的顶点坐标。"""
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # 顶面
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # 底面
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # 左侧
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # 右侧
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # 前侧
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # 后侧
    ]
def tex_coord(x, y, n=8):
    """ 返回纹理方块的边界顶点。"""
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m
def tex_coords(top, bottom, side):
    """ 返回顶部、底部和侧面的纹理坐标列表。 """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result
TEXTURE_PATH = 'texture.png'
Dirt = tex_coords((0, 1), (0, 1), (0, 1))  # ABC为泥土
WOOD  = tex_coords((7, 0), (7, 0), (0, 2))
GRASS = tex_coords((1, 0), (0, 1), (0, 0))#草方块
SAND = tex_coords((1, 1), (1, 1), (1, 1))
hot_wood =  tex_coords((7, 0), (7, 0), (4, 1))
water = tex_coords((1, 2), (1, 2), (1, 2))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))
# 新建泥土方块

Oak_Leaves = tex_coords((1, 0), (1, 0), (1, 0))  # CAO为草
SNOW =  tex_coords((3, 1), (3, 1), (3, 1))
Andesite = tex_coords((4, 0), (4, 0), (4, 0))
Red_Mushroom_Block = tex_coords((5, 0), (5, 0), (5, 0))
Pumpkin = tex_coords((6, 0), (6, 0), (6, 0))
spruce_board = tex_coords((5, 1), (5, 1), (5, 1))
tropical_board = tex_coords((6, 1), (6, 1), (6, 1))
AIR = None


FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
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
        # Batch 用于批量渲染的顶点列表集合。
        self.batch = pyglet.graphics.Batch()
        # TextureGroup 管理一个 OpenGL 纹理。
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        # 从位置到该位置方块的纹理的映射。
        # 这定义了当前在世界中的所有方块。
        self.world = {}
        # 与 `world` 相同的映射，但只包含显示的方块。
        self.shown = {}
        # 从位置到所有显示方块的 pyglet `VertexList` 的映射。
        self._shown = {}
        # 从扇区到该扇区内的位置列表的映射。
        self.sectors = {}
        # 简单的函数队列实现。队列填充有 _show_block() 和 _hide_block() 调用
        self.queue = deque()
        self._initialize()

    def _initialize(self):
        """ 通过放置所有方块来初始化世界。"""
        n = 160  # 世界宽度和高度的一半
        s = 1  # 步长
        y = 0  # 初始 y 高度
        # 随机生成矿洞
        for _ in xrange(50):  # 生成50个矿洞
            x_cave = random.randint(-n, n)
            z_cave = random.randint(-n, n)
            y_cave = random.randint(-10, -5)  # 矿洞生成在地下
            self.generate_cave((x_cave, y_cave, z_cave))
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # 生成空气方块，确保可以在山的内部生成矿洞

                # 最底层用安山岩铺一层
                self.add_block((x, y - 11, z), Andesite, immediate=False)
                # 上面十层用石头
                for dy in xrange(-10, 0):
                    self.add_block((x, y + dy, z), STONE, immediate=False)
                # 地表铺不同方块
                if x in (-n, n) or z in (-n, n):
                    # 创建外部墙壁
                    for dy in xrange(-2, 3):
                        self.add_block((x, y + dy, z), STONE, immediate=False)
                # 西北区域用沙子覆盖
                if x <= 0 and z < 0:
                    self.add_block((x, y, z), SAND, immediate=False)
                # 东北区域用雪覆盖
                if x > 0 and z < 0:
                    self.add_block((x, y, z), SNOW, immediate=False)
                # 东南区域用草地覆盖
                if x > 0 and z >= 0:
                    self.add_block((x, y, z), GRASS, immediate=False)
                # 西南区域用草地覆盖
                if x <= 0 and z >= 0:
                    self.add_block((x, y, z), GRASS, immediate=False)

        # 随机生成地形
        o = n - 10

        # 东南平原生成平缓大的山
        for _ in xrange(120):
            a = random.randint(0, o)  # 山丘的 x 位置
            b = random.randint(0, o)  # 山丘的 z 位置
            c = 0  # 山丘的基地
            h = random.randint(1, 5)  # 山丘的高度
            s = random.randint(8, 16)  # 2 * s 是山丘的边长
            d = 1  # 山丘如何快速变薄
            t = random.choice([GRASS])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # 减小边长以使山丘逐渐变薄

        # 西南山地生成陡峭的山
        for _ in xrange(120):
            a = random.randint(-o, 0)  # 山丘的 x 位置
            b = random.randint(0, o)  # 山丘的 z 位置
            c = 0  # 山丘的基地
            h = random.randint(7, 12)  # 山丘的高度
            s = random.randint(8, 16)  # 2 * s 是山丘的边长
            t = random.choice([GRASS])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                        self.generate_cave((x, y, z))
                # 随机减少宽度以使山丘变薄
                if random.random() > 0.5:
                    s -= random.randint(0, 2)
                else:
                    s -= random.randint(2, 5)

        # 东北区域生成雪山
        for _ in xrange(120):
            a = random.randint(0, o)  # 山丘的 x 位置
            b = random.randint(-o, 0)  # 山丘的 z 位置
            c = 0  # 山丘的基地
            h = random.randint(12, 20)  # 山丘的高度
            s = random.randint(16, 24)  # 2 * s 是山丘的边长
            d = 3  # 山丘如何快速变薄
            t = random.choice([SNOW])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                        # 随机生成矿洞
                        if random.random() < 0.9:  # 控制生成矿洞的概率
                            self.generate_cave((x, y, z))
                # 随机减少宽度以使山丘变薄
                if random.random() > 0.5:
                    s -= random.randint(0, 2)
                else:
                    s -= random.randint(2, 5)
            s -= d  # 减小边长以使山丘逐渐变薄

        # 西北区域生成沙丘
        for _ in xrange(60):
            a = random.randint(-o, 0)  # 山丘的 x 位置
            b = random.randint(-o, 0)  # 山丘的 z 位置
            c = 0  # 山丘的基地
            h = random.randint(1, 5)  # 山丘的高度
            s = random.randint(8, 16)  # 2 * s 是山丘的边长
            d = 1  # 山丘如何快速变薄
            t = random.choice([SAND])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # 减小边长以使山丘逐渐变薄

        # 随机生成树，仅限于地图的东南方向
        for _ in xrange(100):  # 生成100棵树
            a = random.randint(-o, o)  # 树的 x 位置，限定为正值（东）
            b = random.randint(0, o)  # 树的 z 位置，限定为正值（南）
            c = 0  # 树的基地
            self.add_tree((a, c, b),WOOD,Oak_Leaves,9,15,True)
        for _ in xrange(100):  # 生成100棵树
            a = random.randint(-o, o)  # 树的 x 位置，限定为正值（东）
            b = random.randint(0, o)  # 树的 z 位置，限定为正值（南）
            c = 0  # 树的基地
            self.add_tree((a, c, b),hot_wood,Oak_Leaves,9,15,True)
        #随机生长蘑菇
        for _ in xrange(50):  # 生成100棵树
            a = random.randint(-o, o)  # 树的 x 位置，限定为正值（东）
            b = random.randint(0, o)  # 树的 z 位置，限定为正值（南）
            c = 0  # 树的基地
            self.add_tree((a, c, b),Red_Mushroom_Block,Red_Mushroom_Block,12,24,False)
        #随机生长南瓜
        for _ in xrange(50):  # 生成100棵树
            a = random.randint(-o, o)  # 树的 x 位置，限定为正值（东）
            b = random.randint(0, o)  # 树的 z 位置，限定为正值（南）
            c = 0  # 树的基地
            self.add_diamond((a, c, b),Pumpkin,Pumpkin,5,9)
            # 随机石块
        for _ in xrange(200):  #
            a = random.randint(-o, o)  # 树的 x 位置，限定为正值（东）
            b = random.randint(-o, 0)  # 树的 z 位置，限定为正值（南）
            c = 0  # 树的基地
            self.add_diamond((a, c, b), Andesite, Andesite, 5, 9)

    def add_diamond(self, position,wen,li,minheight, maxheight):
        """ 在指定位置添加一棵树。 """
        x, y, z = position
        height = random.randint(minheight, maxheight)  # 随机生成树的高度
        # 添加树干
        for i in range(height):
            self.add_block((x, y + i, z), wen, immediate=False)


    def generate_cave(self, position):
        """ 生成一个矿洞。"""
        x, y, z = position
        cave_length = random.randint(5, 15)
        for _ in range(cave_length):
            if abs(x - position[0]) > 10 or abs(y - position[1]) > 4 or abs(z - position[2]) > 10:
                break

            self.add_block((x, y, z), AIR, immediate=False)
            # 随机方向延伸矿洞
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            z += random.randint(-1, 1)

    def add_tree(self, position,wen,li,minheight, maxheight,heightll):
        """ 在指定位置添加一棵树。 """
        x, y, z = position
        height = random.randint(minheight, maxheight)  # 随机生成树的高度
        # 添加树干
        for i in range(height):
            self.add_block((x, y + i-1, z), wen, immediate=False)
        # 添加树叶
        leaf_height = 4
        if  heightll == True:
            height_leaf = -leaf_height
        else:
            height_leaf = 0
        for dy in range(height_leaf, leaf_height + 1):
            for dx in range(-leaf_height, leaf_height + 1):
                for dz in range(-leaf_height, leaf_height + 1):
                    if abs(dx) + abs(dy) + abs(dz) <= leaf_height + 1:
                        self.add_block((x + dx, y + height + dy, z + dz), li, immediate=False)

    def hit_test(self, position, vector, max_distance=8):
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
    def exposed(self, position):
        """ 如果给定的 `position` 在 6 个方向都被方块包围，则返回 False，否则返回 True。"""
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False
    def add_block(self, position, texture, immediate=True):
        if texture is None:
            return  # 跳过 AIR 方块
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)
    def remove_block(self, position, immediate=True):
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)
    def show_block(self, position, immediate=True):
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)
    def _show_block(self, position, texture):
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        if texture is None:
            return  # 跳过 AIR 方块
        texture_data = list(texture)
        # 创建顶点列表
        # 或许应该使用 `add_indexed()` 代替？
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))
    def hide_block(self, position, immediate=True):
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)
    def _hide_block(self, position):
        """ 'hide_block()` 方法的私有实现。 """
        self._shown.pop(position).delete()
    def show_sector(self, sector):
        """ 确保给定扇区中应该显示的所有方块都绘制到画布上。 """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)
    def hide_sector(self, sector):
        """ 确保给定扇区中应该隐藏的所有方块都从画布上移除。 """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)
    def change_sectors(self, before, after):
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)
    def _enqueue(self, func, *args):
        self.queue.append((func, args))
    def _dequeue(self):
        func, args = self.queue.popleft()
        func(*args)
    def process_queue(self):
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()
    def process_entire_queue(self):
        """ 处理整个队列，没有中断。 """
        while self.queue:
            self._dequeue()
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