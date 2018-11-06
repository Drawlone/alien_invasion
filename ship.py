#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pygame


class Ship:

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置初始位置"""
        self.screen = screen

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        # 画板screen位置确定后，元素的位置均用画板screen属性来确定
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 以浮点数来计算位置，可应对浮点数的速率，然后传给centerx
        # centerx只接受整数部分，这样误差小
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘飞船"""
        self.screen.blit(self.image, self.rect)