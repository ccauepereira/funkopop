"""test_workspace_pipeline.py — Pytest suite verifying Astra Blender Workspace V1."""

from pathlib import Path
import subprocess
import struct
import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_BLEND = ROOT / "output/blender/runner_workspace_v001.blend"
CALIBRATION_STL = ROOT / "output/calibration/calibration_cube_20mm.stl"
SMOKE_TEST_SCRIPT = ROOT / "scripts/blender/smoke_test.py"
SETUP_SCRIPT = ROOT / "scripts/blender/setup_workspace.py"
SCENE_AUDIT_SCRIPT = ROOT / "scripts/blender/scene_audit.py"
RENDER_VIEWS_SCRIPT = ROOT / "scripts/blender/render_views.py"


def test_required_scripts_exist():
    """Verify that all required workspace scripts exist."""
    assert SETUP_SCRIPT.exists(), f"Missing {SETUP_SCRIPT}"
    assert SCENE_AUDIT_SCRIPT.exists(), f"Missing {SCENE_AUDIT_SCRIPT}"
    assert RENDER_VIEWS_SCRIPT.exists(), f"Missing {RENDER_VIEWS_SCRIPT}"
    assert SMOKE_TEST_SCRIPT.exists(), f"Missing {SMOKE_TEST_SCRIPT}"


def test_calibration_stl_dimensions():
    """Verify that calibration_cube_20mm.stl has exact 20x20x20mm bounding box and 12 facets."""
    assert CALIBRATION_STL.exists(), f"Missing {CALIBRATION_STL}"
    with open(CALIBRATION_STL, "rb") as f:
        header = f.read(80)
        facet_count = struct.unpack("<I", f.read(4))[0]
        assert facet_count == 12, f"Expected 12 facets for cube, got {facet_count}"

        min_v = [float("inf")] * 3
        max_v = [float("-inf")] * 3
        for _ in range(facet_count):
            facet = f.read(50)
            floats = struct.unpack("<12f", facet[:48])
            for v in (floats[3:6], floats[6:9], floats[9:12]):
                for i in range(3):
                    min_v[i] = min(min_v[i], v[i])
                    max_v[i] = max(max_v[i], v[i])

        dims = [round(max_v[i] - min_v[i], 4) for i in range(3)]
        assert dims == [20.0, 20.0, 20.0], f"Expected dimensions [20, 20, 20], got {dims}"


def test_blender_smoke_test_execution():
    """Execute smoke_test.py inside Blender and verify clean exit code."""
    cmd = [
        "blender",
        "--background",
        "--factory-startup",
        "--python-exit-code",
        "1",
        "--python",
        str(SMOKE_TEST_SCRIPT),
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    print("STDOUT:", proc.stdout)
    print("STDERR:", proc.stderr)
    assert proc.returncode == 0, f"Smoke test failed with return code {proc.returncode}:\n{proc.stdout}\n{proc.stderr}"
    assert "SMOKE TEST: PASSED ALL CHECKS" in proc.stdout
