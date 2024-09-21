# 可爱的Windows锁屏小助手

这是一个卡通风格的Windows桌面应用程序，允许用户设置一个指定的时间后自动锁定屏幕。

## 功能

- 可爱的图形用户界面，方便设置锁屏时间
- 用户可以精确设置分钟和秒数作为倒计时
- 倒计时最后10秒会在屏幕上方中央显示可爱的倒计时提醒
- 时间到达后自动锁定Windows屏幕
- 支持停止计时和重置功能

## 技术栈

- 使用Python编写
- GUI框架: PyQt5
- 系统操作: ctypes库

## 安装

1. 确保您的系统已安装Python 3.7+
2. 克隆此仓库
3. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

## 使用方法

运行主程序文件:
```
python main.py
```

1. 在输入框中设置希望多少分钟和秒后锁屏（默认为1分钟0秒）
2. 点击"开始倒计时"按钮开始计时
3. 可以随时点击"停止计时"按钮暂停倒计时
4. 点击"重置"按钮可以重新设置时间
5. 应用将在后台运行，到达设定时间后自动锁定屏幕

注意：最后10秒将在屏幕上方中央显示可爱的倒计时提醒。

## 贡献

欢迎提交问题和改进建议。如果您想贡献代码，请先开issue讨论您想改变的内容。

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)