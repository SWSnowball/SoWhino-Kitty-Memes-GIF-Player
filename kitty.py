import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QKeyEvent, QImageReader
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
import traceback

def handle_exception(exc_type, exc_value, exc_traceback):
    # 打印回溯信息
    traceback.print_tb(exc_traceback)

    # 执行默认的异常处理
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

# 设置自定义的异常处理函数
sys.excepthook = handle_exception


class KittyWin(QWidget):
    def __init__(self, parent = None):
        super(KittyWin, self).__init__(parent)
        self.resize(400,398)
        self.move(1000,200)
        self.setWindowFlags(Qt.Dialog|Qt.CustomizeWindowHint|Qt.WindowStaysOnTopHint)

        self.kitty_label = QLabel(self)
        self.kitty_label.move(0,0)
        self.kitty_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        kitties_gifs = os.listdir("./kitties")
        self.kitties = []
        for item in kitties_gifs:
            self.kitties.append(item)
        self.idx = 0
        self.max_idx = len(self.kitties)

        self.mov = QMovie("kitties/oiiaiioiiiai.gif")
        self.kitty_label.setMovie(self.mov)
        self.mov.start()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        new_movie = None

        if key == Qt.Key_W:
            self.move(self.x(), self.y() - 10)  # 注意：y 减小是向上移动
        elif key == Qt.Key_S:
            self.move(self.x(), self.y() + 10)  # y 增大是向下移动
        elif key == Qt.Key_A:
            self.move(self.x() - 10, self.y())
        elif key == Qt.Key_D:
            self.move(self.x() + 10, self.y())

        # 根据按下的键选择新的GIF
        if key == Qt.Key_Right:
            if self.idx + 1 < self.max_idx:  # 未到末尾
                self.idx += 1
            else:  # 已到末尾，循环到第一张
                self.idx = 0
            new_movie = self.kitties[self.idx]

        elif key == Qt.Key_Left:
            if self.idx - 1 >= 0:  # 未到开头
                self.idx -= 1
            else:  # 已在开头，循环到最后一张
                self.idx = self.max_idx - 1
            new_movie = self.kitties[self.idx]

        # 停止当前动画
        self.mov.stop()
        # 设置并启动新动画
        self.mov = QMovie(f"./kitties/{new_movie}")
        self.kitty_label.setMovie(self.mov)
        self.mov.start()
        reader = QImageReader(f"./kitties/{new_movie}")
        if reader.canRead():
            size = reader.size()
            if size.isValid():
                self.resize(size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    oii = KittyWin()
    oii.show()
    sys.exit(app.exec_())



