''' app/ui/main_window.py '''
from PyQt6 import (QtCore, QtWidgets)
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ..utils.config import AppConfig
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.statusbar import StatusBar
from .widgets.treeview import TreeView
import os
import sys
# from PySide6.QtCore import QTime, QTimer, Slot
# from PySide6.QtWidgets import QLCDNumber

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window-Settings
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.originalPalette = QApplication.palette()

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.changeStyle('Fusion')

        
        # self.createTopGroupBox()
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createProgressBar()
        self.createCountdown()
        
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.topLeftGroupBox, 0, 0)
        self.mainLayout.addWidget(self.topRightGroupBox, 0, 1)
        self.mainLayout.addWidget(self.progressBar, 1, 0,1,2)
        self.mainLayout.addWidget(self.Countdown, 2, 0,1,2)
    
        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 1)
        self.central_widget.setLayout(self.mainLayout)

        self.create_toolbars()
        self.setMenuBar(MenuBar(self))
        # self.setStatusBar(StatusBar(self))
        
        
## Toolbar widget
    def create_toolbars(self) -> None:
        """
        Creates and adds the top and right toolbars to the main window.
        """
        # Top Toolbar [PyQt6.QtWidgets.QToolBar]
        self.topbar = ToolBar(self, 
                              orientation=Qt.Orientation.Horizontal,
                              style=Qt.ToolButtonStyle.ToolButtonIconOnly, 
                              icon_size=(36, 36))
        # Top Toolbar Buttons
        self.topbar.add_button(
            "Open", resource_path("resources\\assets\\icons\\open_folder.ico"), self.open_file)
        self.topbar.add_button(
            "Save", resource_path("resources\\assets\\icons\\save.ico"), self.save_file)
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Start", resource_path("resources\\assets\\icons\\start.png"), self.start_counter)
        self.topbar.add_button(
            "Alarm", resource_path("resources\\assets\\icons\\bell_on.png"), self.enable_alarm)
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Settings", resource_path("resources\\assets\\icons\\settings.ico"), self.settings_window)
        self.topbar.addSeparator()
        self.topbar.add_separator()
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Exit", resource_path("resources\\assets\\icons\\exit.ico"), self.exit_app)
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)

    def create_edit(self) -> QTextEdit:
        """
        Creates and adds the QTextEdit widget to the main window.
        """
        return QTextEdit(self)

    def open_file(self) -> None:
        """
        Event handler for the "Open" button. Displays the "Open File" dialog.
        """
        print("Open")

    def save_file(self) -> None:
        """
        Event handler for the "Save" button. Displays the "Save File" dialog.
        """
        print("Save")

    def exit_app(self) -> None:
        """
        Event handler for the "Exit" button. Closes the application.
        """
        self.close()

    def settings_window(self) -> None:
        """
        Event handler for the "Settings" button. Displays the "Settings" window.
        """
        print("Settings")

    def privacy_window(self) -> None:
        """
        Event handler for the "Privacy" button. Displays the "Privacy" window.
        """
        print("privacy_window")

    def start_counter(self) -> None:
        """
        Event handler for the "Alarm" button. Enables/disables the alarm, which must change icon.
        """
        print("Counting down...")

    def enable_alarm(self) -> None:
        """
        Event handler for the "Alarm" button. Enables/disables the alarm, which must change icon.
        """
        print("Ring ring!")

