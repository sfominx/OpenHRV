from datetime import datetime
from PySide6.QtCore import QObject, Signal
from openhrv.utils import NamedSignal


class Logger(QObject):
    recording_status = Signal(int)
    status_update = Signal(str)

    def __init__(self):
        super().__init__()
        self.file = None

    def start_recording(self, file_path: str):
        if self.file:
            self.status_update.emit(f"Запись уже идет в {self.file.name}.")
            return  # only write to one file at a time
        self.file = open(file_path, "a+")
        self.file.write("event,value,timestamp\n")  # header
        self.recording_status.emit(0)
        self.status_update.emit(f"Начата запись в {self.file.name}.")

    def save_recording(self):
        """Called when:
        1. User saves recording.
        2. User closes app while recording
        """
        if not self.file:
            return
        self.file.close()
        self.recording_status.emit(1)
        self.status_update.emit(f"Запись сохранена в {self.file.name}.")
        self.file = None

    def write_to_file(self, data: NamedSignal):
        if not self.file:
            return
        key, val = data
        if isinstance(val, list):
            val = val[-1]
        if isinstance(val, tuple):
            val = val[-1][-1]
        timestamp = datetime.now().isoformat()
        self.file.write(f"{key},{val},{timestamp}\n")
