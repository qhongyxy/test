import pyglet
from pyglet import media
from pyglet.gl import *

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
play_music()

# 创建一个窗口对象
window = pyglet.window.Window(width=800, height=600, caption='Pyglet Music Player')

@window.event
def on_draw():
    window.clear()
    label = pyglet.text.Label('Playing Music', font_size=36,
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')
    label.draw()

# 保持应用程序的事件循环运行
pyglet.app.run()
