#!/usr/bin/env python3
"""scene_audit.py — Non-destructive QA inspection tool for Blender scenes.

Audits scene units, collection hierarchy, object transforms, dimensions, mesh statistics,
and checks for naming anomalies (e.g. '.001' suffixes, unapplied scale, orphaned objects).

Execution:
  blender <file.blend> --background --factory-startup --python-exit-code 1 --python scripts/blender/scene_audit.py [-- [OPTIONS]]
Or run directly specifying --blend:
  blender --background --factory-startup --python-exit-code 1 --python scripts/blender/scene_audit.py -- --blend output/blender/runner_workspace_v001.blend

Options:
  --blend PATH       Path to .blend file to audit (if not already opened)
  --json PATH        Export audit results to a JSON file
  --strict           Return non-zero exit code if warnings or anomalies are detected
"""

import argparse
import json
from math import degrees
from pathlib import Path
import re
import sys
import bpy

STANDARD_COLLECTIONS = {
    "00_REFERENCES",
    "01_CAMERAS",
    "02_LIGHTING",
    "10_BLOCKOUT",
    "20_CHARACTER",
    "30_ENGINEERING",
    "90_TEMP",
}

EXPECTED_WORKSPACE_OBJECTS = {
    "TARGET_FRAME",
    "CAM_FRONT",
    "CAM_SIDE",
    "CAM_BACK",
    "CAM_3Q",
    "LIGHT_KEY",
    "LIGHT_FILL",
    "LIGHT_RIM",
    "CALIBRATION_CUBE_20MM",
}

# Future convention objects allowed during character modeling
FUTURE_CONVENTION_OBJECTS = {
    "HEAD",
    "HAIR",
    "CAP",
    "GLASSES",
    "TORSO",
    "SHORTS",
    "ARM_L",
    "ARM_R",
    "LEG_L",
    "LEG_R",
    "KICHUTE_L",
    "KICHUTE_R",
    "BASE",
}


def audit_scene(scene: bpy.types.Scene) -> dict:
    """Perform comprehensive read-only audit of the given scene."""
    audit = {
        "scene_name": scene.name,
        "units": {
            "system": scene.unit_settings.system,
            "scale_length": scene.unit_settings.scale_length,
            "length_unit": scene.unit_settings.length_unit,
        },
        "render": {
            "engine": scene.render.engine,
            "resolution": [scene.render.resolution_x, scene.render.resolution_y],
        },
        "collections": [],
        "missing_standard_collections": [],
        "objects": [],
        "warnings": [],
        "errors": [],
    }

    # Verify standard collections
    existing_cols = {c.name for c in bpy.data.collections}
    audit["collections"] = sorted(list(existing_cols))
    missing = STANDARD_COLLECTIONS - existing_cols
    if missing:
        audit["missing_standard_collections"] = sorted(list(missing))
        audit["warnings"].append(f"Missing standard collections: {sorted(list(missing))}")

    # Check unit settings
    if scene.unit_settings.system != "METRIC":
        audit["warnings"].append(f"Unit system is '{scene.unit_settings.system}', expected 'METRIC'")
    if abs(scene.unit_settings.scale_length - 0.001) > 1e-6:
        audit["warnings"].append(
            f"Unit scale_length is {scene.unit_settings.scale_length}, expected 0.001 (1 BU = 1 mm)"
        )
    if scene.unit_settings.length_unit != "MILLIMETERS":
        audit["warnings"].append(
            f"Length unit is '{scene.unit_settings.length_unit}', expected 'MILLIMETERS'"
        )

    # Inspect objects
    duplicate_name_pattern = re.compile(r"\.\d{3}$")

    for obj in bpy.data.objects:
        obj_cols = [c.name for c in obj.users_collection]
        loc = [round(v, 4) for v in obj.location]
        rot_deg = [round(degrees(v), 2) for v in obj.rotation_euler]
        scale = [round(v, 4) for v in obj.scale]
        dims = [round(v, 4) for v in obj.dimensions]

        obj_data = {
            "name": obj.name,
            "type": obj.type,
            "collections": obj_cols,
            "location_mm": loc,
            "rotation_deg": rot_deg,
            "scale": scale,
            "dimensions_mm": dims,
            "hide_viewport": obj.hide_viewport,
            "hide_render": obj.hide_render,
            "modifiers": [m.name for m in obj.modifiers],
        }

        # Mesh-specific stats
        if obj.type == "MESH" and obj.data:
            mesh = obj.data
            obj_data["mesh_stats"] = {
                "vertices": len(mesh.vertices),
                "edges": len(mesh.edges),
                "polygons": len(mesh.polygons),
                "materials": [m.name for m in mesh.materials if m],
            }

        audit["objects"].append(obj_data)

        # Anomaly checks
        # 1. Accidental duplicate suffix check (e.g. Cube.001)
        if duplicate_name_pattern.search(obj.name):
            msg = f"Object '{obj.name}' has duplicate index suffix (e.g. .001). Stable explicit names required."
            audit["warnings"].append(msg)

        # 2. Unapplied scale check
        is_scaled = any(abs(s - 1.0) > 1e-4 for s in obj.scale)
        if is_scaled and obj.type == "MESH":
            msg = f"Object '{obj.name}' has unapplied scale {scale}. For 3D printing, apply scale before export."
            audit["warnings"].append(msg)

        # 3. Orphaned object check (in root or no collection)
        if not obj_cols:
            audit["warnings"].append(f"Object '{obj.name}' is orphaned (not in any collection).")
        elif all(c not in STANDARD_COLLECTIONS for c in obj_cols):
            audit["warnings"].append(f"Object '{obj.name}' is outside standard collections: {obj_cols}")

        # 4. Unexpected name alert
        allowed_names = EXPECTED_WORKSPACE_OBJECTS | FUTURE_CONVENTION_OBJECTS
        # Allow prefix matches for submodules (e.g. KICHUTE_L_SOLE, ASTRA_TEST_*)
        is_known = obj.name in allowed_names or any(obj.name.startswith(p) for p in allowed_names) or obj.name.startswith("ASTRA_TEST_")
        if not is_known:
            audit["warnings"].append(f"Object '{obj.name}' is not in known/approved naming conventions.")

    return audit


