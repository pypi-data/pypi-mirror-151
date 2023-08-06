# SimpleWin32 简单使用pywin32框架

## 安装
```pycon
pip install simplewin32
```

## 引用
```pycon
from SimpleWin32.simplewin32 import KeyCode, MouseEvent, Mouse, Keyboard, Message, ClipBoard, Window
```

## 可使用对象
**KeyCode**
快捷使用键盘字符码

**MouseEvent**
鼠标的左右中键的点击事件定义

**Mouse**
进行鼠标操作的类，可以使用方法链的形式进行调用

**Keyboard**
键盘事件的操作类

**Message**
进行输入、弹窗等文字类的操作，包含弹窗的基本类型

**ClipBoard**
粘贴板设置和获取值操作类

**Window**
集合以及二次封装了窗口方法，便捷获取窗口信息、枚举窗口句柄等操作

**Custom**
封装了一些常用的窗口操作方法：
- UploadFile: 文件上传操作

