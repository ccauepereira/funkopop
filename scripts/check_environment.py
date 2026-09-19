#!/usr/bin/env python3
"""Environment verification script for standard Python environment."""

import sys


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")

    try:
        import numpy as np
    except ImportError as exc:
        print(f"Error importing NumPy: {exc}", file=sys.stderr)
        return 1
    print(f"NumPy: {np.__version__}")

    try:
        import cv2
    except ImportError as exc:
        print(f"Error importing OpenCV: {exc}", file=sys.stderr)
        return 1
    print(f"OpenCV: {cv2.__version__}")

    print("Environment check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
