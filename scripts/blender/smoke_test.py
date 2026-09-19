#!/usr/bin/env python3
"""smoke_test.py — Automated validation of Astra Blender Workspace V1.

Tests:
  1. Scene loading & verification of units and standard collections.
  2. Creation of ASTRA_TEST_CUBE and ASTRA_TEST_SPHERE in 90_TEMP.
  3. Transformation of test objects.
  4. Movement of test objects between collections (90_TEMP -> 10_BLOCKOUT).
  5. Multi-camera rendering (FRONT, SIDE, BACK, THREE_QUARTER) to renders/smoke_test/.
  6. Scene audit reporting and verification.
  7. Saving and reloading of test .blend.
  8. Clean removal of test objects, preserving CALIBRATION_CUBE_20MM in runner_workspace_v001.blend.

Execution:
  blender --background --factory-startup --python-exit-code 1 --python scripts/blender/smoke_test.py
"""

import sys
from pathlib import Path

# Prevent pytest from collecting this file outside Blender
__test__ = False

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import bpy
    from mathutils import Euler, Vector
    import render_views
    import scene_audit
    import setup_workspace
except ImportError:
    pass

WORKSPACE_BLEND = REPO_ROOT / "output/blender/runner_workspace_v001.blend"
SMOKE_RENDER_DIR = REPO_ROOT / "renders/smoke_test"
TEMP_TEST_BLEND = REPO_ROOT / "output/blender/smoke_test_temp.blend"


