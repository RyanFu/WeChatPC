# -*- encoding: utf-8 -*-
# !/usr/bin/python3
# @Time   : 2019/3/13 17:17
# @File   : wechat_handle.py
import time

from handle import Handle, InvalidHandleError
from settings import HANDLE_PIXEL_RATIO
from tools.functions import get_img_pix_color


class WeChatPCLoginHandle(Handle):

    def __init__(self):
        class_titles = ["登录", '微信']
        for title_index, class_title in enumerate(class_titles, start=1):
            try:
                self.initial("WeChatLoginWndForPC", class_title, *(None, None, 280, 400))
                break
            except InvalidHandleError:
                if title_index == len(class_titles):
                    self.load_error("没有登陆窗口，请确认您的操作")

    def code_login(self, relative_x=140, relative_y=280):
        """二维码登陆"""
        self.handle_full_screen_shot(image_file_name='code_login.png')
        self.show_screen_shot(key_function=self.check_login, key_params=(relative_x, relative_y))

    def click_login(self, relative_x=140, relative_y=280):
        """点击登陆按钮登录"""
        self.show_handle()
        # wx.handle_full_screen_shot(image_file_name='login.png')
        login_color = wx.get_position_color(relative_x, relative_y)
        # print(login_color)
        if login_color == (26, 173, 25, 255):
            self.mouse_left_click_position(relative_x, relative_y)
        self.check_login(relative_x, relative_y)

    def check_login(self, relative_x, relative_y):
        """登录验证"""
        while 1:
            # wx.handle_full_screen_shot(image_file_name='login.png')
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatMainWndForPC", '微信'):
                    break
            else:
                login_color = wx.get_position_color(relative_x, relative_y)
                print(login_color)
                if login_color != (26, 173, 25, 255):
                    self.code_login()
            self.show_handle()


class WeChatPCHandle(Handle):

    def __init__(self):
        self.initial("WeChatMainWndForPC", "微信", *(None, None, 850, 560))

    def message_list_move2top(self):
        position_x = self.left + 305
        position_y = self.top + 100
        self.mouse_left_click_move(position_x, position_y, position_x, position_y + 100)

        # self.message_list_range_move(10000)

    def message_list_move2bottom(self):
        self.message_list_range_move(10000, move_up=False)
        # position_x = self.left + 180
        # position_y = self.top + 150
        # color = self.get_position_color(position_x, position_y)
        # print(color)

    def message_list_range_move(self, frequency: int, move_up: bool = True):
        self.show_handle()
        time.sleep(0.1)
        position_x = self.left + 180
        position_y = self.top + 150
        for i in range(frequency):
            self.mouse_move_up(position_x, position_y) if move_up else self.mouse_move_down(position_x, position_y)
        self.hidden_handle()

    def menu_more(self):
        self.show_handle()
        self.mouse_left_click_position(30, 535)
        feedback = self.search_children_handle_from_parent('SetMenuWnd')
        print(feedback)
        # menu_handle = WeChatPCMenuHandle()
        # menu_handle.feedback('希望微信PC版出朋友圈功能')
        # print(menu_handle.handler)


class WeChatPCMenuHandle(Handle):

    def __init__(self):
        self.initial("SetMenuWnd", "", *(None, None, 134, 138))

    def feedback(self, message):
        self.show_handle()
        self.mouse_left_click_position(60, 25)

        # feedback.feedback(message)


class WeChatPCFeedbackHandle(Handle):
    def __init__(self):
        self.initial("SetMenuWnd", "", *(None, None, 134, 138))

    def feedback(self, message):
        self.set_text_to_clipboard(message)
        self.show_handle()
        self.mouse_left_click_position(100, 100)
        self.ctrl_v()


class WeChatPCLogoutHandle(Handle):

    def __init__(self):
        self.initial("ConfirmDialog", "微信", *(None, None, 360, 224))

    def logout(self):
        """退出登陆"""
        self.set_handle_foreground()
        self.show_handle()
        self.mouse_left_click_position(225, 190)
        # self.mouse_left_click_position(self.left + 190, self.top + 225)
        self.check_logout()

    def check_logout(self):
        """退出登录验证"""
        while 1:
            if not self.check_handle(self.class_name, self.class_title):
                if self.check_handle("WeChatLoginWndForPC", '微信'):
                    break
                # self.show_handle()
                # color = self.get_position_color(self.left + 64, self.top + 98)
                # print(color)
            # break


if __name__ == '__main__':
    # wx = WeChatPCLogoutHandle()
    # wx.logout()
    # wx = WeChatPCHandle()
    # wx.menu_more()
    wx = WeChatPCLoginHandle()
    wx.handle_full_screen_shot(image_file_name='login.png')
    wx.click_login()

    # print(wx.handler)
    # wx.hidden_handle()
    # wx.show_handle()
    # wx.message_list_move2top()
    # wx.message_list_move2bottom()
