''' app/ui/widgets/digitalCalendar.py '''
from PyQt6.QtWidgets import QLCDNumber
from PyQt6.QtCore import QTimer, QDateTime

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