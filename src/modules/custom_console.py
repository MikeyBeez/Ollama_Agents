# src/modules/custom_console.py

from rich.console import Console as RichConsole
from typing import List, Any

class CaptureConsole(RichConsole):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured_output: List[str] = []

    def print(self, *args, **kwargs):
        # Capture the output as a string
        with self.capture() as capture:
            super().print(*args, **kwargs)
        self.captured_output.append(capture.get())

    def get_captured_output(self) -> str:
        return ''.join(self.captured_output)

    def clear_captured_output(self):
        self.captured_output.clear()
