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

WOOD  = tex_coords((0, 2), (0, 2), (0, 2))
GRASS = tex_coords((1, 0), (0, 1), (0, 0))#草方块
SAND = tex_coords((1, 1), (1, 1), (1, 1))
hot_wood =  tex_coords((1, 4), (1, 4), (1, 4))
water = tex_coords((1, 2), (1, 2), (1, 2))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))
# 新建泥土方块
Dirt = tex_coords((0, 1), (0, 1), (0, 1))  # ABC为泥土
Oak_Leaves = tex_coords((1, 0), (1, 0), (1, 0))  # CAO为草
SNOW =  tex_coords((3, 1), (3, 1), (3, 1))
Andesite = tex_coords((4, 0), (4, 0), (4, 0))
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
            c = h  # 树的基地
            self.add_tree((a, c, b))



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

    def add_tree(self, position):
        """ 在指定位置添加一棵树。 """
        x, y, z = position
        height = random.randint(7, 15)  # 随机生成树的高度
        # 添加树干
        for i in range(height):
            self.add_block((x, y + i, z), WOOD, immediate=False)
        # 添加树叶
        leaf_height = 4
        for dy in range(-leaf_height, leaf_height + 1):
            for dx in range(-leaf_height, leaf_height + 1):
                for dz in range(-leaf_height, leaf_height + 1):
                    if abs(dx) + abs(dy) + abs(dz) <= leaf_height + 1:
                        self.add_block((x + dx, y + height + dy, z + dz), Oak_Leaves, immediate=False)

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
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 玩家的物品栏
        self.inventory = []  # 初始化 inventory 属性为空列表
        self.inventory_size = 9  # 设置物品栏大小为9，可以根据需要进行调整
        self.inventory_slot_width = 50
        self.inventory_slot_height = 50
        self.inventory_bg_color = (0.2, 0.2, 0.2)  # 物品栏背景颜色
        self.inventory_bg_vertices = None
        self.setup_inventory_background()  # 调用设置物品栏背景的方法
        # 是否独占鼠标
        self.exclusive = True
        # 当飞行时，重力不起作用且速度增加。
        self.flying = True
        # Strafing 是指横向移动，即在继续面向前方的同时向左或向右移动。
        # 第一个元素在向前移动时为 -1，在向后移动时为 1，在其他情况下为 0。
        # 第二个元素在向左移动时为 -1，在向右移动时为 1，在其他情况下为 0。
        self.strafe = [0, 0]
        # 当前世界中的 (x, y, z) 位置，用浮点数指定。请注意，与数学课程中不同，y 轴是垂直轴。
        self.position = (0, 0, 0)
        # 在 x-z 平面（地平面）中的玩家旋转，从 z 轴测量向下。第二个是从地平面向上的旋转角度。旋转以度为单位。
        # 垂直平面旋转范围从 -90（直视向下）到 90（直视向上）。水平旋转范围无界。
        self.rotation = (0, 0)
        # 玩家当前所在的扇区。
        self.sector = None
        # 屏幕中心的准星。
        self.reticle = None
        # 在 y（向上）方向的速度。
        self.dy = 0
        # 玩家可以放置的方块列表。按数字键切换。

        self.inventory = [BRICK, GRASS, SAND, STONE, Dirt, Oak_Leaves,WOOD,water,hot_wood]
        # 用户可以放置的当前方块。按数字键切换。
        self.block = self.inventory[0]
        # 快捷数字键列表。
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]
        # 处理世界的模型实例。
        self.model = Model()
        # 在画布的左上角显示的标签。
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
                                       x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
                                       color=(0, 0, 0, 255))

        # 此调用安排了以 TICKS_PER_SEC 调用 `update()` 方法。这是主游戏事件循环。
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        self.setup_inventory_background()  # 设置物品栏背景

    def set_exclusive_mouse(self, exclusive):
        """设置鼠标是否独占
        参数:
            exclusive (bool): 如果为True，则鼠标将被窗口独占，否则释放。"""
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        """获取视线向量
        返回:
            tuple: 视线向量的 (x, y, z) 分量。"""
        x, y = self.rotation
        # y 范围从 -90 到 90，或者 -pi/2 到 pi/2，所以 m 范围从 0 到 1，
        # 并且在平行于地面的前方时为 1，直视向上或向下时为 0。
        m = math.cos(math.radians(y))
        # dy 范围从 -1 到 1，直视向下时为 -1，直视向上时为 1。
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """获取运动向量返回:tuple: 运动向量的 (x, y, z) 分量。 """
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # 向左或向右移动。
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # 向后移动。
                    dy *= -1
                # 当你在飞行时上下运动时，左右运动会减少。
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)
    def update(self, dt):
        """更新窗口状态参数:dt (float): 时间间隔，以秒为单位。"""
        self.model.process_queue()
        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)
    def _update(self, dt):
        """内部更新方法参数:dt (float): 时间间隔，以秒为单位。"""
        # 行走速度
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        d = dt * speed  # 每个 tick 移动的距离。
        dx, dy, dz = self.get_motion_vector()
        # 空间中的新位置，还未考虑重力。
        dx, dy, dz = dx * d, dy * d, dz * d
        # 重力
        if not self.flying:
            # 更新垂直速度：如果你正在下落，则加速直到达到终端速度；
            # 如果你在跳跃，则减速直到开始下落。
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        # 碰撞检测
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

    def collide(self, position, height):
        """处理碰撞检测参数:position (tuple): 碰撞检测前的位置。height (int): 碰撞检测的高度。返回:tuple: 处理碰撞检测后的位置。"""
        # 你需要在周围方块的尺寸上有多少重叠才算是碰撞。如果为 0，那么任何接触地形都算是碰撞。
        # 如果为 .49，则你会陷入地面，就像走在高草中一样。如果大于等于 .5，则你会掉到地面下面。
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # 检查所有周围
            for i in xrange(3):  # 检查每个维度
                if not face[i]:
                    continue
                # 与这个维度的重叠程度。
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # 检查每个高度
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # 你正在与地面或天花板碰撞，所以停止
                        # 下降/上升。
                        self.dy = 0
                    break
        return tuple(p)
    def on_mouse_press(self, x, y, button, modifiers):
        """处理鼠标按下事件。Parameters:x (int): 鼠标点击的x坐标。 y (int): 鼠标点击的y坐标。button (int): 鼠标按下的按钮。modifiers (int): 按下的修饰键。  """
        if self.exclusive:
            # 获取玩家朝向的矢量
            vector = self.get_sight_vector()
            # 进行碰撞检测
            block, previous = self.model.hit_test(self.position, vector)
            # 右键或Ctrl+左键，放置方块
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                if previous:
                    self.model.add_block(previous, self.block)
            # 左键，移除方块
            elif button == pyglet.window.mouse.LEFT and block:
                texture = self.model.world[block]
                if texture != Andesite:
                    self.model.remove_block(block)
        else:
            self.set_exclusive_mouse(True)
    def on_mouse_motion(self, x, y, dx, dy):
        """处理鼠标移动事件。Parameters: x (int): 当前鼠标的x坐标。y (int): 当前鼠标的y坐标。 dx (int): 鼠标在x轴上的移动量。dy (int): 鼠标在y轴上的移动量。"""
        if self.exclusive:
            # 鼠标灵敏度
            m = 0.15
            x, y = self.rotation
            # 更新玩家的旋转角度
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)
    def on_key_press(self, symbol, modifiers):
        """处理键盘按下事件。Parameters:symbol (int): 按键的符号。modifiers (int): 按下的修饰键。"""
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        elif symbol == key.S and modifiers & key.MOD_CTRL:
            save_game_state('save_game.json', game_state)
        elif symbol == key.L and modifiers & key.MOD_CTRL:
            game_state = load_game_state('save_game.json')
    def on_key_release(self, symbol, modifiers):
        """处理键盘释放事件。Parameters:symbol (int): 释放的按键符号。modifiers (int): 释放时的修饰键。"""
        if symbol == key.W:
            self.strafe[0] = 0
        elif symbol == key.S:
            self.strafe[0] = 0
        elif symbol == key.A:
            self.strafe[1] = 0
        elif symbol == key.D:
            self.strafe[1] = 0
    def on_resize(self, width, height):
        """处理窗口大小改变事件。  Parameters:width (int): 窗口的新宽度。height (int): 窗口的新高度。"""
        # 调整标签位置
        self.label.y = height - 10
        # 调整准星位置
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
                                                   ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
                                                   )
    def set_2d(self):
        """配置OpenGL绘制2D图形。"""
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    def set_3d(self):
        """配置OpenGL绘制3D图形。"""
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)
    def on_draw(self):
        """由pyglet调用以绘制画布。"""
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()  # 切换到2D绘制模式
        self.draw_inventory_background()  # 绘制物品栏背景
        self.draw_label()
        self.draw_reticle()
    def draw_inventory_background(self):
        """绘制物品栏背景。"""
        # 绘制背景矩形
        glColor3d(*self.inventory_bg_color)
        pyglet.graphics.draw(4, GL_QUADS, ('v2f', self.inventory_bg_vertices))
        # 绘制每个物品栏的外框
        for i in range(self.inventory_size):
            x = (self.width - self.inventory_size * self.inventory_slot_width) // 2 + i * self.inventory_slot_width
            y = 20
            # 计算每个物品栏的顶点
            slot_vertices = (
                x, y,
                x + self.inventory_slot_width, y,
                x + self.inventory_slot_width, y + self.inventory_slot_height,
                x, y + self.inventory_slot_height
            )
            # 绘制每个物品栏外框为白色线条
            glColor3d(1, 1, 1)
            pyglet.graphics.draw(4, GL_LINE_LOOP, ('v2f', slot_vertices))
    def draw_focused_block(self):
        """在当前准星下方绘制黑色边框的方块。"""
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    def draw_label(self):
        """在屏幕左上角绘制标签。"""
        x, y, z = self.position
        # 标签显示当前帧率、位置坐标以及显示的方块数量
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.draw()
    def draw_reticle(self):
        """绘制准星。"""
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)
    def setup_inventory_background(self):
        """设置物品栏背景。"""
        # 计算物品栏背景矩形的位置和大小
        inventory_bg_x = (self.width - self.inventory_size * self.inventory_slot_width) // 2
        inventory_bg_y = 10
        inventory_bg_width = self.inventory_size * self.inventory_slot_width
        inventory_bg_height = self.inventory_slot_height + 20  # 添加一些内边距
        # 定义物品栏背景矩形的顶点
        self.inventory_bg_vertices = (
            inventory_bg_x, inventory_bg_y,
            inventory_bg_x + inventory_bg_width, inventory_bg_y,
            inventory_bg_x + inventory_bg_width, inventory_bg_y + inventory_bg_height,
            inventory_bg_x, inventory_bg_y + inventory_bg_height
        )
