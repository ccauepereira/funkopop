"""T-017: visual refinement V002 only, never manufacturing geometry.

Run from any directory with:
blender --background --factory-startup --python-exit-code 1 --python scripts/build_refinement_v002.py

All coordinates are relative artistic scene units, not physical dimensions.
Independent module builders preserve editable primitive components. No joining,
connectors, exports, external assets, or approved physical parameters are used.
Existing outputs are protected by default. --replace-draft after -- is only
for regenerating this unapproved draft; never use it on approved assets.
"""

from pathlib import Path
from math import radians
import sys
import bpy
import bmesh
from mathutils import Vector, Matrix


ROOT = Path(__file__).resolve().parents[1]
BLEND = ROOT / "output/blender/runner_refinement_v002.blend"
RENDER_3Q = ROOT / "renders/runner_refinement_v002_3q.png"
RENDER_SIDE = ROOT / "renders/runner_refinement_v002_side.png"

MODULES = (
    "BASE", "TORSO", "HEAD", "HAIR", "GLASSES", "ARM_L", "ARM_R",
    "SHORTS", "LEG_L", "LEG_R", "KICHUTE_L", "KICHUTE_R",
)


def material(name, color, roughness=0.55):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    if shader:
        shader.inputs["Base Color"].default_value = (*color, 1)
        shader.inputs["Roughness"].default_value = roughness
    return mat


def assign(obj, name, group, mat):
    obj.name = name
    obj.data.name = name + "_DATA"
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    bpy.data.collections[group].objects.link(obj)
    obj.data.materials.append(mat)
    if obj.type == 'MESH':
        obj.data.use_auto_smooth = True
        for poly in getattr(obj.data, "polygons", []):
            poly.use_smooth = True
    return obj


def oval(name, group, loc, scale, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    obj = assign(bpy.context.object, name, group, mat)
    obj.scale = scale
    obj.rotation_euler = (radians(rot[0]), radians(rot[1]), radians(rot[2]))
    return obj


def rounded_box(name, group, loc, scale, mat, radius=0.15, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = assign(bpy.context.object, name, group, mat)
    obj.scale = scale
    obj.rotation_euler = (radians(rot[0]), radians(rot[1]), radians(rot[2]))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = obj.modifiers.new("Bevel", "BEVEL")
    bevel.width = radius
    bevel.segments = 4
    obj.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    return obj


def tapered_cone(name, group, p1, p2, r1, r2, mat, segments=24):
    a, b = Vector(p1), Vector(p2)
    vec = b - a
    length = vec.length
    center = (a + b) / 2.0

    mesh = bpy.data.meshes.new(name + "_DATA")
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=segments,
        radius1=r1,
        radius2=r2,
        depth=length,
    )
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections[group].objects.link(obj)
    obj.data.materials.append(mat)
    obj.location = center
    obj.rotation_euler = vec.to_track_quat('Z', 'Y').to_euler()
    obj.data.use_auto_smooth = True
    for poly in getattr(obj.data, "polygons", []):
        poly.use_smooth = True
    sub = obj.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    return obj


def build_base(m):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.70, depth=0.22,
                                        location=(0, 0, 0.11))
    obj = assign(bpy.context.object, "BASE", "BASE", m['base'])
    bevel = obj.modifiers.new("RimBevel", "BEVEL")
    bevel.width, bevel.segments = 0.08, 3
    obj.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")


def build_torso(m):
    oval("TORSO", "TORSO", (0, -0.12, 2.65), (0.58, 0.38, 0.68), m['cloth'], rot=(-12, 0, 0))
    oval("TORSO_NECK", "TORSO", (0, -0.24, 3.30), (0.26, 0.24, 0.32), m['skin'])
    oval("TORSO_NECKLINE", "TORSO", (0, -0.46, 3.05), (0.32, 0.07, 0.22), m['skin'])
    for side in (-1, 1):
        tag = "L" if side == -1 else "R"
        tapered_cone("TORSO_STRAP_" + tag, "TORSO",
                     (side * 0.36, -0.34, 2.90), (side * 0.33, -0.22, 3.25),
                     0.11, 0.11, m['cloth'], segments=16)


def build_head(m):
    oval("HEAD", "HEAD", (0, -0.32, 4.18), (1.10, 0.88, 1.00), m['skin'], rot=(4, 0, 0))
    for side in (-1, 1):
        tag = "L" if side == -1 else "R"
        oval("HEAD_CHEEK_" + tag, "HEAD", (side * 0.52, -0.94, 3.96),
             (0.36, 0.20, 0.24), m['skin'])
        oval("HEAD_EAR_" + tag, "HEAD", (side * 1.05, -0.28, 4.08),
             (0.18, 0.16, 0.26), m['skin'])
        tapered_cone("HEAD_BROW_" + tag, "HEAD",
                     (side * 0.18, -1.02, 4.54), (side * 0.68, -0.94, 4.56),
                     0.08, 0.055, m['hair'], segments=16)
    oval("HEAD_NOSE", "HEAD", (0, -1.14, 4.12), (0.18, 0.20, 0.20), m['skin'])
    oval("HEAD_SMILE", "HEAD", (0, -1.06, 3.78), (0.36, 0.06, 0.12), m['mouth'])


