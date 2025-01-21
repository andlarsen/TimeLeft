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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # layout = QHBoxLayout(central_widget)
        # central_widget.setLayout(layout)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        
        # self.createTopGroupBox()
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        
        # self.editbox = self.create_edit()

        styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        # disableWidgetsCheckBox.toggled.connect(self.topGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        # disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        # topLayout.addWidget(self.editbox)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        central_widget.setLayout(mainLayout)

        self.create_toolbars()
        self.setMenuBar(MenuBar(self))
        self.setStatusBar(StatusBar(self))
        
        self.changeStyle('Fusion')
        
## Toolbar widget
    def create_toolbars(self) -> None:
        """
        Creates and adds the top and right toolbars to the main window.
        """
        # Top Toolbar [PyQt6.QtWidgets.QToolBar]
        self.topbar = ToolBar(self, orientation=Qt.Orientation.Horizontal,
                              style=Qt.ToolButtonStyle.ToolButtonTextUnderIcon, icon_size=(24, 24))

        # Top Toolbar Buttons
        self.topbar.add_button(
            "Open", resource_path("resources\\assets\\icons\\open_folder.ico"), self.open_file)
        self.topbar.add_button(
            "Save", resource_path("resources\\assets\\icons\\save.ico"), self.save_file)
        self.topbar.add_separator()
        self.topbar.add_button(
            "Exit", resource_path("resources\\assets\\icons\\exit.ico"), self.exit_app)
        # Right Toolbar [PyQt6.QtWidgets.QToolBar]
        self.rightbar = ToolBar(self, orientation=Qt.Orientation.Vertical,
                                style=Qt.ToolButtonStyle.ToolButtonIconOnly,
                                icon_size=(24, 24))
        
        # Right Toolbar Buttons
        self.rightbar.add_separator()
        self.rightbar.add_button(
            "Privacy", resource_path("resources\\assets\\icons\\privacy.ico"), self.privacy_window)
        self.rightbar.add_button(
            "Settings", resource_path("resources\\assets\\icons\\settings.ico"), self.settings_window)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.topbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.rightbar)

    # def create_treeview(self) -> TreeView:
    #     """
    #     Creates and adds the tree view widget to the main window.
    #     """
    #     return TreeView(self)

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

    def privacy_window(self) -> None:
        """
        Event handler for the "Privacy" button. Displays the "Privacy" window.
        """
        print("privacy_window")


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
        self.topLeftGroupBox = QGroupBox("Countdown")

        dateedit = DateEdit()
        timeedit = TimeEdit()

        layout = QVBoxLayout()
        layout.addWidget(dateedit)
        layout.addWidget(timeedit)

        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Current time")

        digitalcalendar = DigitalCalendar()
        digitalclock = DigitalClock()

        layout = QVBoxLayout()
        layout.addWidget(digitalcalendar)
        layout.addWidget(digitalclock)
        self.topRightGroupBox.setLayout(layout)
        
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