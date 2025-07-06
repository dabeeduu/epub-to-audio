import threading


class Progress:
    def __init__(self, total):
        self.total = total
        self.completed = 0
        self.lock = threading.Lock()

    def update(self):
        with self.lock:
            self.completed += 1
            self.show_progress()

    def show_progress(self):
        bar_length = 40
        filled_length = int(bar_length * self.completed / self.total)
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(
            f"\r[{bar}] {self.completed}/{self.total} chapters done", end="", flush=True
        )

    def done(self):
        print()
