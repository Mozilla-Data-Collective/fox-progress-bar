import sys
import time


class ProgressBar:
    """A custom progress bar with a fox emoji that moves across the bar."""

    def __init__(self, total_size: int, bar_length: int = 50, unit: str | None = "B") -> None:
        """
        Args:
            total_size (int): Total size of the download/process.
            bar_length (int): Length of the progress bar in characters.
            unit (str | None): Unit to display. If None, no unit is shown.
                If "B", bytes formatting is used and scaled accordingly to KB, MB, etc.
        """
        self.total_size = total_size
        self.downloaded = 0
        self.bar_length = bar_length
        self.start_time = time.time()
        self.last_update_time = 0.0
        self.update_interval = 0.1  # seconds
        self.unit = unit

    def update(self, chunk_size: int) -> None:
        """Update the progress bar with new downloaded data"""
        self.downloaded += chunk_size

        # Only update display if enough time has passed
        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            self._display()
            self.last_update_time = current_time

    def _display(self) -> None:
        """Render the progress bar to stdout."""
        if self.total_size <= 0:
            return

        # Calculate percentage and bar position
        percentage = min(100.0, (self.downloaded / self.total_size) * 100)
        filled_length = int(self.bar_length * self.downloaded // self.total_size)

        # Create the progress bar - always show fox, even at 0%
        bar = "█" * filled_length + "░" * (self.bar_length - filled_length)

        # Position the fox emoji - always visible at position 0 or current progress
        if filled_length == 0:
            # Fox at the start when no progress yet
            bar = "🦊" + bar[1:]
        else:
            # Fox at the leading edge of progress
            fox_position = min(filled_length, self.bar_length - 1)
            bar = bar[:fox_position] + "🦊" + bar[fox_position + 1 :]

        # Calculate speed and ETA
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0 and self.downloaded > 0:
            speed = self.downloaded / elapsed_time
            eta = (self.total_size - self.downloaded) / speed if speed > 0 else 0
            speed_str = f"{self._format_value(speed)}/s"
            eta_str = f"ETA: {self._format_time(eta)}"
        else:
            speed_str = "0.0" if self.unit is None else f"0.0 {self.unit}/s"
            eta_str = "ETA: --:--"

        sys.stdout.write(
            f"\r{bar} {percentage:.1f}% "
            f"({self._format_value(self.downloaded)}/{self._format_value(self.total_size)}) "
            f"{speed_str} {eta_str}"
        )
        sys.stdout.flush()

    def finish(self) -> None:
        """Complete the progress bar and move to the next line."""
        elapsed_time = time.time() - self.start_time
        if self.total_size > 0:
            # Show completed bar with fox at the end
            bar = "█" * (self.bar_length - 1) + "🦊"
            avg_speed = self.downloaded / elapsed_time if elapsed_time > 0 else 0
            sys.stdout.write(
                f"\r{bar} 100.0% "
                f"({self._format_value(self.downloaded)}/{self._format_value(self.total_size)}) "
                f"Average: {self._format_value(avg_speed)}/s "
                f"Total time: {self._format_time(elapsed_time)}\n"
            )
        else:
            avg_speed = self.downloaded / elapsed_time if elapsed_time > 0 else 0
            unit_suffix = "" if self.unit is None else f" {self.unit}"
            sys.stdout.write(
                f"\n🦊 Process complete! {self.downloaded:.1f}{unit_suffix} "
                f"in {self._format_time(elapsed_time)} "
                f"(avg: {self._format_value(avg_speed)}/s)\n"
            )
        sys.stdout.flush()

    def _format_value(self, value: float) -> str:
        """Format current value with or without unit."""
        if self.unit is None:
            return f"{value:.1f}"
        if self.unit == "B":
            return self._format_bytes(value)
        return f"{value:.1f} {self.unit}"

    @staticmethod
    def _format_bytes(bytes_val: float) -> str:
        """Format bytes into a human readable string."""
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        value = float(bytes_val)
        for unit in units:
            if value < 1024.0 or unit == units[-1]:
                return f"{value:.1f} {unit}"
            value /= 1024.0
        return ""

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds into MM:SS."""
        if seconds < 0:
            return "--:--"
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02d}:{secs:02d}"
