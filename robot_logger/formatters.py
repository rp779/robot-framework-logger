"""
Formatters for different output types in Robot Logger.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any
from .colors import Colors, ColorTheme
from .config import LoggerConfig


class Formatter(ABC):
    """Abstract base class for log formatters."""

    def __init__(self, config: LoggerConfig):
        self.config = config

    @abstractmethod
    def format_message(self, level: str, message: str, **kwargs) -> str:
        """Format a log message."""
        pass

    def format_timestamp(self) -> str:
        """Format current timestamp."""
        if not self.config.show_timestamp:
            return ""

        timestamp = datetime.now().strftime(self.config.timestamp_format)
        if self.config.use_colors:
            return Colors.colorize(timestamp, self.config.colors.get("TIMESTAMP", ""))
        return timestamp

    def format_test_name(self, test_name: Optional[str] = None) -> str:
        """Format test name."""
        if not self.config.show_test_name or not test_name:
            return ""

        if self.config.use_colors:
            return Colors.colorize(test_name, self.config.colors.get("TEST_NAME", ""))
        return test_name

    def format_log_level(self, level: str) -> str:
        """Format log level."""
        if not self.config.show_log_level:
            return ""

        color = (
            self.config.colors.get(level.upper(), "") if self.config.use_colors else ""
        )
        formatted_level = f"[{level.upper():<8}]"

        if color:
            return Colors.colorize(formatted_level, color)
        return formatted_level

    def format_step(
        self, step_number: Optional[int] = None, step_name: Optional[str] = None
    ) -> str:
        """Format step information."""
        if not self.config.show_step_numbers:
            return ""

        step_parts = []
        if step_number is not None:
            step_parts.append(f"{self.config.robot_step_prefix} {step_number}")
        if step_name:
            step_parts.append(step_name)

        if not step_parts:
            return ""

        step_str = " | ".join(step_parts)
        if self.config.use_colors:
            return Colors.colorize(step_str, self.config.colors.get("STEP", ""))
        return step_str

    def format_message_content(self, message: str) -> str:
        """Format the main message content."""
        if self.config.use_colors:
            return Colors.colorize(message, self.config.colors.get("MESSAGE", ""))
        return message

    def create_separator(
        self, char: Optional[str] = None, length: Optional[int] = None
    ) -> str:
        """Create a separator line."""
        char = char or self.config.separator
        length = length or self.config.separator_length

        separator = char * length
        if self.config.use_colors:
            return Colors.colorize(separator, self.config.colors.get("SEPARATOR", ""))
        return separator


class ConsoleFormatter(Formatter):
    """Formatter for console output with colors and rich formatting."""

    def format_message(self, level: str, message: str, **kwargs) -> str:
        """Format a message for console output."""
        parts = []

        # Timestamp
        if timestamp := self.format_timestamp():
            parts.append(timestamp)

        # Log level
        if level_str := self.format_log_level(level):
            parts.append(level_str)

        # Test name
        if test_name := self.format_test_name(kwargs.get("test_name")):
            parts.append(test_name)

        # Step information
        if step_str := self.format_step(
            kwargs.get("step_number"), kwargs.get("step_name")
        ):
            parts.append(step_str)

        # Main message
        if message:
            parts.append(self.format_message_content(message))

        return " | ".join(filter(None, parts))

    def format_test_start(self, test_name: str, **kwargs) -> str:
        """Format test start message."""
        separator = self.create_separator()
        header = f"🚀 Starting Test: {test_name}"

        if self.config.use_colors:
            header = Colors.colorize(header, self.config.colors.get("HEADER", ""))

        return f"\n{separator}\n{header}\n{separator}"

    def format_test_end(self, test_name: str, result: str, **kwargs) -> str:
        """Format test end message."""
        separator = self.create_separator()
        result_icon = self._get_result_icon(result)
        header = f"{result_icon} Test {result}: {test_name}"

        if self.config.use_colors:
            color = self.config.colors.get(result.upper(), "")
            if color:
                header = Colors.colorize(header, color)

        return f"\n{separator}\n{header}\n{separator}\n"

    def format_assertion(
        self, assertion_type: str, expected: Any, actual: Any, **kwargs
    ) -> str:
        """Format assertion message."""
        parts = ["🔍 Assertion:"]

        if assertion_type:
            parts.append(f"Type: {assertion_type}")
        if expected is not None:
            parts.append(f"Expected: {expected}")
        if actual is not None:
            parts.append(f"Actual: {actual}")

        assertion_str = " | ".join(parts)
        if self.config.use_colors:
            assertion_str = Colors.colorize(
                assertion_str, self.config.colors.get("ASSERTION", "")
            )

        return assertion_str

    def format_error(self, error_type: str, error_message: str, **kwargs) -> str:
        """Format error message."""
        parts = ["❌ Error:"]

        if error_type:
            parts.append(f"Type: {error_type}")
        if error_message:
            parts.append(error_message)

        error_str = " | ".join(parts)
        if self.config.use_colors:
            error_str = Colors.colorize(error_str, self.config.colors.get("ERROR", ""))

        return error_str

    def _get_result_icon(self, result: str) -> str:
        """Get appropriate icon for test result."""
        icons = {"PASS": "✅", "FAIL": "❌", "ERROR": "💥", "SKIP": "⏭️", "WARNING": "⚠️"}
        return icons.get(result.upper(), "📋")


class FileFormatter(Formatter):
    """Formatter for file output without colors."""

    def format_message(self, level: str, message: str, **kwargs) -> str:
        """Format a message for file output (no colors)."""
        parts = []

        # Timestamp
        if self.config.show_timestamp:
            timestamp = datetime.now().strftime(self.config.timestamp_format)
            parts.append(timestamp)

        # Log level
        if self.config.show_log_level:
            parts.append(f"[{level.upper():<8}]")

        # Test name
        if self.config.show_test_name and kwargs.get("test_name"):
            parts.append(kwargs["test_name"])

        # Step information
        if self.config.show_step_numbers:
            step_parts = []
            if kwargs.get("step_number") is not None:
                step_parts.append(
                    f"{self.config.robot_step_prefix} {kwargs['step_number']}"
                )
            if kwargs.get("step_name"):
                step_parts.append(kwargs["step_name"])

            if step_parts:
                parts.append(" | ".join(step_parts))

        # Main message
        if message:
            parts.append(message)

        return " | ".join(filter(None, parts))

    def format_test_start(self, test_name: str, **kwargs) -> str:
        """Format test start message for file."""
        separator = "=" * self.config.separator_length
        return f"\n{separator}\nStarting Test: {test_name}\n{separator}"

    def format_test_end(self, test_name: str, result: str, **kwargs) -> str:
        """Format test end message for file."""
        separator = "=" * self.config.separator_length
        return f"\n{separator}\nTest {result}: {test_name}\n{separator}\n"

    def format_assertion(
        self, assertion_type: str, expected: Any, actual: Any, **kwargs
    ) -> str:
        """Format assertion message for file."""
        parts = ["Assertion:"]

        if assertion_type:
            parts.append(f"Type: {assertion_type}")
        if expected is not None:
            parts.append(f"Expected: {expected}")
        if actual is not None:
            parts.append(f"Actual: {actual}")

        return " | ".join(parts)

    def format_error(self, error_type: str, error_message: str, **kwargs) -> str:
        """Format error message for file."""
        parts = ["Error:"]

        if error_type:
            parts.append(f"Type: {error_type}")
        if error_message:
            parts.append(error_message)

        return " | ".join(parts)
