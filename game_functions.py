#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys

import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    # 外星人间距为外星人宽度
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width  # 两边各留一个alien_width的间距
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人
    # 击中则删除外星人和子弹
    # 使用sprite检测碰撞函数
    # 两个True表示检测到两个Group中对象有碰撞时，均删除
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并创建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings, ship, aliens):
    """更新外星人群中所有外星人位置"""
    check_fleet_edges(ai_settings, aliens)

    # Sprite和Group的组合拳体现在这里，alien类继承了Sprite
    # 并且重写了update，这样Group对象可一句话调用所有alien对象的update()
    aliens.update()

    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹位置，并删除已消失子弹"""
    bullets.update()
    # 删除已经消失的子弹
    # 不可以在遍历编组时删除该编组的条目，常识！
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def update_screen(ai_settings, screen, ship, bullets, aliens):
    """更新屏幕图像，并切换到新图像"""
    # 每次循环重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for alien in aliens:
        alien.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()