def run_smoke_test() -> int:
    print("=" * 80)
    print("STARTING ASTRA BLENDER WORKSPACE V1 SMOKE TEST")
    print("=" * 80)

    # 1. Load workspace blend
    if not WORKSPACE_BLEND.exists():
        print(f"[FAIL] Workspace blend file not found at {WORKSPACE_BLEND}")
        return 1

    bpy.ops.wm.open_mainfile(filepath=str(WORKSPACE_BLEND))
    scene = bpy.context.scene
    print(f"[STEP 1] Loaded {WORKSPACE_BLEND.name}")
    print(f"         Units: system={scene.unit_settings.system}, scale_length={scene.unit_settings.scale_length}")

    # Check collections
    cols = {c.name for c in bpy.data.collections}
    for req_col in setup_workspace.COLLECTIONS_HIERARCHY:
        assert req_col in cols, f"Missing required collection: {req_col}"
    print(f"         All {len(setup_workspace.COLLECTIONS_HIERARCHY)} standard collections verified.")

    # 2. Create ASTRA_TEST_CUBE and ASTRA_TEST_SPHERE in 90_TEMP
    col_temp = bpy.data.collections["90_TEMP"]
    col_blockout = bpy.data.collections["10_BLOCKOUT"]

    bpy.ops.mesh.primitive_cube_add(size=15.0, location=(10.0, 10.0, 7.5))
    test_cube = bpy.context.object
    test_cube.name = "ASTRA_TEST_CUBE"
    setup_workspace.move_to_collection(test_cube, "90_TEMP")

    bpy.ops.mesh.primitive_uv_sphere_add(radius=8.0, location=(-10.0, -10.0, 8.0))
    test_sphere = bpy.context.object
    test_sphere.name = "ASTRA_TEST_SPHERE"
    setup_workspace.move_to_collection(test_sphere, "90_TEMP")

    assert test_cube.name in col_temp.objects, "ASTRA_TEST_CUBE not in 90_TEMP"
    assert test_sphere.name in col_temp.objects, "ASTRA_TEST_SPHERE not in 90_TEMP"
    print("[STEP 2] Successfully created ASTRA_TEST_CUBE and ASTRA_TEST_SPHERE in 90_TEMP")

    # 3. Test Transformation
    test_cube.location = (20.0, 0.0, 15.0)
    test_cube.rotation_euler = Euler((0.0, 0.0, 0.785), "XYZ")
    test_cube.scale = (1.5, 1.5, 1.5)
    bpy.ops.object.select_all(action="DESELECT")
    test_cube.select_set(True)
    bpy.context.view_layer.objects.active = test_cube
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assert abs(test_cube.scale[0] - 1.0) < 1e-4, f"Scale application failed on test cube: scale={test_cube.scale}"

    test_sphere.location = (-20.0, 0.0, 15.0)
    test_sphere.scale = (1.2, 1.2, 1.2)
    bpy.ops.object.select_all(action="DESELECT")
    test_sphere.select_set(True)
    bpy.context.view_layer.objects.active = test_sphere
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assert abs(test_sphere.scale[0] - 1.0) < 1e-4, f"Scale application failed on test sphere: scale={test_sphere.scale}"
    print("[STEP 3] Object transformations applied and scale normalized.")

    # 4. Move between collections (90_TEMP -> 10_BLOCKOUT)
    setup_workspace.move_to_collection(test_cube, "10_BLOCKOUT")
    setup_workspace.move_to_collection(test_sphere, "10_BLOCKOUT")

    assert test_cube.name in col_blockout.objects, "ASTRA_TEST_CUBE not in 10_BLOCKOUT"
    assert test_cube.name not in col_temp.objects, "ASTRA_TEST_CUBE still in 90_TEMP"
    assert test_sphere.name in col_blockout.objects, "ASTRA_TEST_SPHERE not in 10_BLOCKOUT"
    assert test_sphere.name not in col_temp.objects, "ASTRA_TEST_SPHERE still in 90_TEMP"
    print("[STEP 4] Successfully moved test objects from 90_TEMP to 10_BLOCKOUT.")

    # 5. Render 4 cameras
    print("[STEP 5] Rendering 4 camera views with test objects framed...")
    renders = render_views.render_all_views(
        output_dir=SMOKE_RENDER_DIR,
        prefix="smoke_",
        target_spec="10_BLOCKOUT",
        margin=1.35,
        samples=8,  # Fast samples for smoke test
        resolution=(400, 400),
        overwrite=True,
    )
    assert len(renders) == 4, f"Expected 4 renders, got {len(renders)}"
    for r in renders:
        assert r.exists() and r.stat().st_size > 1000, f"Render file missing or empty: {r}"
    print(f"         All 4 views rendered successfully to {SMOKE_RENDER_DIR}:")
    for r in renders:
        print(f"           - {r.name} ({r.stat().st_size} bytes)")

    # 6. Scene audit test
    print("[STEP 6] Running scene audit on active test scene...")
    audit = scene_audit.audit_scene(scene)
    test_obj_names = {o["name"] for o in audit["objects"]}
    assert "ASTRA_TEST_CUBE" in test_obj_names
    assert "ASTRA_TEST_SPHERE" in test_obj_names
    assert "CALIBRATION_CUBE_20MM" in test_obj_names
    print(f"         Audit detected {len(audit['objects'])} objects.")
    scene_audit.print_audit_report(audit)

    # 7. Test save & reload .blend
    print("[STEP 7] Testing temporary save and reload...")
    bpy.ops.wm.save_as_mainfile(filepath=str(TEMP_TEST_BLEND))
    assert TEMP_TEST_BLEND.exists(), "Temp test blend failed to save"
    bpy.ops.wm.open_mainfile(filepath=str(TEMP_TEST_BLEND))
    assert "ASTRA_TEST_CUBE" in bpy.data.objects, "Reload failed to retain test objects"
    TEMP_TEST_BLEND.unlink()
    print("         Save and reload verified. Temp blend cleaned up.")

    # 8. Clean removal of test objects & save clean workspace
    print("[STEP 8] Removing temporary test objects and restoring clean workspace...")
    scene = bpy.context.scene
    for obj_name in ("ASTRA_TEST_CUBE", "ASTRA_TEST_SPHERE"):
        obj = bpy.data.objects.get(obj_name)
        if obj:
            mesh = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if mesh:
                bpy.data.meshes.remove(mesh, do_unlink=True)

    # Verify test objects are completely gone
    assert "ASTRA_TEST_CUBE" not in bpy.data.objects, "ASTRA_TEST_CUBE still exists"
    assert "ASTRA_TEST_SPHERE" not in bpy.data.objects, "ASTRA_TEST_SPHERE still exists"

    # Verify CALIBRATION_CUBE_20MM is strictly preserved
    cal_cube = bpy.data.objects.get("CALIBRATION_CUBE_20MM")
    assert cal_cube is not None, "CALIBRATION_CUBE_20MM was accidentally deleted!"
    assert "30_ENGINEERING" in [c.name for c in cal_cube.users_collection]
    assert tuple(round(v, 2) for v in cal_cube.dimensions) == (20.0, 20.0, 20.0)

    # Re-frame cameras on CALIBRATION_CUBE_20MM
    setup_workspace.frame_cameras_to_target([cal_cube], margin=1.35)

    # Restore standard production resolution and sample settings
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.cycles.samples = 32

    # Save clean runner_workspace_v001.blend
    bpy.ops.wm.save_as_mainfile(filepath=str(WORKSPACE_BLEND))
    print(f"         Clean workspace re-saved to {WORKSPACE_BLEND.name}")

    # Final post-cleanup audit
    final_audit = scene_audit.audit_scene(bpy.context.scene)
    assert not final_audit["errors"], f"Final audit has errors: {final_audit['errors']}"
    assert not any("ASTRA_TEST" in o["name"] for o in final_audit["objects"])
    print("[FINAL AUDIT PASS] Workspace is clean, compliant, and ready for Astra.")
    print("=" * 80)
    print("SMOKE TEST: PASSED ALL CHECKS")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    ret = run_smoke_test()
    sys.exit(ret)
