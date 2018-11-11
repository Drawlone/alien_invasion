#!/usr/bin/python3
# -*- coding:utf-8 -*-

class Settings:
    """存储游戏的所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # 飞船速度
        self.ship_speed_factor = 1.5
        # 子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 100  # 外星人撞到屏幕边缘时，向下移动速度
        self.fleet_direction = 1  # 1表示右移，-1表示左移