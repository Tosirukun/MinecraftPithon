import math

from pyglet.gl import *
from pyglet.window import key

import pyglet
from block import Block

class World:

    def __init__(self, blockmanager):
        self.batch = pyglet.graphics.Batch()
        self.blockManager = blockmanager
        for i in range(20):
            for ii in range(20):
                self.addBatch(x=i, y=20, z=ii, sysId="test001")
                for iii in range(3):
                    self.addBatch(x=i, y=19-iii, z=ii, sysId="dirt")
                for iiii in range(10):
                    self.addBatch(x=i, y=16-iiii, z=ii, sysId="stone")

    def addBatch(self, sysId="null", x = 0, y = 0, z = -1):
        blockdata = self.blockManager.getBlock(sysId)
        texture_coordinates = ('t2f', (0,0,
                                       1,0,
                                       1,1,
                                       0,1,))

        #奥
        self.batch.add(4, GL_QUADS, blockdata["oku"],
                       ('v3f', (x,y,z,
                                x,y,z+1,
                                x,y+1,z+1,
                                x,y+1,z,)), texture_coordinates)

        #手前
        self.batch.add(4, GL_QUADS, blockdata["temae"],
                       ('v3f', (x + 1, y, z + 1, x + 1, y, z, x + 1, y + 1, z, x + 1, y + 1, z + 1,)),
                       texture_coordinates)
        # 下面
        self.batch.add(4, GL_QUADS, blockdata["sita"], ('v3f', (x, y, z, x + 1, y, z, x + 1, y, z + 1, x, y, z + 1,)),
                       texture_coordinates)
        # 上面
        self.batch.add(4, GL_QUADS, blockdata["ue"],
                       ('v3f', (x, y + 1, z + 1, x + 1, y + 1, z + 1, x + 1, y + 1, z, x, y + 1, z,)),
                       texture_coordinates)
        # 右側
        self.batch.add(4, GL_QUADS, blockdata["migi"], ('v3f', (x + 1, y, z, x, y, z, x, y + 1, z, x + 1, y + 1, z,)),
                       texture_coordinates)
        # 左側
        self.batch.add(4, GL_QUADS, blockdata["hidari"],
                       ('v3f', (x, y, z + 1, x + 1, y, z + 1, x + 1, y + 1, z + 1, x, y + 1, z + 1,)),
                       texture_coordinates)

    def draw(self):
        self.batch.draw()

    def load_texture(self, path):
        texture = pyglet.image.load(path).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(texture)

class Player:

    def __init__(self, position=(0,0,0), rotation=(0,0)):
        self.position = list(position)
        self.rotation = list(rotation)
        self.tick = 0
        self.velocity_x = 0
        self.velocity_z = 0
        self.velocity_y = 0

    def on_mouse_motion(self, dx, dy):
        sensitivity = 0.1
        self.rotation[0] += dy * sensitivity
        self.rotation[1] -= dx * sensitivity

        dx /= 8
        dy /= 8

        if self.rotation[0] > 90:
            self.rotation[0] = 90
        elif self.rotation[0] < -90:
            self.rotation[0] = -90

    def gravity(self):
        print(self.tick)

    def update(self, dt, keys):
        if keys[key.LCTRL]:
            dt = dt * 1.5
        self.tick += 1
        s = dt * 5

        rotation_y = -self.rotation[1] / 180 * math.pi
        dx = s * math.sin(rotation_y)
        dz = s * math.cos(rotation_y)
        if keys[key.W]:
            self.position[0] += dx
            self.position[2] -= dz
            self.velocity_x += dt * 10
        if keys[key.S]:
            self.position[0] -= dx
            self.position[2] += dz
        if keys[key.A]:
            self.position[0] -= dz
            self.position[2] -= dx
        if keys[key.D]:
            self.position[0] += dz
            self.position[2] += dx

        if keys[key.SPACE]:
            self.position[1] += s
        if keys[key.LSHIFT]:
            self.position[1] -= s

        self.velocity_x -= self.velocity_x / 50
        self.velocity_z -= self.velocity_z / 50
        self.velocity_y -= self.velocity_y / 50

        # 負の値であれば0に戻します
        if self.velocity_x < 0: self.velocity_x = 0
        if self.velocity_z < 0: self.velocity_z = 0
        if self.velocity_y < 0: self.velocity_y = 0

        max_inertia_speed = 0.2  # 値の大きさに比例して滑ります

        # 最大速度を超えていれば最大速度に戻します
        if self.velocity_x > max_inertia_speed: self.velocity_x -= dt * 10.5
        if self.velocity_z > max_inertia_speed: self.velocity_z = max_inertia_speed
        if self.velocity_y > max_inertia_speed: self.velocity_y = max_inertia_speed

        # 前進にはたらく慣性
        self.position[0] += self.velocity_x * dx  # ローテーションを考慮に入れつつ現在の座標に足す
        self.position[2] -= self.velocity_x * dz  # ローテーションを考慮に入れつつ現在の座標から引く

class Window(pyglet.window.Window):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.debugMode = True
        self.BlockManager = Block()
        self.world = World(self.BlockManager)

        self.keys = key.KeyStateHandler()

        self.push_handlers(self.keys)
        self.player = Player((0.5,1.5,1.5), (-30, 0))
        pyglet.clock.schedule(self.update)
        pyglet.clock.schedule_interval(self.update, 1.0/120.0)

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.on_mouse_motion(dx, dy)

    def on_key_press(self, KEY, MOD):
        if KEY == key.ESCAPE:
            self.mouse_lock = not self.mouse_lock

    def update_camera(self, position, rotation):
        glPushMatrix()
        glRotatef(-rotation[0], 1, 0, 0)
        glRotatef(-rotation[1], 0, 1, 0)
        glTranslatef(-position[0], -position[1], -position[2],)

    def mouse_lock(self, enable):
        self.set_exclusive_mouse(enable)
        self.mouse_grabbed = enable

    mouse_grabbed = False
    mouse_lock = property(lambda self: self.mouse_grabbed, mouse_lock)

    def on_draw(self):
        pyglet.clock.tick()
        self.clear()
        self.render_mode_3d()
        self.update_camera(self.player.position, self.player.rotation)
        self.world.draw()
        if self.debugMode:
            print(pyglet.clock.get_fps())
        glPopMatrix()

    def render_mode_3d(self):
        self.render_mode_projection()
            # 視野を設定
        gluPerspective(70, self.width / self.height, 0.05, 1000)
        self.render_mode_modelview()

    def render_mode_2d(self):
        self.render_mode_projection()
       # 描画領域 0からwindow_width、 0からwindow_height
        gluOrtho2D(0, self.width, 0, self.height)
        self.render_mode_modelview()

    def render_mode_projection(self):
        glMatrixMode(GL_PROJECTION)  # 投影変換モード
        glLoadIdentity()  # 変換処理の累積を消去

    def render_mode_modelview(self):
        glMatrixMode(GL_MODELVIEW)  # モデリング変換モード(視野変換)
        glLoadIdentity()  # 変換処理の累積を消去

if __name__ == '__main__':
    pyglet.options['shadow_window'] = False
    window = Window(width=1280, height=720, caption='Minecraft Py', resizable=True)
    glClearColor(0.5, 0.7, 1, 1)  # クリア時の色を空色に設定
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()
