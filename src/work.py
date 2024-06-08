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
from pyglet import media
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
from pyglet.media import load, Player

from resource.Model import Model
from resource.Window import Window
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

# 定义播放音乐函数
def play_music():
    global player
    # 定义音乐文件路径列表
    music_sources = [
        'music/Minecraft.mp3',
        'music/Moog_City.flac',
        'music/Subwoofer_Lullaby.flac'
    ]

    # 创建一个播放器对象
    player = media.Player()

    # 循环遍历音乐文件路径列表，加载并将每个音乐文件添加到播放器的播放列表中
    for source in music_sources:
        try:
            music = media.load(source)
            player.queue(music)
            print(f"Loaded music file: {source}")
        except Exception as e:
            print(f"Failed to load music file: {source}. Error: {e}")

    # 播放器设置为循环播放
    player.loop = True

    # 播放音乐
    player.play()
    print("Music playback started")

# 调用播放音乐函数
# play_music()
print(1)
def main():

    window = Window(width=1500, height=920, caption='Pyglet', resizable=True)
    # 隐藏鼠标光标并防止鼠标离开窗口。
    window.set_exclusive_mouse(False)
    block = Block(200, 200, 50)  # 创建方块对象
    setup()  # 调用 OpenGL 的基本配置函数
    play_music()
    pyglet.app.run()  # 启动 Pyglet 应用程序
if __name__ == '__main__':
    main()