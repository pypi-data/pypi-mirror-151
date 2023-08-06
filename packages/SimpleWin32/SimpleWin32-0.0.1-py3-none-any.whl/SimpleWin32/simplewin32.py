import win32api, win32con, win32gui, win32clipboard, win32print
from typing import *


class KeyCode:
    # 字母按键
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90
    # 字母键盘上方数字
    ZERO = 48
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57
    # 小键盘按键
    Number_0 = 96
    Number_1 = 97
    Number_2 = 98
    Number_3 = 99
    Number_4 = 100
    Number_5 = 101
    Number_6 = 102
    Number_7 = 103
    Number_8 = 104
    Number_9 = 105
    MUL = 106
    ADD = 107
    Number_Enter = 108
    SUB = 109
    DecimalPoint = 110      # 小数点
    DIV = 111
    # 字母上方F数字键
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    # 功能按键
    BackSpace = 8
    Tab = 9
    Clear = 12
    Enter = 13
    Shift = 16
    Control = 17
    Alt = 18
    CapeLock = 20
    Esc = 27
    SpaceBar = 32
    PageUp = 33
    PageDown = 34
    End = 35
    Home = 36
    LeftArrow = 37
    UpArrow = 38
    RightArrow = 39
    DownArrow = 40
    Insert = 45
    Delete = 46
    NumLock = 144
    SemicolonOrColon = 186      # 分号和引号";:"
    EqSignOrPluSign = 187       # 等于号和加号"=+"
    Comma = 188                 # 逗号和小于号",<"
    FullStop = 190              # 句号和大于号">."
    Dash = 189                  # 短横线破折号等"- --"
    Slash = 191                 # 斜杠和问号"/?"
    BeakLine = 192              # `~
    LeftSquareBrackets = 219    # {[
    RightSquareBrackets = 221   # ]}
    BackSlash = 220             # \|
    QuotationMark = 222         # '"
    # 多媒体按键
    AddVolume = 175             # 音量加
    SmallVolume = 174           # 音量减
    Stop = 179                  # 停止
    Mute = 173                  # 静音
    Browser = 172               # 浏览器
    Email = 180                 # 邮箱
    Search = 170                # 搜索
    Collect = 171               # 收藏

class MouseEvent:
    """
    部分常用事件集合
    """
    # 鼠标事件
    MOUSELEFT = (win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP)
    MOUSERIGHT = (win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP)
    MOUSEMIDDLE = (win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP)

class __MessageType:
    """
    消息类型集合
    """
    OK = win32con.MB_OK                         # 带OK按钮
    YESNO = win32con.MB_YESNO                   # 带Yes和No按钮
    YESNOCANCEL = win32con.MB_YESNOCANCEL       # 带Yes、No、Cancel按钮
    HELP = win32con.MB_HELP                     # 说明信息
    WARNING = win32con.MB_ICONWARNING           # 警告提示信息
    QUESTION = win32con.MB_ICONQUESTION         # 疑问信息框
    ASTERISK = win32con.MB_ICONASTERISK         # 提示信息框
    OKCANCEL = win32con.MB_OKCANCEL             # 带OK和Cancel的确认框
    RETRYCANCEL = win32con.MB_RETRYCANCEL       # 重试取消信息框
    ERROR = win32con.MB_ICONERROR               # 错误提示框

class Mouse:
    """
    鼠标操作，
    :param x: x轴坐标
    :param y: y轴坐标点
    :param use_dpi: 当前坐标点是否以分辨率为准的，默认为False
    """
    def __init__(self, x, y, use_dpi=False):
        self.x = x
        self.y = y
        self.use_dpi = use_dpi

    def move(self):
        if self.use_dpi is not False:
            scale = Window.ComputerDeviceScale()
            self.x = int(self.x / scale)
            self.y = int(self.y / scale)
        win32api.SetCursorPos((self.x, self.y))
        return self

    def click(self, event=MouseEvent.MOUSELEFT):
        win32api.mouse_event(event[0], 0, 0, 0, 0)
        win32api.mouse_event(event[1], 0, 0, 0, 0)
        return self

class Keyboard:
    """
    需要填写键盘码，可以使用KeyCode类快捷指定
    """
    def __init__(self, keycode):
        self.keycode = keycode

    def click(self):
        win32api.keybd_event(int(self.keycode), 0, 0, 0)
        win32api.keybd_event(int(self.keycode), 0, win32con.KEYEVENTF_KEYUP, 0)
        return self

    def press(self):
        win32api.keybd_event(int(self.keycode), 0, 0, 0)
        return self

    def release(self):
        win32api.keybd_event(int(self.keycode), 0, win32con.KEYEVENTF_KEYUP, 0)
        return self


