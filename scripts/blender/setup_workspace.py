#!/usr/bin/env python3
"""setup_workspace.py — Prepares the reproducible technical workspace for Astra.

Sets up metric millimeter units, scene collections hierarchy, neutral studio lighting,
orthographic and perspective inspection cameras with target tracking, and creates the
initial 20mm calibration cube exported to STL for OrcaSlicer scale validation.

Execution:
  blender --background --factory-startup --python-exit-code 1 --python scripts/blender/setup_workspace.py [-- [OPTIONS]]

Options:
  --force               Allow overwriting output/blender/runner_workspace_v001.blend
  --no-export           Skip calibration cube STL export
  --output-blend PATH   Custom output blend path
  --output-stl PATH     Custom output STL path
"""

import argparse
from math import radians, tan
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BLEND_PATH = ROOT / "output/blender/runner_workspace_v001.blend"
DEFAULT_STL_PATH = ROOT / "output/calibration/calibration_cube_20mm.stl"

# Standard collections required for technical collectible pipeline
COLLECTIONS_HIERARCHY = [
    "00_REFERENCES",
    "01_CAMERAS",
    "02_LIGHTING",
    "10_BLOCKOUT",
    "20_CHARACTER",
    "30_ENGINEERING",
    "90_TEMP",
]

# Future character object naming convention (DO NOT instantiate in this script)
FUTURE_OBJECT_NAMES = (
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
)


def ensure_collection(name: str, parent: bpy.types.Collection = None) -> bpy.types.Collection:
    """Idempotently ensure a collection exists and is linked to parent."""
    if parent is None:
        parent = bpy.context.scene.collection
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
    if col.name not in parent.children:
        parent.children.link(col)
    return col


def move_to_collection(obj: bpy.types.Object, target_collection_name: str) -> None:
    """Move an object exclusively to the specified target collection."""
    target_col = ensure_collection(target_collection_name)
    for col in list(obj.users_collection):
        if col != target_col:
            col.objects.unlink(obj)
    if obj.name not in target_col.objects:
        target_col.objects.link(obj)


def configure_scene_units(scene: bpy.types.Scene) -> None:
    """Configure Blender for metric millimeter 3D printing workflow."""
    scene.unit_settings.system = "METRIC"
    # 1 Blender Unit = 1 millimeter (scale_length = 0.001)
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"
    scene["purpose"] = "Astra Technical Workspace V1 — FDM 3D Printing Millimeter Pipeline"
    scene["unit_system"] = "METRIC"
    scene["unit_scale"] = 0.001
    scene["unit_length"] = "MILLIMETERS"


def setup_collections(scene: bpy.types.Scene) -> dict[str, bpy.types.Collection]:
    """Ensure all standard pipeline collections are established."""
    cols = {}
    for col_name in COLLECTIONS_HIERARCHY:
        cols[col_name] = ensure_collection(col_name, parent=scene.collection)
    return cols


def create_or_update_track_constraint(obj: bpy.types.Object, target: bpy.types.Object) -> bpy.types.TrackToConstraint:
    """Ensure a TRACK_TO constraint points object -Z towards target with Y up."""
    constraint_name = "TRACK_TARGET"
    c = obj.constraints.get(constraint_name)
    if c is None:
        c = obj.constraints.new(type="TRACK_TO")
        c.name = constraint_name
    c.target = target
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return c


