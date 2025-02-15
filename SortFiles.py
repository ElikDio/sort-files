import sys
import os
import shutil
import time
from pathlib import Path
from PyQt5 import uic
from PyQt5.Qt import QPropertyAnimation, QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'data')

class SortFiles(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(RESOURCES_DIR, 'sortfiles.ui'), self)

        self.setWindowIcon(QIcon(os.path.join(RESOURCES_DIR, 'logo.png')))

        self.paint_dir = QPixmap(os.path.join(RESOURCES_DIR, 'paint_dir.png'))
        self.label_p_dir = QLabel(self)
        self.label_p_dir.move(650, 370)
        self.label_p_dir.resize(self.paint_dir.width(), self.paint_dir.height())
        self.label_p_dir.setPixmap(self.paint_dir)

        self.choose_start.setIcon(QIcon(os.path.join(RESOURCES_DIR, 'dir.png')))
        self.choose_start.setIconSize(QSize(55, 58))
        self.choose_start.clicked.connect(self.get_start_direction)

        self.choose_end.setIcon(QIcon(os.path.join(RESOURCES_DIR, 'dir.png')))
        self.choose_end.setIconSize(QSize(55, 58))
        self.choose_end.clicked.connect(self.get_end_direction)

        self.file = QPixmap(os.path.join(RESOURCES_DIR, 'extension.png'))
        self.file_extension = QLabel(self)
        self.file_extension.move(380, 455)
        self.file_extension.resize(self.file.width(), self.file.height())
        self.file_extension.setPixmap(self.file)

        self.arrow.setIcon(QIcon(os.path.join(RESOURCES_DIR, 'arrow.png')))
        self.arrow.setIconSize(QSize(141, 41))

        self.start_button.clicked.connect(self.sort_event)

        self.monthes = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

        self.symbols = [self.symbol_1, self.symbol_2, self.symbol_3, self.symbol_4, self.symbol_5,
                        self.symbol_6, self.symbol_7, self.symbol_8, self.symbol_9]
        for symbol in self.symbols:
            symbol.clicked.connect(self.symbol_choose)

        self.symbol = '_'

        self.choose_dates = [self.choose_date1, self.choose_date2, self.choose_date3,
                             self.choose_date4, self.choose_date5, self.choose_date6,
                             self.choose_date7, self.choose_date8]
        for choose_date in self.choose_dates:
            choose_date.clicked.connect(self.choose_date)

        self.dates = ['210', '120', '012', '021', '102', '201', '21', '12']
        self.date = '210'

        self.checks = [self.file_extension_1, self.file_extension_2, self.file_extension_3,
                       self.file_extension_4, self.file_extension_5]
        for check in self.checks:
            check.index = self.checks.index(check)
            check.stateChanged.connect(self.file_format)

        self.formats = {'Текстовые': ['txt', 'text', 'doc', 'docx'],
                        'Видео': ['mov', 'mp4', 'wbem', 'avi'], 'Аудио': ['mp3'],
                        'Фото': ['jpg', 'jpeg', 'png']}

        self.formats_choose = ['jpg', 'jpeg', 'png']
        self.color = 'Blue'
        self.title.setIcon(QIcon(os.path.join(RESOURCES_DIR, 'sort_files.png')))
        self.title.setIconSize(QSize(481, 131))

        self.types = [self.type_1, self.type_2, self.type_3, self.type_4, self.type_5, self.type_6,
                      self.type_7, self.type_8]

        self.help.triggered.connect(self.help_f)

        self.doanim()

    def help_f(self):
        self.close()
        self.about_ex = About()
        self.about_ex.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.sort_event()

    def doanim(self):
        self.anims = [self.anim_0, self.anim_1, self.anim_2, self.anim_3, self.anim_4, self.anim_5,
                      self.anim_6, self.anim_7, self.anim_8, self.anim_9, self.anim_10]
        for anim in self.anims:
            if self.color == 'Blue':
                anim.setStyleSheet('background-color: rgb(15, 180, 168)')
            elif self.color == 'Red':
                anim.setStyleSheet('background-color: rgb(255, 0, 50)')
            else:
                anim.setStyleSheet('background-color: rgb(0, 255, 50)')

        self.animations = ['' for _ in range(10)]
        x = 5
        y = 60
        obj = self.anim_0
        for i in range(10):
            self.animations[i] = QPropertyAnimation(obj, b"geometry")
            self.animations[i].setDuration(800)
            self.animations[i].setStartValue(QRect(x, -70, 4, 70))
            self.animations[i].setEndValue(QRect(x, y, 4, 0))
            self.animations[i].start()
            x += 80
            obj = self.anims[i + 1]
            if i == 4:
                x += 380
            if i % 2 == 0:
                y = 100
            else:
                y = 60

    def sort_event(self):
        reply = QMessageBox.question(self, 'Внимание!',
                                     "Начать сортировку?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.start_sort()
        else:
            pass

    def file_format(self):
        if self.sender().index < 4:
            format = self.formats[self.sender().text()]
            for form in format:
                if form in self.formats_choose:
                    del self.formats_choose[self.formats_choose.index(form)]
                else:
                    self.formats_choose.append(form)
        else:
            if self.sender().checkState() == 2:
                for i in range(4):
                    self.checks[i].setCheckState(2)
            else:
                for i in range(4):
                    self.checks[i].setCheckState(0)

    def choose_date(self):
        self.date = self.dates[self.choose_dates.index(self.sender())]

    def symbol_choose(self):
        sym = self.symbol
        self.symbol = self.sender().text()
        for type in self.types:
            type.setText(self.symbol.join(type.text().split(sym)))

    def move_files(self, file, path, date):
        if self.choose_move.currentText() == 'Переместить файлы':
            shutil.move(file, (path + '/' + date))
        else:
            shutil.copy(file, (path + '/' + date))

    def get_start_direction(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.start_dir.setText(dirlist)
        if dirlist:
            self.color = 'Green'
        else:
            self.color = 'Blue'
        self.doanim()

    def get_end_direction(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.end_dir.setText(dirlist)
        if dirlist:
            self.color = 'Green'
        else:
            self.color = 'Blue'
        self.doanim()

    def start_sort(self):
        if not (self.start_dir.text()) or not (self.end_dir.text()):
            self.color = 'Red'
            self.doanim()
            QMessageBox.critical(self, 'Ошибка!', 'Выберите директории!')
        elif not self.formats_choose:
            self.color = 'Red'
            self.doanim()
            QMessageBox.critical(self, 'Ошибка!', 'Выберите хотя бы один тип файлов!')
        else:
            self.color = 'Green'
            self.doanim()
            path = self.start_dir.text()
            file_list = os.listdir(path)
            full_list = [os.path.join(path, i) for i in file_list if
                         Path(i).suffix[1:].lower() in [f.lower() for f in self.formats_choose]]
            if full_list:
                for file in full_list:
                    clock = str(os.path.getmtime(file))
                    time_all = time.ctime(int(clock[:clock.find('.')]))
                    month_txt = time_all[4:7]
                    places = [time_all[8:10].strip().rjust(2, '0'), self.monthes[month_txt],
                              time_all[-4:]]
                    if len(self.date) == 3:
                        index1 = int(self.date[0])
                        index2 = int(self.date[1])
                        index3 = int(self.date[2])

                        date = places[index1] + self.symbol + places[index2] + self.symbol + places[
                            index3]
                    else:
                        index1 = int(self.date[0])
                        index2 = int(self.date[1])

                        date = places[index1] + self.symbol + places[index2]

                    try:
                        os.mkdir(self.end_dir.text() + '/' + date)
                    except OSError:
                        self.move_files(file, self.end_dir.text(), date)
                    else:
                        self.move_files(file, self.end_dir.text(), date)
                QMessageBox.information(self, 'Finish', 'Готово!')
            else:
                QMessageBox.information(self, 'Готово', 'Нужных файлов не обнаружено')

            self.start_dir.setText('')
            self.end_dir.setText('')


class About(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(RESOURCES_DIR, 'about.ui'), self)
        self.setWindowIcon(QIcon(os.path.join(RESOURCES_DIR, 'logo.png')))

    def home(self):
        self.ex = SortFiles()
        self.ex.show()

    def closeEvent(self, event):
        self.home()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SortFiles()
    ex.show()
    sys.exit(app.exec())
