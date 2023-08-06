# SimpleWin32 简单使用pywin32框架

## 安装
```pycon
pip install simplewin32
```

## 引用
```pycon
from SimpleWin32.simplewin32 import *
```

## 可使用对象
### **KeyCode**
快捷使用键盘字符码

### **MouseEvent**
鼠标的左右中键的点击事件定义

### **Mouse**
进行鼠标操作的类，可以使用方法链的形式进行调用
- move: 鼠标移动
- roll: 鼠标滚动
- mouse_position: 获取当前鼠标位置
- click: 前台鼠标点击
- bg_Click: 后台点击

### **Keyboard**
键盘事件的操作类
- click: 点击
- press: 按下
- release: 松开
- bg_Click: 后台点击

### **Message**
进行输入、弹窗等文字类的操作，包含弹窗的基本类型
- InputMessage: 输入文字
- AlertMessage: 弹出信息框
- SetText: 窗口设置文字

### **ClipBoard**
粘贴板设置和获取值操作类
- SetClipboard: 设置粘贴板文字
- GetClipboard: 获取粘贴板文字

### **Window**
集合以及二次封装了窗口方法，便捷获取窗口信息、枚举窗口句柄等操作
- GetSystemMetrics: 获取屏幕尺寸
- GetDeviceCaps: 获取屏幕分辨率
- ComputerDeviceScale: 计算设备缩放比
- GetAllWindows: 获取所有的窗口或一级子窗口
- FindWindow: 搜索窗口
- GetWindowInfo: 获取窗口class、title
- MoveOrResizeWindow: 设置窗口大小和位置
- ShowWindow: 显示窗口
- GetCurrentWindow: 获取当前窗口句柄值以及title和class
- GetWindowRect: 获取窗口坐标位置
- MarkChildWindow: 标记窗口句柄位置(需要numpy、opencv和pillow库支持)
- FuzzySearchWindow: 通过class和窗口title模糊搜索窗口句柄

### **Voice**
声音模块
- Speak: 将文字转换为电脑语音朗读，调用本地电脑api

### **Custom**
封装了一些常用的窗口操作方法：
- UploadFile: 文件上传操作