def setup_cameras(scene: bpy.types.Scene) -> dict[str, bpy.types.Object]:
    """Create or update FRONT, SIDE, BACK (orthographic) and 3Q (perspective) cameras."""
    cameras_col = ensure_collection("01_CAMERAS")

    # Camera target empty
    target_name = "TARGET_FRAME"
    target = bpy.data.objects.get(target_name)
    if target is None:
        target = bpy.data.objects.new(target_name, None)
        target.empty_display_type = "PLAIN_AXES"
        target.empty_display_size = 15.0
        cameras_col.objects.link(target)
    target.location = (0.0, 0.0, 10.0)
    move_to_collection(target, "01_CAMERAS")

    # Distance from target for placement
    cam_dist = 500.0  # mm
    target_z = 10.0   # mm

    specs = {
        "CAM_FRONT": {
            "type": "ORTHO",
            "ortho_scale": 60.0,
            "location": (0.0, -cam_dist, target_z),
            "lens": 50.0,
        },
        "CAM_SIDE": {
            "type": "ORTHO",
            "ortho_scale": 60.0,
            "location": (cam_dist, 0.0, target_z),
            "lens": 50.0,
        },
        "CAM_BACK": {
            "type": "ORTHO",
            "ortho_scale": 60.0,
            "location": (0.0, cam_dist, target_z),
            "lens": 50.0,
        },
        "CAM_3Q": {
            "type": "PERSP",
            "lens": 85.0,  # 85mm portrait perspective to avoid distortion
            "location": (350.0, -350.0, 250.0),
            "ortho_scale": 60.0,
        },
    }

    cams = {}
    for name, spec in specs.items():
        cam_obj = bpy.data.objects.get(name)
        if cam_obj is None:
            cam_data = bpy.data.cameras.new(name)
            cam_obj = bpy.data.objects.new(name, cam_data)
            cameras_col.objects.link(cam_obj)
        else:
            cam_data = cam_obj.data

        cam_data.type = spec["type"]
        if spec["type"] == "ORTHO":
            cam_data.ortho_scale = spec["ortho_scale"]
        else:
            cam_data.lens = spec["lens"]

        cam_data.clip_start = 0.1     # 0.1 mm
        cam_data.clip_end = 10000.0   # 10,000 mm (10 m)

        cam_obj.location = spec["location"]
        create_or_update_track_constraint(cam_obj, target)
        move_to_collection(cam_obj, "01_CAMERAS")
        cams[name] = cam_obj

    scene.camera = cams["CAM_FRONT"]
    return cams


def setup_lighting(scene: bpy.types.Scene, target: bpy.types.Object) -> dict[str, bpy.types.Object]:
    """Create or update neutral 3-point studio lighting for silhouette and volume reading."""
    lighting_col = ensure_collection("02_LIGHTING")

    specs = {
        "LIGHT_KEY": {
            "type": "AREA",
            "energy": 120.0,   # Watts
            "size": 400.0,     # mm (soft shadows)
            "color": (1.0, 1.0, 1.0),
            "location": (-250.0, -350.0, 350.0),
        },
        "LIGHT_FILL": {
            "type": "AREA",
            "energy": 60.0,
            "size": 500.0,
            "color": (0.95, 0.97, 1.0),  # Subtle cool fill
            "location": (300.0, -250.0, 200.0),
        },
        "LIGHT_RIM": {
            "type": "AREA",
            "energy": 90.0,
            "size": 300.0,
            "color": (1.0, 0.98, 0.95),  # Subtle warm rim separation
            "location": (0.0, 350.0, 400.0),
        },
    }

    lights = {}
    for name, spec in specs.items():
        light_obj = bpy.data.objects.get(name)
        if light_obj is None:
            light_data = bpy.data.lights.new(name, spec["type"])
            light_obj = bpy.data.objects.new(name, light_data)
            lighting_col.objects.link(light_obj)
        else:
            light_data = light_obj.data

        light_data.type = spec["type"]
        light_data.energy = spec["energy"]
        light_data.size = spec["size"]
        light_data.color = spec["color"]
        light_obj.location = spec["location"]
        create_or_update_track_constraint(light_obj, target)
        move_to_collection(light_obj, "02_LIGHTING")
        lights[name] = light_obj

    # Studio background world
    if scene.world is None:
        scene.world = bpy.data.worlds.new("STUDIO_WORLD")
    scene.world.use_nodes = False
    scene.world.color = (0.12, 0.12, 0.12)  # Neutral dark gray for clear silhouette contrast

    return lights


