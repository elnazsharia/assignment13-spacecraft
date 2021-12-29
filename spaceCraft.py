import random
import time
import math
import threading
import arcade

SCREEN_WIDTH = 700
SCREEN_HEHGHT = 700


class Spacecraft(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 30
        self.width = 45
        self.height = 45
        self.angle = 0
        self.change_angle = 20
        self.speed = 4
        self.bullet_list = []
        self.score = 0
        self.heart = 3
        self.heart_image = arcade.load_texture("redheart.png")
        self.fire_sound = arcade.load_sound(":resources:sounds/hurt5.wav")

    def fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(self.fire_sound)

    def rotate(self, key):
        if key == "L":
            self.angle += self.change_angle
        elif key == "R":
            self.angle -= self.change_angle


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png")
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = SCREEN_HEHGHT + 30
        self.width = 45
        self.height = 45
        self.speed = 4

    def move(self):
        self.center_y -= self.speed


class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.center_x = host.center_x
        self.center_y = host.center_y
        self.speed = 10
        self.angle = host.angle

    def move(self):
        a = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(a)
        self.center_y += self.speed * math.cos(a)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEHGHT, "Interstelar Game")
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        self.background_image = arcade.load_texture(
            ":resources:images/backgrounds/stars.png")
        self.me = Spacecraft()
        self.enemy_list = []
        self.change_level = 0.2
        self.game_status = True
        self.destroy_sound = arcade.load_sound(
            ":resources:sounds/explosion2.wav")
        self.my_thread = threading.Thread(target=self.add_enemy)
        self.my_thread.start()

    def add_enemy(self):
        while True:
            time.sleep(random.randint(2, 8))
            self.enemy_list.append(Enemy())
            for enemy in self.enemy_list:
                enemy.speed += self.change_level
            self.change_level += 0.1

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEHGHT, self.background_image)
        self.me.draw()
        for enemy in self.enemy_list:
            enemy.draw()
        for bullet in self.me.bullet_list:
            bullet.draw()
        arcade.draw_text(f"Score: {self.me.score}",
                         600, 20, arcade.color.WHITE, 15)
        for i in range(self.me.heart):
            arcade.draw_lrwh_rectangle_textured(
                30 * i, 10, 28, 26, self.me.heart_image)
        if self.game_status == False:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH // 2, SCREEN_HEHGHT // 2, SCREEN_WIDTH, SCREEN_HEHGHT, arcade.color.BLACK)
            arcade.draw_text("GAME OVER!", SCREEN_WIDTH // 2 -
                             70, SCREEN_HEHGHT // 2, arcade.color.WHITE, 15)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.me.fire()
        if symbol == arcade.key.LEFT:
            self.me.rotate("L")
        if symbol == arcade.key.RIGHT:
            self.me.rotate("R")

    def on_update(self, delta_time: float):
        for enemy in self.enemy_list:
            enemy.move()
            if enemy.center_y < 0:
                self.enemy_list.pop(self.enemy_list.index(enemy))
                self.me.heart -= 1

        for bullet in self.me.bullet_list:
            bullet.move()
            if bullet.center_y > SCREEN_HEHGHT or bullet.center_y < 0 or bullet.center_x > SCREEN_WIDTH or bullet.center_x < 0:
                self.me.bullet_list.pop(self.me.bullet_list.index(bullet))

        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(enemy, bullet):
                    arcade.play_sound(self.destroy_sound)
                    self.me.bullet_list.pop(self.me.bullet_list.index(bullet))
                    self.enemy_list.pop(self.enemy_list.index(enemy))
                    self.me.score += 1

        if self.me.heart < 1:
            self.game_status = False


game = Game()
arcade.run()
