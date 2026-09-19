#!/usr/bin/env python3
"""Environment verification script for Blender's embedded Python environment."""

import sys
import bpy


def main() -> int:
    print(f"Blender version: {bpy.app.version_string}")
    print(f"Blender embedded Python: {sys.version.split()[0]}")
    print(f"bpy.app.version_string: {bpy.app.version_string}")
    print("Blender environment check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