def create_or_update_calibration_cube() -> bpy.types.Object:
    """Create or verify CALIBRATION_CUBE_20MM in 30_ENGINEERING collection."""
    name = "CALIBRATION_CUBE_20MM"
    cube_obj = bpy.data.objects.get(name)

    if cube_obj is None:
        # Create standard mesh cube
        bpy.ops.mesh.primitive_cube_add(size=20.0, location=(0.0, 0.0, 10.0))
        cube_obj = bpy.context.object
        cube_obj.name = name
        cube_obj.data.name = f"{name}_DATA"
    else:
        cube_obj.location = (0.0, 0.0, 10.0)

    # Ensure uniform scale and correct dimensions
    cube_obj.scale = (1.0, 1.0, 1.0)
    cube_obj.dimensions = (20.0, 20.0, 20.0)

    # Assign neutral calibration material
    mat_name = "MAT_CALIBRATION_GRAY"
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.7, 0.7, 0.72, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.5
    if not cube_obj.data.materials:
        cube_obj.data.materials.append(mat)
    else:
        cube_obj.data.materials[0] = mat

    move_to_collection(cube_obj, "30_ENGINEERING")
    return cube_obj


def export_calibration_stl(cube_obj: bpy.types.Object, stl_path: Path) -> None:
    """Export ONLY CALIBRATION_CUBE_20MM to STL for OrcaSlicer scale validation."""
    stl_path.parent.mkdir(parents=True, exist_ok=True)

    # Select only the calibration cube
    bpy.ops.object.select_all(action="DESELECT")
    cube_obj.select_set(True)
    bpy.context.view_layer.objects.active = cube_obj

    # In Blender 4.0 with scale_length=0.001 (1 BU = 1 mm),
    # use_scene_unit=False with global_scale=1.0 writes raw coordinates (20 units = 20 mm).
    # Slicers interpret 1 STL unit as 1 mm.
    bpy.ops.export_mesh.stl(
        filepath=str(stl_path),
        check_existing=False,
        use_selection=True,
        global_scale=1.0,
        use_scene_unit=False,
        ascii=False,
        use_mesh_modifiers=True,
    )
    print(f"[STL EXPORT] Exported {cube_obj.name} to {stl_path}")
    print(f"  Dimensions: {cube_obj.dimensions}")
    print(f"  Parameters: use_selection=True, use_scene_unit=False, global_scale=1.0, ascii=False")


def get_objects_bounding_box(objects: list[bpy.types.Object]) -> tuple[Vector, Vector] | tuple[None, None]:
    """Calculate world-space bounding box for mesh objects."""
    min_co = Vector((float("inf"), float("inf"), float("inf")))
    max_co = Vector((float("-inf"), float("-inf"), float("-inf")))
    mesh_found = False

    for obj in objects:
        if obj.type != "MESH" or obj.hide_render:
            continue
        mesh_found = True
        for corner in obj.bound_box:
            world_pt = obj.matrix_world @ Vector(corner)
            for i in range(3):
                min_co[i] = min(min_co[i], world_pt[i])
                max_co[i] = max(max_co[i], world_pt[i])

    if not mesh_found:
        return None, None
    return min_co, max_co


def frame_cameras_to_target(target_objects: list[bpy.types.Object], margin: float = 1.35) -> None:
    """Automatically frame all workspace cameras on the specified target objects."""
    min_co, max_co = get_objects_bounding_box(target_objects)
    if min_co is None:
        return

    center = (min_co + max_co) / 2.0
    size = max_co - min_co
    max_span = max(size.x, size.y, size.z, 10.0)

    # Update TARGET_FRAME position
    target = bpy.data.objects.get("TARGET_FRAME")
    if target:
        target.location = center

    # Distance proportional to object size for perspective camera
    dist = max(max_span * 2.5, 100.0)

    # Update cameras
    cams = {
        "CAM_FRONT": {"dir": Vector((0.0, -1.0, 0.0)), "span": max(size.x, size.z)},
        "CAM_SIDE": {"dir": Vector((1.0, 0.0, 0.0)), "span": max(size.y, size.z)},
        "CAM_BACK": {"dir": Vector((0.0, 1.0, 0.0)), "span": max(size.x, size.z)},
    }

    for cam_name, info in cams.items():
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            cam_obj.location = center + info["dir"] * dist
            cam_obj.data.ortho_scale = max(info["span"] * margin, 25.0)

    cam_3q = bpy.data.objects.get("CAM_3Q")
    if cam_3q:
        dir_3q = Vector((1.0, -1.0, 0.75)).normalized()
        cam_3q.location = center + dir_3q * dist * 1.2


