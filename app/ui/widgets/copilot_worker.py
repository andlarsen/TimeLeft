import sys
import time
from PyQt6.QtCore import QObject, QThread, pyqtSignal as Signal, pyqtSlot as Slot
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit

class Worker(QObject):
    finished = Signal()
    progress = Signal(int)
    stop_signal = Signal()

    def __init__(self, duration):
        super().__init__()
        self._is_running = True
        self.duration = duration

    @Slot()
    def run(self):
        """Long-running task."""
        self._is_running = True
        # for i in range(5):
        #     time.sleep(1)
        #     if not self._is_running:
        #         break
        #     self.progress.emit(i + 1)
        # for i in range(self.duration, 0, -1):
        #     if not self._is_running:
        #         break
        #     self.progress.emit(i)
        #     time.sleep(1)
        i = 0
        while(i<=self.duration):
            if not self._is_running:
                break
            self.progress.emit(self.duration-i)
            i = i+1
            time.sleep(1)
        self.finished.emit()

    @Slot()
    def stop(self):
        self._is_running = False

class Gui(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.worker = None
        self.thread = None

    def init_ui(self):
        self.label = QLabel("Countdown: 0", self)
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter countdown duration (seconds)")
        self.start_button = QPushButton("Start Countdown", self)
        self.start_button.clicked.connect(self.start_thread)

        self.stop_button = QPushButton("Stop Countdown", self)
        self.stop_button.clicked.connect(self.stop_thread)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("PyQt6 Countdown Timer")
        self.show()

    def start_thread(self):
        # Checks if the thread is running and only starts a new one if it's not
        if self.thread and self.thread.isRunning():
            return
        
        try:
            duration = int(self.input.text())
        except ValueError:
            self.label.setText("Invalid input! Please enter a number.")
            return
        
        self.worker = Worker(duration)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater) # This line deletes the thread if finished and prevents restarting thread

        self.worker.progress.connect(self.update_label)

        self.thread.start()

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

    def update_label(self, value):
        self.label.setText(f"Progress: {value}")
