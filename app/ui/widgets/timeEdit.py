''' app/ui/widgets/timeEdit.py '''
from PyQt6.QtCore import QDateTime, QDate, pyqtSlot as Slot
from PyQt6.QtWidgets import QTimeEdit

class TimeEdit(QTimeEdit):
    def __init__(self):
        super().__init__()
        self.setDisplayFormat("hh:mm:ss")
        self.setDateTime(QDateTime.currentDateTime())

    @Slot()
    def _update_now(self) -> None:
        now = QDateTime.currentDateTime()
        self.setDateTime(now)

    @Slot()
    def _add_secs(self, secs) -> None:
        new_time = self.time().addSecs(secs)
        now = QDateTime.currentDateTime()
        self.setTime(new_time)
    