def setup_fog():
    """配置OpenGL雾效果属性。"""
    # 启用雾效果。雾效果“将雾颜色与每个光栅化像素片段的后纹理颜色混合”。
    glEnable(GL_FOG)
    # 设置雾颜色。
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    # 告诉OpenGL我们对渲染速度和质量没有偏好。
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    # 指定用于计算混合因子的方程式。
    glFogi(GL_FOG_MODE, GL_LINEAR)
    # 雾开始和结束的距离。开始和结束越接近，雾范围内的雾越密集。
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)
class Block:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 0, 0)  # 初始方块的颜色，这里用红色表示
    def draw(self):
        """绘制方块。"""
        pyglet.graphics.draw(4, GL_QUADS, ('v2f', (self.x, self.y, self.x + self.size, self.y, self.x + self.size, self.y + self.size, self.x, self.y + self.size)), ('c3B', self.color * 4))
def setup():
    """基本的OpenGL配置。"""
    # 设置“清除”颜色，即天空的颜色，采用rgba格式。
    glClearColor(0.5, 0.69, 1.0, 1)
    # 启用背面剔除（不渲染）-- 你看不见的面。
    glEnable(GL_CULL_FACE)
    # 设置纹理过滤参数，使用最近邻插值。
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()  # 调用设置雾效果的函数。
def main():
    window = Window(width=1500, height=920, caption='Pyglet', resizable=True)
    # 隐藏鼠标光标并防止鼠标离开窗口。
    window.set_exclusive_mouse(False)
    block = Block(200, 200, 50)  # 创建方块对象
    setup()  # 调用 OpenGL 的基本配置函数
    pyglet.app.run()  # 启动 Pyglet 应用程序
if __name__ == '__main__':
    main()