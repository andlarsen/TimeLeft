import sys
import time
from PyQt6.QtCore import QObject, QThread, QDateTime, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLCDNumber, QProgressBar, QMessageBox

class Worker(QObject):
    finished = Signal()
    timeElapsed = Signal(int)
    timeRemaining = Signal(int)
    stop_signal = Signal()

    def __init__(self, target):
        super().__init__()
        self._is_running = False
        self.target = target

    @Slot()
    def run(self):
        """Long-running task."""
        self._is_running = True
        time_elapsed = 0
        time_remaining = self.target-time_elapsed
        while(time_remaining>0):
            if not self._is_running:
                break
            time_remaining = self.target-time_elapsed
            self.timeRemaining.emit(time_remaining)
            self.timeElapsed.emit(time_elapsed)
            time.sleep(1)
            time_elapsed = time_elapsed+1
        self.finished.emit()

    @Slot()
    def stop(self):
        self._is_running = False

class countdownTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.worker = None
        self.thread = None

    def init_ui(self):
        self.progressbar = QProgressBar()
        self.timer = QLCDNumber()
        self.timer.setDigitCount(6)
        # self.label = QLabel("Countdown: 0", self)
        # self.input = QLineEdit(self)
        # self.input.setPlaceholderText("Enter countdown target (seconds)")
        # self.start_button = QPushButton("Start Countdown", self)
        # self.start_button.clicked.connect(self.start_thread)

        # self.stop_button = QPushButton("Stop Countdown", self)
        # self.stop_button.clicked.connect(self.stop_thread)

        layout = QVBoxLayout()
        # layout.addWidget(self.input)
        layout.addWidget(self.progressbar)
        layout.addWidget(self.timer)
        # layout.addWidget(self.label)
        # layout.addWidget(self.start_button)
        # layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # self.setGeometry(300, 300, 300, 220)
        # self.show()

    def start_thread(self,target):
        # Checks if the thread is running and only starts a new one if it's not
        if self.thread and self.thread.isRunning():
            return
        self.progressbar.setMaximum(target)

        self.worker = Worker(target)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater) # This line deletes the thread if finished and prevents restarting thread

        self.worker.timeRemaining.connect(self.update_timer)
        self.worker.timeElapsed.connect(self.update_progressbar)

        self.thread.start()
        
    def check_thread(self):
        # Stops the worker and quits and waits for the thread to finish to ensure that it is properly cleaned up before starting a new one.
        if self.thread and self.thread.isRunning():
            return True

    def stop_thread(self):
        # Stops the worker and quits and waits for the thread to finish to ensure that it is properly cleaned up before starting a new one.
        if self.worker:
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()

    def stopThreadOnExit(self):
        # Stops the worker and quits and waits for the thread to finish to ensure that it is properly cleaned up before starting a new one.
        if self.worker:
            self.worker.stop()
            self.worker.deleteLater
            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater

    # def update_label(self, value):
    #     self.label.setText(f"Progress: {value}")

    def update_timer(self, remaining):
        self.timer.display(remaining)

    def update_progressbar(self, elapsed):
        self.progressbar.setValue(elapsed)