def print_audit_report(audit: dict) -> None:
    """Render human-readable terminal audit summary."""
    print("=" * 80)
    print(f"SCENE AUDIT REPORT — {audit['scene_name']}")
    print("=" * 80)
    print("UNITS & SCALE:")
    print(f"  System:       {audit['units']['system']}")
    print(f"  Scale Length: {audit['units']['scale_length']} (1 BU = 1 mm)")
    print(f"  Length Unit:  {audit['units']['length_unit']}")
    print(f"  Render Engine:{audit['render']['engine']} ({audit['render']['resolution'][0]}x{audit['render']['resolution'][1]})")

    print("\nCOLLECTIONS:")
    for col in audit["collections"]:
        status = "[STANDARD]" if col in STANDARD_COLLECTIONS else "[CUSTOM]"
        print(f"  {status:12} {col}")

    if audit["missing_standard_collections"]:
        print("\nMISSING STANDARD COLLECTIONS:")
        for col in audit["missing_standard_collections"]:
            print(f"  [MISSING]   {col}")

    print(f"\nOBJECTS ({len(audit['objects'])} total):")
    print(f"{'NAME':<24} {'TYPE':<8} {'COLLECTION':<18} {'DIMS (X,Y,Z mm)':<20} {'SCALE':<14} {'VIS':<6}")
    print("-" * 96)
    for obj in audit["objects"]:
        col_str = ",".join(obj["collections"]) if obj["collections"] else "NONE"
        dims_str = f"{obj['dimensions_mm'][0]:.1f}, {obj['dimensions_mm'][1]:.1f}, {obj['dimensions_mm'][2]:.1f}"
        scale_str = f"{obj['scale'][0]:.2f}, {obj['scale'][1]:.2f}, {obj['scale'][2]:.2f}"
        vis = "R+V" if not obj["hide_viewport"] and not obj["hide_render"] else "HID"
        print(f"{obj['name']:<24} {obj['type']:<8} {col_str:<18} {dims_str:<20} {scale_str:<14} {vis:<6}")
        if "mesh_stats" in obj:
            stats = obj["mesh_stats"]
            mats = ",".join(stats["materials"]) if stats["materials"] else "None"
            print(f"    Mesh stats: {stats['vertices']} verts, {stats['edges']} edges, {stats['polygons']} faces | Mats: {mats}")

    print("\nANOMALIES / AUDIT FINDINGS:")
    if audit["errors"]:
        print(f"  ERRORS ({len(audit['errors'])}):")
        for err in audit["errors"]:
            print(f"    [!] {err}")
    if audit["warnings"]:
        print(f"  WARNINGS ({len(audit['warnings'])}):")
        for w in audit["warnings"]:
            print(f"    [*] {w}")
    if not audit["errors"] and not audit["warnings"]:
        print("  [PASS] Scene is fully compliant with workspace specifications.")
    print("=" * 80)


def parse_args():
    parser = argparse.ArgumentParser(description="Audit Blender Scene against Workspace V1 Spec")
    parser.add_argument("--blend", type=str, default="", help="Path to .blend file to inspect")
    parser.add_argument("--json", type=str, default="", help="Path to export JSON audit output")
    parser.add_argument("--strict", action="store_true", help="Fail if any warnings or errors are present")

    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    return parser.parse_args(argv)


def main():
    args = parse_args()
    if args.blend:
        blend_path = Path(args.blend).resolve()
        if not blend_path.exists():
            print(f"[ERROR] Blend file does not exist: {blend_path}")
            sys.exit(1)
        bpy.ops.wm.open_mainfile(filepath=str(blend_path))

    scene = bpy.context.scene
    audit = audit_scene(scene)
    print_audit_report(audit)

    if args.json:
        json_path = Path(args.json).resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2)
        print(f"[AUDIT] Exported JSON audit to {json_path}")

    has_issues = bool(audit["errors"]) or (args.strict and bool(audit["warnings"]))
    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
