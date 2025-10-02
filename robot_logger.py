import os
from datetime import datetime


class RobotLogger:
    """Simple logger for Robot tests with colors.
    
    Args:
        use_colors: Whether to use colors in the output.
        test_name: The name of the current test.
        step_num: The number of the current step.
    """

    # Colors
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"

    def __init__(self):
        self.use_colors = self._supports_color()
        self.test_name = None
        self.step_num = 0

    def _supports_color(self):
        """Check if the terminal supports colors."""
        return (
            hasattr(os.sys.stdout, "isatty")
            and os.sys.stdout.isatty()
            and os.environ.get("TERM") != "dumb"
            and os.environ.get("NO_COLOR") is None
        )

    def _color(self, text, color):
        """Add color to the text."""
        return f"{color}{text}{self.RESET}" if self.use_colors else text

    def _log(self, level, message, color):
        """Log a message."""
        time = datetime.now().strftime("%H:%M:%S")
        level_str = self._color(f"[{level}]", color)
        test_part = f" | {self.test_name}" if self.test_name else ""
        print(f"{time} {level_str}{test_part} | {message}")

    def start_test(self, test_name):
        """Start a new test."""
        self.test_name = test_name
        self.step_num = 0
        print(f"\n{self._color('─' * 40, self.CYAN)}")
        print(self._color(f"🚀 {test_name}", self.CYAN + self.BOLD))
        print(f"{self._color('─' * 40, self.CYAN)}")

    def end_test(self, result):
        """End the current test."""
        icon = "✅" if result == "PASS" else "❌"
        color = self.GREEN if result == "PASS" else self.RED
        print(f"\n{self._color('─' * 40, self.CYAN)}")
        print(self._color(f"{icon} {self.test_name}: {result}", color + self.BOLD))
        print(f"{self._color('─' * 40, self.CYAN)}\n")
        self.test_name = None
        self.step_num = 0

    def step(self, message):
        """Log a test step."""
        self.step_num += 1
        self._log("INFO", f"Step {self.step_num}: {message}", self.BLUE)

    def info(self, message):
        """Log info message."""
        self._log("INFO", message, self.BLUE)

    def pass_test(self, message):
        """Log test pass."""
        self._log("PASS", message, self.GREEN)

    def fail(self, message):
        """Log test fail."""
        self._log("FAIL", message, self.RED)

    def error(self, message):
        """Log error."""
        self._log("ERROR", message, self.RED + self.BOLD)

    def warning(self, message):
        """Log warning."""
        self._log("WARNING", message, self.YELLOW)


# Usage example
if __name__ == "__main__":
    logger = RobotLogger()

    logger.info("Robot Logger ready!")
    logger.pass_test("Basic functionality works")

    logger.start_test("Login Test")
    logger.step("Navigate to login page")
    logger.step("Enter username")
    logger.step("Enter password")
    logger.pass_test("Login successful")
    logger.end_test("PASS")
