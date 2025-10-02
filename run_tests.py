#!/usr/bin/env python3
"""
Simple script to run Robot Framework tests with custom logger
"""

import subprocess
import sys
import os


def run_robot_tests():
    """Run Robot Framework tests."""

    # Check if robot is installed
    try:
        subprocess.run(["robot", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Robot Framework not found!")
        print("Install it with: pip install robotframework")
        return False

    # Run the test suite
    print("🚀 Running Robot Framework tests with custom logger...")
    print("=" * 60)

    try:
        result = subprocess.run(
            [
                "robot",
                "--outputdir",
                "results",
                "--log",
                "log.html",
                "--report",
                "report.html",
                "test_suite.robot",
            ],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")

        print(f"\n📊 Results saved in 'results' directory")
        print(f"📄 Open 'results/log.html' to view detailed logs")
        print(f"📈 Open 'results/report.html' to view test report")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_robot_tests()
    sys.exit(0 if success else 1)
