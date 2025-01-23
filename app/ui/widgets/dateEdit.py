''' app/ui/widgets/dateEdit.py '''
from PyQt6.QtCore import QDateTime, QDate, pyqtSlot
from PyQt6.QtWidgets import QPushButton, QDateEdit

class DateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent, calendarPopup=True)
        self._today_button = QPushButton(self.tr("Today"))
        self._today_button.clicked.connect(self._update_today)
        self.calendarWidget().layout().addWidget(self._today_button)
        self.setDateTime(QDateTime.currentDateTime())
        
    # @QtCore.pyqtSlot()
    @pyqtSlot()
    def _update_today(self):
        self._today_button.clearFocus()
        today = QDate.currentDate()
        self.calendarWidget().setSelectedDate(today)