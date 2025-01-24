''' app/ui/main_window.py '''
from PyQt6 import (QtCore, QtWidgets)
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from ..utils.config import AppConfig
from .widgets.menubar import MenuBar
from .widgets.toolbar import ToolBar
from .widgets.statusbar import StatusBar
from .widgets.treeview import TreeView
from .widgets.digitalClock import DigitalClock
from .widgets.digitalCalendar import DigitalCalendar
from .widgets.dateEdit import DateEdit
from .widgets.timeEdit import TimeEdit
from .widgets.countdownTimer import countdownTimer
from ..utils.utils import *
import os
import sys

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

        # Styling
        self.originalPalette = QApplication.palette()
        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)
        self.changeStyle('Fusion')

        # Create main_widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Create widgets for main_layout
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createCountdown()
        
        # Add widgets to the main_layout
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.topLeftGroupBox, 0, 0)
        self.main_layout.addWidget(self.topRightGroupBox, 0, 1)
        self.main_layout.addWidget(self.countdownTimer, 1, 0,1,2)
    
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 1)
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_widget.setLayout(self.main_layout)

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
            "Open", 
            resource_path("resources\\assets\\icons\\open_folder.ico"), 
            self.open_file,
            False)
        self.topbar.add_button(
            "Save", 
            resource_path("resources\\assets\\icons\\save.ico"),  
            self.save_file,
            False)
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Start", 
            resource_path("resources\\assets\\icons\\start.png"), 
            self.start_countdown,
            False)
        self.topbar.add_button(
            "Stop", 
            resource_path("resources\\assets\\icons\\stop.png"), 
            self.stop_countdown,
            True)
        self.topbar.add_togglebutton(
            "Alarm", 
            resource_path("resources\\assets\\icons\\bell_off.png"), 
            resource_path("resources\\assets\\icons\\bell_on.png"), 
            self.enable_alarm,
            False)
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Settings", 
            resource_path("resources\\assets\\icons\\settings.ico"), 
            self.settings_window,
            False)
        self.topbar.addSeparator()
        self.topbar.add_separator()
        self.topbar.addSeparator()
        self.topbar.add_button(
            "Exit", 
            resource_path("resources\\assets\\icons\\exit.ico"), 
            self.exit_app,
            False)
        
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

    def start_countdown(self) -> None:
        """
        Event handler for the "Start" button. Starts the countdown.
        """
        currentTime = QDateTime.currentDateTime()
        targetTime = self.editTime.time()

        # Create a QDateTime object for targetTime on the current date
        targetDateTime = QDateTime(currentTime.date(), targetTime)

        # Calculate the difference in seconds
        remainingTime = targetDateTime.toSecsSinceEpoch() - currentTime.toSecsSinceEpoch()
        # Check if remainingTime is negative
        if remainingTime < 0:
            QMessageBox.information(self, "Error", "Target time is in the past.")
            return
        try:
            self.countdownTimer.start_thread(remainingTime)
        except ValueError:
            QMessageBox.information(self, "Error", "Please enter a number.")
            return
        if self.countdownTimer.check_thread():
            self.topbar.disable_button("Start",True)
            self.topbar.disable_button("Stop",False)

    def stop_countdown(self) -> None:
        """
        Event handler for the "Stop" button. Stops the countdown.
        """
        self.countdownTimer.stop_thread()
        if not self.countdownTimer.check_thread():
            self.topbar.disable_button("Start",False)
            self.topbar.disable_button("Stop",True)

    def abort_countdown(self) -> None:
        self.countdownTimer.stopThreadOnExit

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

        topleft_layout = QVBoxLayout()

        # Define "Set date" group box
        setDateBox = QGroupBox("Set date")      
        # Add buttons for "Set date" group box
        self.editDate = DateEdit()                   
        self.todayButton = QPushButton("Today")
        self.todayButton.clicked.connect(self.set_today)
        self.todayButton.setFixedWidth(100)
        self.plus1dButton = QPushButton("+1d")
        self.plus1dButton.clicked.connect(lambda: self.add_days(1))
        self.plus1dButton.setFixedWidth(40)
        self.minus1dButton = QPushButton("-1d")
        self.minus1dButton.clicked.connect(lambda: self.add_days(-1))
        self.minus1dButton.setFixedWidth(40)
        self.plus7dButton = QPushButton("+7d")
        self.plus7dButton.clicked.connect(lambda: self.add_days(7))
        self.plus7dButton.setFixedWidth(40)
        self.minus7dButton = QPushButton("-7d")
        self.minus7dButton.clicked.connect(lambda: self.add_days(-7))
        self.minus7dButton.setFixedWidth(40)
        # Group 1 day and 7 days buttons as HBox layouts
        dateBox1dButtonsLayout = QHBoxLayout()
        dateBox1dButtonsLayout.addWidget(self.plus1dButton,1)
        dateBox1dButtonsLayout.addWidget(self.minus1dButton,1)
        dateBox7dButtonsLayout = QHBoxLayout()
        dateBox7dButtonsLayout.addWidget(self.plus7dButton)
        dateBox7dButtonsLayout.addWidget(self.minus7dButton)
        # Define "Set date" button layout
        dateBoxButtonLayout = QHBoxLayout()
        dateBoxButtonLayout.addWidget(self.todayButton)
        dateBoxButtonLayout.addSpacing(20)
        dateBoxButtonLayout.addLayout(dateBox1dButtonsLayout)
        dateBoxButtonLayout.addSpacing(20)
        dateBoxButtonLayout.addLayout(dateBox7dButtonsLayout)
        dateBoxButtonLayout.addStretch(1)
        # Define and set the "Set date" box layout
        dateBoxLayout = QVBoxLayout()
        dateBoxLayout.addWidget(self.editDate,1)
        dateBoxLayout.addLayout(dateBoxButtonLayout)
        setDateBox.setLayout(dateBoxLayout)

        # Set time group box
        setTimeBox = QGroupBox("Set time")
        # Add buttons for "Set time" group box
        self.editTime = TimeEdit()
        self.nowButton = QPushButton('Now')
        self.nowButton.clicked.connect(self.set_now)
        self.nowButton.setFixedWidth(100)
        self.plus1mButton = QPushButton("+1m")
        self.plus1mButton.clicked.connect(lambda: self.add_secs(1*60))
        self.plus1mButton.setFixedWidth(35)
        self.minus1mButton = QPushButton("-1m")
        self.minus1mButton.clicked.connect(lambda: self.add_secs(-1*60))
        self.minus1mButton.setFixedWidth(35)
        self.plus10mButton = QPushButton("+10m")
        self.plus10mButton.clicked.connect(lambda: self.add_secs(10*60))
        self.plus10mButton.setFixedWidth(35)
        self.minus10mButton = QPushButton("-10m")
        self.minus10mButton.clicked.connect(lambda: self.add_secs(-10*60))
        self.minus10mButton.setFixedWidth(35)
        self.plus1hButton = QPushButton("+1h")
        self.plus1hButton.clicked.connect(lambda: self.add_secs(60*60))
        self.plus1hButton.setFixedWidth(35)
        self.minus1hButton = QPushButton("-1h")
        self.minus1hButton.clicked.connect(lambda: self.add_secs(-60*60))
        self.minus1hButton.setFixedWidth(35)
        # Group 1 min, 10min and 1hour buttons as HBox layouts
        timeBox1mButtonsLayout = QHBoxLayout()
        timeBox1mButtonsLayout.addWidget(self.plus1mButton,1)
        timeBox1mButtonsLayout.addWidget(self.minus1mButton,1)
        timeBox10mButtonsLayout = QHBoxLayout()
        timeBox10mButtonsLayout.addWidget(self.plus10mButton,1)
        timeBox10mButtonsLayout.addWidget(self.minus10mButton,1)
        timeBox1hButtonsLayout = QHBoxLayout()
        timeBox1hButtonsLayout.addWidget(self.plus1hButton,1)
        timeBox1hButtonsLayout.addWidget(self.minus1hButton,1)
        # Define "Set date" button layout
        timeBoxButtonLayout = QHBoxLayout()
        timeBoxButtonLayout.addWidget(self.nowButton)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox1mButtonsLayout)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox10mButtonsLayout)
        timeBoxButtonLayout.addSpacing(20)
        timeBoxButtonLayout.addLayout(timeBox1hButtonsLayout)
        timeBoxButtonLayout.addStretch(1)
        # Define and set the "Set date" box layout
        timeBoxLayout = QVBoxLayout()
        timeBoxLayout.addWidget(self.editTime,1)
        timeBoxLayout.addLayout(timeBoxButtonLayout)
        setTimeBox.setLayout(timeBoxLayout)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter countdown target (seconds)")
        
        # Building parent layout
        topleft_layout.addWidget(setDateBox)
        topleft_layout.addWidget(setTimeBox)
        topleft_layout.addWidget(self.input)
        self.topLeftGroupBox.setLayout(topleft_layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()

        digitalcalendar = DigitalCalendar()
        digitalclock = DigitalClock()

        topright_layout = QVBoxLayout()
        topright_layout.addWidget(digitalcalendar)
        topright_layout.addWidget(digitalclock)
        self.topRightGroupBox.setLayout(topright_layout)
        
    def createCountdown(self):
        self.countdownTimer = countdownTimer()
        self.countdownTimer.setMinimumHeight(300)

    def set_today(self):
        self.editDate._update_today()

    def add_days(self,days):
        self.editDate._add_days(days)

    def set_now(self):
        self.editTime._update_now()

    def add_secs(self,secs):
        self.editTime._add_secs(secs)