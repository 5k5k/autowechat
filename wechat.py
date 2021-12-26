# coding=utf-8

import configparser
import random
import time
from datetime import datetime

import pyautogui

# 要发送目标名字对应的图片地址
target = 'img/target.png'
# 发送间隔最短时间，单位秒
send_mini_seconds = 1.0
# 发送间隔最长时间，单位秒
send_max_seconds = 2.0
# 发送间隔的随机范围
send_random_duration = send_max_seconds - send_mini_seconds
# 发送图片地址
send = 'img/send.png'
# 表情图标
face = 'img/face.png'
# 左箭头
right_arrow = 'img/right_arrow.png'
# 是否打印控制台日志
print_log = True
# 点击笑脸图标打开的对话框中底部分组图标的宽度+单侧间距，整形
group_icon_width = 48
# 滚动距离
scroll_size = group_icon_width * 2
# 单侧滚动距离
half_scroll_size = int(scroll_size / 2)
# 要发送的表情宽度
icon_width = 80
icon_init_x = 20
icon_init_y = 80

last_right = None

# pyautogui库官方文档
# https://pyautogui.readthedocs.io/en/latest/screenshot.html?highlight=confidence#the-locate-functions


# 加载配置信息
def load_config():
    global print_log, target, send_random_duration, send_mini_seconds, send_max_seconds, group_icon_width
    global scroll_size, half_scroll_size, icon_width
    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    if cf.has_section('base'):
        if cf.has_option('base', 'print_log'):
            print_log = cf.getboolean('base', 'print_log')
        if cf.has_option('base', 'target'):
            target = cf.get('base', 'target')
        if cf.has_option('base', 'send_mini_seconds'):
            send_mini_seconds = cf.getfloat('base', 'send_mini_seconds')
        if cf.has_option('base', 'send_max_seconds'):
            send_max_seconds = cf.getfloat('base', 'send_max_seconds')
        if cf.has_option('base', 'group_icon_width'):
            group_icon_width = cf.getint('base', 'group_icon_width')
        if cf.has_option('base', 'icon_width'):
            icon_width = cf.getint('base', 'icon_width')

    send_random_duration = send_max_seconds - send_mini_seconds
    scroll_size = group_icon_width * 4
    half_scroll_size = int(scroll_size / 2)
    trace('读取配置：' + ' 发送目标名称图片名 = ' + target)


# 如果目标存在发送表情
def check_to_send():
    if check_target_open():
        trace('准备发表情')
        click_face()


# 点击表情图标
def click_face():
    face_location = get_img_center_location(face)
    if face_location is not None:
        click_left(face_location)
        move_to_right_arrow(face_location)


# 移动到右箭头
def move_to_right_arrow(face_location):
    global last_right
    right_arrow_position = get_img_center_location(right_arrow)
    if right_arrow_position is None:
        right_arrow_position = last_right
    if right_arrow_position is not None:
        last_right = right_arrow_position
        x = right_arrow_position.x - group_icon_width * (1 + next_int(5))
        pyautogui.moveTo(x, right_arrow_position.y, duration=0.1)
    else:
        # 这里为表情组太少没有右箭头的情况
        pyautogui.moveTo(face_location.x - 20 + group_icon_width * (next_int(4) - 1), face_location.y - 60,
                         duration=0.1)
    pyautogui.leftClick()
    # click_left(pyautogui.Point(x, right_arrow_position.y))
    scroll_face_groups(right_arrow_position)


# 轮动表情分组，产生随机表情组效果
def scroll_face_groups(right_arrow_position):
    s = next_int(scroll_size) - half_scroll_size
    pyautogui.scroll(s)
    pyautogui.leftClick()
    # pyautogui.moveTo(right_arrow_position.x - icon_init_x - icon_width,
    #                  right_arrow_position.y - icon_init_y - icon_width, duration=0.1)
    position = pyautogui.Point(right_arrow_position.x - icon_init_x - icon_width * next_int(4),
                               right_arrow_position.y - icon_init_y - icon_width * next_int(2))
    # pyautogui.moveTo(position.x, position.y)
    click_left(position)


# 随机下一个整形值
def next_int(integer: int):
    return int(random.random() * integer)


# 点击左键
def click_left(position):
    pyautogui.click(position.x, position.y, clicks=1, interval=0.1, duration=0.1, button="left")


# 检查要发送目标当前的对话框是否打开
def check_target_open():
    target_position = get_img_center_location(target)
    send_position = get_img_center_location(send)
    return target_position is not None and send_position is not None


# 根据图片路径获取图片在屏幕中的中心位置坐标
# 其中的confidence根据官方文档：
# The optional confidence keyword argument specifies the accuracy with
# which the function should locate the image on screen.
# This is helpful in case the function is not able to locate an image due to negligible pixel differences:
# Note: You need to have OpenCV installed for the confidence keyword to work.
# 也就是配置像素差异导致的识别精度变化 需要本机安装OpenCV，本机截图的话估计可以去掉这个参数
def get_img_center_location(img_path):
    return pyautogui.locateCenterOnScreen(img_path, confidence=0.9)


# 打印开关
def trace(message):
    if print_log:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + str(message))


# 随机发送表情
# 不适用于表情包少于一组的情况
if __name__ == '__main__':
    load_config()
    while True:
        check_to_send()
        dur = send_mini_seconds + random.random() * send_random_duration
        time.sleep(dur)
        trace("等待" + str(dur) + "秒\n")
