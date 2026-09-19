#!/usr/bin/env python3
"""render_views.py — Multi-angle QA rendering tool for Astra Blender Workspace.

Renders FRONT, SIDE, BACK, and THREE_QUARTER views from standard workspace cameras,
supporting auto-framing on target objects or collections, versioned output directories,
and overwrite protection.

Execution:
  blender <file.blend> --background --factory-startup --python-exit-code 1 --python scripts/blender/render_views.py [-- [OPTIONS]]
Or run specifying --blend:
  blender --background --factory-startup --python-exit-code 1 --python scripts/blender/render_views.py -- --blend output/blender/runner_workspace_v001.blend --output-dir renders/workspace_v001

Options:
  --blend PATH          Path to .blend file to load (if not already opened)
  --output-dir PATH     Directory where renders will be saved (e.g. renders/workspace_v001)
  --prefix STR          Optional prefix for generated filenames (default: empty)
  --target STR          Object name or collection name to frame (default: auto-detect visible meshes)
  --margin FLOAT        Framing margin multiplier (default: 1.35)
  --samples INT         Cycles rendering sample count (default: 32)
  --resolution WIDTHxHEIGHT  Output image resolution (default: 1000x1000)
  --overwrite           Allow overwriting existing render files
"""

import argparse
from pathlib import Path
import sys
import bpy
from mathutils import Vector

CAMERA_VIEW_MAP = {
    "CAM_FRONT": "front",
    "CAM_SIDE": "side",
    "CAM_BACK": "back",
    "CAM_3Q": "three_quarter",
}


def get_target_objects(target_spec: str = "") -> list[bpy.types.Object]:
    """Resolve target specification to a list of mesh objects for camera framing."""
    if target_spec:
        # Check if target is a collection
        col = bpy.data.collections.get(target_spec)
        if col:
            return [o for o in col.all_objects if o.type == "MESH" and not o.hide_render]
        # Check if target is an object
        obj = bpy.data.objects.get(target_spec)
        if obj and obj.type == "MESH":
            return [obj]
        print(f"[WARN] Target '{target_spec}' not found or has no meshes. Falling back to all visible meshes.")

    # Default: collect all visible meshes excluding temporary/reference meshes
    visible_meshes = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH" and not obj.hide_render:
            # Skip reference planes
            is_ref = any(c.name == "00_REFERENCES" for c in obj.users_collection)
            if not is_ref:
                visible_meshes.append(obj)
    return visible_meshes


def calculate_bounding_box(objects: list[bpy.types.Object]) -> tuple[Vector, Vector] | tuple[None, None]:
    """Calculate world-space bounding box for a set of objects."""
    min_co = Vector((float("inf"), float("inf"), float("inf")))
    max_co = Vector((float("-inf"), float("-inf"), float("-inf")))
    found = False

    for obj in objects:
        if obj.type != "MESH" or obj.hide_render:
            continue
        found = True
        for corner in obj.bound_box:
            pt = obj.matrix_world @ Vector(corner)
            for i in range(3):
                min_co[i] = min(min_co[i], pt[i])
                max_co[i] = max(max_co[i], pt[i])

    if not found:
        return None, None
    return min_co, max_co