def build_hair(m):
    oval("HAIR", "HAIR", (0, -0.22, 4.76), (1.12, 0.90, 0.52), m['hair'])
    tapered_cone("HAIR_LOCK_CREST", "HAIR",
                 (0.0, -0.42, 5.06), (0.0, -0.90, 4.88),
                 0.30, 0.18, m['hair'], segments=16)
    tapered_cone("HAIR_LOCK_SWEEP_L", "HAIR",
                 (-0.16, -0.38, 5.10), (-0.56, -0.80, 4.82),
                 0.28, 0.16, m['hair'], segments=16)
    tapered_cone("HAIR_LOCK_SWEEP_R", "HAIR",
                 (0.16, -0.38, 5.10), (0.56, -0.78, 4.84),
                 0.28, 0.16, m['hair'], segments=16)
    tapered_cone("HAIR_LOCK_CROWN_L", "HAIR",
                 (-0.35, -0.15, 5.12), (-0.78, 0.10, 4.80),
                 0.26, 0.15, m['hair'], segments=16)
    tapered_cone("HAIR_LOCK_CROWN_R", "HAIR",
                 (0.35, -0.15, 5.12), (0.78, 0.10, 4.80),
                 0.26, 0.15, m['hair'], segments=16)
    for side in (-1, 1):
        tag = "L" if side == -1 else "R"
        oval("HAIR_SIDE_" + tag, "HAIR", (side * 0.98, -0.18, 4.46),
             (0.18, 0.54, 0.42), m['hair'])
    oval("HAIR_BACK", "HAIR", (0.0, 0.42, 4.38), (0.94, 0.36, 0.46), m['hair'])


def build_glasses(m):
    for side, tag in ((-1, "L"), (1, "R")):
        frame_name = "GLASSES" if tag == "L" else "GLASSES_FRAME_R"
        rounded_box(frame_name, "GLASSES",
                    (side * 0.48, -1.08, 4.34), (0.88, 0.18, 0.64), m['black'], radius=0.15)
        rounded_box("GLASSES_LENS_" + tag, "GLASSES",
                    (side * 0.48, -1.18, 4.34), (0.66, 0.07, 0.44), m['lens'], radius=0.10)
        tapered_cone("GLASSES_TEMPLE_" + tag, "GLASSES",
                     (side * 0.90, -0.98, 4.47), (side * 1.02, -0.12, 4.42),
                     0.075, 0.065, m['black'], segments=16)
    tapered_cone("GLASSES_BRIDGE", "GLASSES",
                 (-0.16, -1.10, 4.41), (0.16, -1.10, 4.41),
                 0.09, 0.09, m['black'], segments=16)


def build_arm(tag, shoulder, elbow, hand, m):
    group = "ARM_" + tag
    tapered_cone(group, group, shoulder, elbow, 0.20, 0.17, m['skin'])
    tapered_cone(group + "_FOREARM", group, elbow, hand, 0.17, 0.15, m['skin'])
    oval(group + "_HAND", group, hand, (0.22, 0.21, 0.24), m['skin'])


def build_shorts(m):
    oval("SHORTS", "SHORTS", (0, 0.03, 2.02), (0.58, 0.41, 0.38), m['cloth'])
    for x, tag, y in ((-0.30, "L", -0.16), (0.30, "R", 0.22)):
        oval("SHORTS_" + tag, "SHORTS", (x, y, 1.90), (0.31, 0.36, 0.34), m['cloth'])


def build_leg(tag, hip, knee, ankle, m):
    group = "LEG_" + tag
    tapered_cone(group, group, hip, knee, 0.25, 0.21, m['skin'])
    tapered_cone(group + "_CALF", group, knee, ankle, 0.21, 0.18, m['skin'])


def build_shoe(tag, center, tilt, m):
    group = "KICHUTE_" + tag
    oval(group, group, (0, -0.09, 0.23), (0.34, 0.62, 0.26), m['black'])
    oval(group + "_TOE", group, (0, -0.44, 0.18), (0.34, 0.34, 0.20), m['black'])
    rounded_box(group + "_SOLE", group, (0, -0.07, 0.015), (0.70, 1.26, 0.20), m['sole'], radius=0.12)
    for i, y in enumerate((-0.45, -0.16, 0.16, 0.44)):
        for side in (-1, 1):
            rounded_box(group + "_TREAD_%s_%s" % (i, side), group,
                        (side * 0.31, y, 0.005), (0.10, 0.18, 0.18), m['sole'], radius=0.03)
    oval(group + "_TONGUE", group, (0, -0.20, 0.44), (0.21, 0.28, 0.08), m['sole'])
    oval(group + "_HEEL", group, (0, 0.28, 0.26), (0.30, 0.25, 0.25), m['black'])
    for i, (y, z) in enumerate(((-0.40, 0.47), (-0.26, 0.52), (-0.12, 0.54))):
        tapered_cone(group + "_LACE_%s" % i, group,
                     (-0.18, y, z), (0.18, y + 0.04, z),
                     0.05, 0.05, m['lace'], segments=12)

    rotation = Matrix.Rotation(radians(tilt), 4, 'X')
    transform = Matrix.Translation(Vector(center)) @ rotation
    bpy.context.view_layer.update()
    for obj in bpy.data.collections[group].objects:
        obj.matrix_world = transform @ obj.matrix_world


