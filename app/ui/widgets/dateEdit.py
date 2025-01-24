''' app/ui/widgets/dateEdit.py '''
from PyQt6.QtCore import QDateTime, QDate, pyqtSlot as Slot
from PyQt6.QtWidgets import QPushButton, QDateEdit

class DateEdit(QDateEdit):
    # def __init__(self, parent=None):
    def __init__(self):
        super().__init__(calendarPopup=True)
        # self._today_button = QPushButton(self.tr("Today"))
        # self._today_button.clicked.connect(self._update_today)
        # self.calendarWidget().layout().addWidget(self._today_button)
        self.setDateTime(QDateTime.currentDateTime())
        
    @Slot()
    def _update_today(self) -> None:
        # self._today_button.clearFocus()
        today = QDate.currentDate()
        self.calendarWidget().setSelectedDate(today)
        self.setDate(today)

    @Slot()
    def _add_days(self, days) -> None:
        new_date = self.date().addDays(days)
        today = QDateTime.currentDateTime().date()
        if new_date >= today:
            self.setDate(new_date)
        else:
            self.setDate(today)