def frame_cameras(target_objects: list[bpy.types.Object], margin: float = 1.35) -> None:
    """Dynamically frame all 4 cameras on target objects."""
    min_co, max_co = calculate_bounding_box(target_objects)
    if min_co is None:
        print("[FRAMING] No mesh geometry found to frame. Using existing camera placements.")
        return

    center = (min_co + max_co) / 2.0
    size = max_co - min_co
    max_span = max(size.x, size.y, size.z, 10.0)

    # Update TARGET_FRAME
    target = bpy.data.objects.get("TARGET_FRAME")
    if target:
        target.location = center

    # Distance proportional to object size
    dist = max(max_span * 2.5, 100.0)

    ortho_cams = {
        "CAM_FRONT": {"dir": Vector((0.0, -1.0, 0.0)), "span": max(size.x, size.z)},
        "CAM_SIDE": {"dir": Vector((1.0, 0.0, 0.0)), "span": max(size.y, size.z)},
        "CAM_BACK": {"dir": Vector((0.0, 1.0, 0.0)), "span": max(size.x, size.z)},
    }

    for cam_name, info in ortho_cams.items():
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            cam_obj.location = center + info["dir"] * dist
            cam_obj.data.ortho_scale = max(info["span"] * margin, 20.0)

    cam_3q = bpy.data.objects.get("CAM_3Q")
    if cam_3q:
        dir_3q = Vector((1.0, -1.0, 0.75)).normalized()
        cam_3q.location = center + dir_3q * dist * 1.2

    # Force dependency graph update
    bpy.context.view_layer.update()
    print(f"[FRAMING] Framed cameras around center ({center.x:.1f}, {center.y:.1f}, {center.z:.1f}) span {max_span:.1f} mm")


def render_all_views(
    output_dir: Path,
    prefix: str = "",
    target_spec: str = "",
    margin: float = 1.35,
    samples: int = 32,
    resolution: tuple[int, int] = (1000, 1000),
    overwrite: bool = False,
) -> list[Path]:
    """Render FRONT, SIDE, BACK, and THREE_QUARTER camera views."""
    output_dir.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene

    # Framing
    target_objects = get_target_objects(target_spec)
    if target_objects:
        frame_cameras(target_objects, margin=margin)

    # Render engine settings
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    rendered_files = []

    for cam_name, view_suffix in CAMERA_VIEW_MAP.items():
        cam_obj = bpy.data.objects.get(cam_name)
        if not cam_obj:
            print(f"[WARN] Camera '{cam_name}' not found in scene! Skipping.")
            continue

        filename = f"{prefix}{view_suffix}.png" if prefix else f"{view_suffix}.png"
        filepath = output_dir / filename

        if filepath.exists() and not overwrite:
            print(f"[ERROR] Output file already exists: {filepath}")
            print("Set --overwrite to replace existing render artifacts.")
            sys.exit(1)

        scene.camera = cam_obj
        scene.render.filepath = str(filepath)

        print(f"[RENDER] Rendering view '{view_suffix}' via {cam_name} -> {filepath.name} ...")
        bpy.ops.render.render(write_still=True)
        print(f"         Done: {filepath} ({filepath.stat().st_size} bytes)")
        rendered_files.append(filepath)

    return rendered_files


def parse_args():
    parser = argparse.ArgumentParser(description="Render Standard Character/Workspace Views")
    parser.add_argument("--blend", type=str, default="", help="Path to .blend file to open")
    parser.add_argument("--output-dir", type=str, required=True, help="Directory to save renders")
    parser.add_argument("--prefix", type=str, default="", help="Filename prefix (e.g. 'v001_')")
    parser.add_argument("--target", type=str, default="", help="Target object or collection to frame")
    parser.add_argument("--margin", type=float, default=1.35, help="Framing margin multiplier")
    parser.add_argument("--samples", type=int, default=32, help="Cycles samples")
    parser.add_argument("--resolution", type=str, default="1000x1000", help="Resolution WxH")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting existing files")

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
            print(f"[ERROR] Blend file not found: {blend_path}")
            sys.exit(1)
        bpy.ops.wm.open_mainfile(filepath=str(blend_path))

    res_parts = args.resolution.lower().split("x")
    resolution = (int(res_parts[0]), int(res_parts[1]))

    out_dir = Path(args.output_dir).resolve()
    rendered = render_all_views(
        output_dir=out_dir,
        prefix=args.prefix,
        target_spec=args.target,
        margin=args.margin,
        samples=args.samples,
        resolution=resolution,
        overwrite=args.overwrite,
    )
    print(f"\n[SUMMARY] Successfully generated {len(rendered)} view renders in {out_dir}")


if __name__ == "__main__":
    main()