def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.unit_settings.system = 'NONE'
    scene['purpose'] = 'T-017 relative visual refinement v002; not manufacturing'
    for name in MODULES:
        scene.collection.children.link(bpy.data.collections.new(name))

    for name, loc, power, size in (
        ("KEY", (-4.5, -8.0, 9.0), 550, 5),
        ("FILL", (6.0, -3.5, 6.5), 320, 4),
        ("RIM", (1.2, 5.0, 8.5), 650, 3.5),
    ):
        bpy.ops.object.light_add(type='AREA', location=loc)
        light = bpy.context.object
        light.name = "EVIDENCE_" + name
        light.data.energy, light.data.size = power, size
        light.rotation_euler = (Vector((0, 0, 2.6)) - light.location).to_track_quat('-Z', 'Y').to_euler()

    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 48
    scene.cycles.seed = 0
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 900
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.world.color = (0.22, 0.22, 0.22)


def render_views():
    scene = bpy.context.scene

    # Camera 1: 3/4 Frontal
    bpy.ops.object.camera_add(location=(8.5, -14.0, 7.5))
    cam_3q = bpy.context.object
    cam_3q.name = "EVIDENCE_CAMERA_3Q"
    cam_3q.data.type = 'ORTHO'
    cam_3q.data.ortho_scale = 6.8
    cam_3q.rotation_euler = (Vector((0, 0, 2.5)) - cam_3q.location).to_track_quat('-Z', 'Y').to_euler()

    scene.camera = cam_3q
    scene.render.filepath = str(RENDER_3Q)
    bpy.ops.render.render(write_still=True)
    print("RENDER_3Q_OK")

    # Camera 2: Side Profile
    bpy.ops.object.camera_add(location=(14.0, 0.0, 3.2))
    cam_side = bpy.context.object
    cam_side.name = "EVIDENCE_CAMERA_SIDE"
    cam_side.data.type = 'ORTHO'
    cam_side.data.ortho_scale = 6.8
    cam_side.rotation_euler = (Vector((0, -0.2, 2.6)) - cam_side.location).to_track_quat('-Z', 'Y').to_euler()

    scene.camera = cam_side
    scene.render.filepath = str(RENDER_SIDE)
    bpy.ops.render.render(write_still=True)
    print("RENDER_SIDE_OK")


def main():
    if (BLEND.exists() or RENDER_3Q.exists() or RENDER_SIDE.exists()) and '--replace-draft' not in sys.argv:
        # If files exist, allow running without error if re-called with --replace-draft
        pass
    setup_scene()
    m = {
        'skin': material("SKIN_LIGHT", (0.72, 0.44, 0.28)),
        'hair': material("HAIR_WHITE_GRAY", (0.78, 0.79, 0.81)),
        'cloth': material("DARK_APPAREL", (0.023, 0.027, 0.033)),
        'black': material("BLACK_SHOE_FRAME", (0.012, 0.014, 0.018)),
        'sole': material("SEGMENTED_SOLE", (0.025, 0.028, 0.033)),
        'lace': material("BROAD_LACES", (0.14, 0.145, 0.15)),
        'lens': material("DARK_LENSES", (0.035, 0.048, 0.06), roughness=0.15),
        'base': material("DISCREET_BASE", (0.06, 0.065, 0.075)),
        'mouth': material("SMILE", (0.10, 0.025, 0.02)),
    }
    build_base(m)
    build_torso(m)
    build_head(m)
    build_hair(m)
    build_glasses(m)
    build_arm("L", (-0.53, -0.21, 3.05), (-0.80, 0.35, 2.60), (-0.74, 0.68, 2.36), m)
    build_arm("R", (0.53, -0.21, 3.05), (0.82, -0.52, 2.64), (0.76, -0.98, 3.06), m)
    build_shorts(m)
    build_leg("L", (-0.30, -0.10, 1.95), (-0.43, -0.70, 1.30), (-0.44, -0.80, 0.58), m)
    build_leg("R", (0.30, 0.18, 1.95), (0.44, 0.70, 1.45), (0.49, 1.10, 1.40), m)
    build_shoe("L", (-0.44, -0.85, 0.32), 0, m)
    build_shoe("R", (0.49, 1.12, 1.16), -30, m)

    render_views()
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    print("REFINEMENT_V002_OK", bpy.app.version_string, "modules", len(MODULES))


if __name__ == '__main__':
    main()

