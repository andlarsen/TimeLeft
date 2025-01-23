'''' app/ui/widgets/digitalClock.py '''
from PyQt6.QtWidgets import QLCDNumber
from PyQt6.QtCore import QTime, QTimer

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
