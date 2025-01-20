''' app/ui/widgets/countdownTimer.py '''
from PyQt6.QtWidgets import QLabel

class countdownTimer(QLabel):
    """
    Initialize the countdown timer.

    Args:
        parent: The parent widget.
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        file_menu = self.addMenu("File")

    