# 后台事件处理方法
class Message(__MessageType):

    @staticmethod
    def InputMessage(message: str, hwnd=None):
        """
        进行文字输入
        :param hwnd: 窗口句柄，如果为空则视为前台剪贴板粘贴输入，需要窗口在最前端
        :param message: 需要进行输入的信息
        :return:
        """
        if hwnd is None:
            ClipBoard.SetClipboard(message)
            win32api.keybd_event(17, 0, 0, 0)
            win32api.keybd_event(86, 0, 0, 0)
            win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
            ord_str = [ord(x) for x in message]
            for item in ord_str:
                win32api.PostMessage(hwnd, win32con.WM_CHAR, item, 0)

    @staticmethod
    def AlertMessage(message: str, title: str, message_type, hwnd=0):
        """
        弹出窗口信息
        :param message: 消息体
        :param title: 标题
        :param message_type: 消息类型，可使用Message.OK等方式设置
        :param hwnd: 弹窗所属的父级句柄，默认为0
        :return:
        """
        win32gui.MessageBox(hwnd, message, title, message_type)


class ClipBoard:

    @staticmethod
    def SetClipboard(message: str, hwnd=None) -> None:
        """
        设置粘贴板数据
        :param message: 存放到粘贴板的数据信息
        :param hwnd: 窗口句柄
        :return:
        """
        if hwnd is None:
            win32clipboard.OpenClipboard()
        else:
            win32clipboard.OpenClipboard(hwnd)
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(message, win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()

    @staticmethod
    def GetClipboard() -> str:
        """
        获取粘贴板数据
        :return: 粘贴板保存的数据
        """
        data = win32clipboard.GetClipboardData()
        return data


class Window:
    @staticmethod
    def GetSystemMetrics() -> tuple:
        """
        或群当前屏幕尺寸
        :return: 屏幕x,y轴长度
        """
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        return width, height

    @staticmethod
    def GetDeviceCaps() -> tuple:
        """
        获取当前设备分辨率
        :return: 分辨率前后值
        """
        hdc = win32gui.GetDC(0)
        dev_h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
        dev_v = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
        return dev_h, dev_v

    @staticmethod
    def ComputerDeviceScale() -> float:
        """
        获取当前设备的屏幕缩放比
        :return: 当前设备的分辨率和实际尺寸的比率
        """
        size_width = Window.GetSystemMetrics()[0]
        dpi_h = Window.GetDeviceCaps()[0]
        return dpi_h / size_width

    @staticmethod
    def GetAllWindows(father_hwnd=None) -> list:
        """
        获取所有窗口句柄值
        :param father_hwnd: 父级窗口句柄，不输入获取全部一级句柄，输入父级句柄则查找子句柄
        :return: 句柄列表
        """
        if father_hwnd is None:
            windows = []
            win32gui.EnumWindows(lambda hwnd, params: windows.append(hwnd), None)
            return windows
        else:
            child_window = []
            win32gui.EnumChildWindows(father_hwnd, lambda hwnd, params: child_window.append(hwnd), None)
            return child_window

    @staticmethod
    def FindWindow(classname=None, windowtext=None, father_hwnd=None) -> int:
        """
        查找窗口句柄值
        :param classname: 窗口的class值
        :param windowtext: 窗口的标题文字
        :param father_hwnd: 父级句柄，填写后默认为查询子句柄
        :return: 返回窗口的句柄值
        """
        if any([classname, windowtext]):
            if father_hwnd is None:
                window = win32gui.FindWindow(classname, windowtext)
            else:
                window = win32gui.FindWindowEx(father_hwnd, None, classname, windowtext)
            return window
        else:
            raise RuntimeError("Need Parameter: classname or windowtext")

    @staticmethod
    def GetWindowInfo(hwnd_list: Union[List[int], Tuple[int]], classname: bool = False, title: bool = False) -> List[dict]:
        """
        获取窗口信息，class、title
        :param hwnd_list: 需要进行获取的句柄列表(或者元组)
        :param classname: 布尔值，是否获取class
        :param title: 布尔值，是否获取title
        :return: 列表嵌套字典的形式返回
        """
        window_info = []
        if any([classname, title]):
            for handle in hwnd_list:
                if classname is False:
                    title = win32gui.GetWindowText(handle)
                    window_info.append({handle: title})
                elif title is False:
                    classname = win32gui.GetClassName(handle)
                    window_info.append({handle: classname})
                else:
                    title = win32gui.GetWindowText(handle)
                    classname = win32gui.GetClassName(handle)
                    window_info.append({handle: {"title": title, "class": classname}})
            return window_info
        else:
            raise ValueError("Need Parameter: classname or title")

    @staticmethod
    def MoveOrResizeWindow(hwnd, x, y, width, height):
        """
        移动或者调整窗口大小
        :param hwnd: 窗口的句柄
        :param x: 窗口左上角x坐标点
        :param y: 窗口左上角y轴坐标点
        :param width: 窗口的宽
        :param height: 窗口的高
        :return:
        """
        win32gui.MoveWindow(hwnd, int(x), int(y), int(width), int(height), True)