## Main window
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()
        
    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox()

        parent_layout = QVBoxLayout()

        # Define "Set date" group box
        setDateBox = QGroupBox("Set date")      
        # Add buttons for "Set date" group box
        editDate = DateEdit()                   
        todayButton = QPushButton("Today")
        todayButton.setFixedWidth(100)
        plus1dButton = QPushButton("+1d")
        plus1dButton.setFixedWidth(40)
        minus1dButton = QPushButton("-1d")
        minus1dButton.setFixedWidth(40)
        plus7dButton = QPushButton("+7d")
        plus7dButton.setFixedWidth(40)
        minus7dButton = QPushButton("-7d")
        minus7dButton.setFixedWidth(40)
        # Group 1 day and 7 days buttons as HBox layouts
        dateBox1dButtonsLayout = QHBoxLayout()
        dateBox1dButtonsLayout.addWidget(plus1dButton,1)
        dateBox1dButtonsLayout.addWidget(minus1dButton,1)
        dateBox7dButtonsLayout = QHBoxLayout()
        dateBox7dButtonsLayout.addWidget(plus7dButton)
        dateBox7dButtonsLayout.addWidget(minus7dButton)
        # Define "Set date" button layout
        dateBoxButtonLayout = QHBoxLayout()
        dateBoxButtonLayout.addWidget(todayButton)
        dateBoxButtonLayout.addSpacing(20)
        dateBoxButtonLayout.addLayout(dateBox1dButtonsLayout)
        dateBoxButtonLayout.addSpacing(20)
        dateBoxButtonLayout.addLayout(dateBox7dButtonsLayout)
        dateBoxButtonLayout.addStretch(1)
        # Define and set the "Set date" box layout
        dateBoxLayout = QVBoxLayout()
        dateBoxLayout.addWidget(editDate,1)
        dateBoxLayout.addLayout(dateBoxButtonLayout)
        setDateBox.setLayout(dateBoxLayout)

        # Set time group box
        setTimeBox = QGroupBox("Set time")
        # Add buttons for "Set time" group box
        editTime = TimeEdit()
        nowButton = QPushButton('Now')
        nowButton.setFixedWidth(100)
        plus1mButton = QPushButton("+1m")
        plus1mButton.setFixedWidth(35)
        minus1mButton = QPushButton("-1m")
        minus1mButton.setFixedWidth(35)
        plus10mButton = QPushButton("+10m")
        plus10mButton.setFixedWidth(35)
        minus10mButton = QPushButton("-10m")
        minus10mButton.setFixedWidth(35)
        plus1hButton = QPushButton("+1h")
        plus1hButton.setFixedWidth(35)
        minus1hButton = QPushButton("-1h")
        minus1hButton.setFixedWidth(35)
        # Group 1 min, 10min and 1hour buttons as HBox layouts
        timeBox1mButtonsLayout = QHBoxLayout()
        timeBox1mButtonsLayout.addWidget(plus1mButton,1)
        timeBox1mButtonsLayout.addWidget(minus1mButton,1)
        timeBox10mButtonsLayout = QHBoxLayout()
        timeBox10mButtonsLayout.addWidget(plus10mButton,1)
        timeBox10mButtonsLayout.addWidget(minus10mButton,1)
        timeBox1hButtonsLayout = QHBoxLayout()
        timeBox1hButtonsLayout.addWidget(plus1hButton,1)
        timeBox1hButtonsLayout.addWidget(minus1hButton,1)
        # Define "Set date" button layout
        timeBoxButtonLayout = QHBoxLayout()
        timeBoxButtonLayout.addWidget(nowButton)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox1mButtonsLayout)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox10mButtonsLayout)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox1hButtonsLayout)
        timeBoxButtonLayout.addStretch(1)
        # Define and set the "Set date" box layout
        timeBoxLayout = QVBoxLayout()
        timeBoxLayout.addWidget(editTime,1)
        timeBoxLayout.addLayout(timeBoxButtonLayout)
        setTimeBox.setLayout(timeBoxLayout)

        # Building parent layout
        parent_layout.addWidget(setDateBox)
        parent_layout.addWidget(setTimeBox)
        self.topLeftGroupBox.setLayout(parent_layout)
        
    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()

        digitalcalendar = DigitalCalendar()
        digitalclock = DigitalClock()

        layout = QVBoxLayout()
        layout.addWidget(digitalcalendar)
        layout.addWidget(digitalclock)
        self.topRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(75)
        
    def createCountdown(self):
        self.Countdown = DigitalClock()
        self.Countdown.setMinimumHeight(300)


class DateEdit(QtWidgets.QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent, calendarPopup=True)
        self._today_button = QtWidgets.QPushButton(self.tr("Today"))
        self._today_button.clicked.connect(self._update_today)
        self.calendarWidget().layout().addWidget(self._today_button)
        self.setDateTime(QtCore.QDateTime.currentDateTime())
        
    @QtCore.pyqtSlot()
    def _update_today(self):
        self._today_button.clearFocus()
        today = QtCore.QDate.currentDate()
        self.calendarWidget().setSelectedDate(today)

class TimeEdit(QtWidgets.QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent, )

class DigitalClock(QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDigitCount(8)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()

        self.resize(250, 60)

    def show_time(self):
        time = QTime.currentTime()
        text = time.toString("hh:mm:ss")

        # Blinking effect
        if (time.second() % 2) == 0:
            text = text.replace(":", " ")

        self.display(text)

class DigitalCalendar(QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDigitCount(10)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_date)
        self.timer.start(1000)
        self.show_date()

        self.resize(250, 60)

    def show_date(self):
        date = QDateTime.currentDateTime()
        text = date.toString("dd-MM-yyyy")
        self.display(text)