def clean_startup_defaults() -> None:
    """Remove unwanted default startup objects if starting from blank scene."""
    default_names = ("Cube", "Light", "Camera")
    for name in default_names:
        obj = bpy.data.objects.get(name)
        if obj is not None and obj.name not in ("CALIBRATION_CUBE_20MM", "TARGET_FRAME"):
            bpy.data.objects.remove(obj, do_unlink=True)
    # Remove default 'Collection' if empty
    default_col = bpy.data.collections.get("Collection")
    if default_col and len(default_col.objects) == 0:
        bpy.data.collections.remove(default_col)


def setup_workspace(
    blend_path: Path = DEFAULT_BLEND_PATH,
    stl_path: Path = DEFAULT_STL_PATH,
    force: bool = False,
    export_stl: bool = True,
) -> int:
    """Full workspace setup pipeline."""
    if blend_path.exists() and not force:
        print(f"[ERROR] Output blend already exists: {blend_path}")
        print("Use --force to update existing workspace without silent overwrite.")
        return 1

    blend_path.parent.mkdir(parents=True, exist_ok=True)
    stl_path.parent.mkdir(parents=True, exist_ok=True)

    clean_startup_defaults()
    scene = bpy.context.scene

    # 1. Units & Scale
    configure_scene_units(scene)

    # 2. Collections
    cols = setup_collections(scene)
    print(f"[WORKSPACE] Established {len(cols)} collections: {list(cols.keys())}")

    # 3. Cameras & Target
    cams = setup_cameras(scene)
    target = bpy.data.objects.get("TARGET_FRAME")
    print(f"[WORKSPACE] Configured {len(cams)} cameras: {list(cams.keys())}")

    # 4. Lighting
    lights = setup_lighting(scene, target)
    print(f"[WORKSPACE] Configured {len(lights)} lights: {list(lights.keys())}")

    # 5. Calibration Cube 20mm
    cube = create_or_update_calibration_cube()
    print(f"[WORKSPACE] Created/verified {cube.name} with dimensions {cube.dimensions}")

    # Auto-frame cameras on the calibration cube
    frame_cameras_to_target([cube], margin=1.35)

    # 6. STL Export
    if export_stl:
        export_calibration_stl(cube, stl_path)

    # Configure Cycles CPU rendering defaults for silhouette QA
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    # Save .blend mainfile
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"[WORKSPACE] Saved workspace to {blend_path}")
    return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Setup Astra Blender Workspace V1")
    parser.add_argument("--force", action="store_true", help="Allow overwrite of workspace file")
    parser.add_argument("--no-export", action="store_true", help="Skip calibration cube STL export")
    parser.add_argument("--output-blend", type=str, default=str(DEFAULT_BLEND_PATH), help="Path to output .blend")
    parser.add_argument("--output-stl", type=str, default=str(DEFAULT_STL_PATH), help="Path to output calibration STL")

    # If invoked inside Blender, parse arguments following '--'
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    return parser.parse_args(argv)


def main():
    args = parse_args()
    ret = setup_workspace(
        blend_path=Path(args.output_blend),
        stl_path=Path(args.output_stl),
        force=args.force,
        export_stl=not args.no_export,
    )
    sys.exit(ret)


if __name__ == "__main__":
    main()
