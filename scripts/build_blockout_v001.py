"""T-015: visual blockout only, never manufacturing geometry.

Run from any directory with Blender --background --factory-startup
--python-exit-code 1 --python scripts/build_blockout_v001.py.
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
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BLEND = ROOT / "output/blender/runner_blockout_v001.blend"
RENDER = ROOT / "renders/runner_blockout_v001.png"
MODULES = (
    "BASE", "TORSO", "HEAD", "HAIR", "GLASSES", "ARM_L", "ARM_R",
    "SHORTS", "LEG_L", "LEG_R", "KICHUTE_L", "KICHUTE_R",
)


def material(name, color, roughness=0.55):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    return mat


def assign(obj, name, group, mat):
    obj.name = name
    obj.data.name = name + "_DATA"
    for collection in list(obj.users_collection):
        collection.objects.unlink(obj)
    bpy.data.collections[group].objects.link(obj)
    obj.data.materials.append(mat)
    if obj.type == 'MESH':
        obj.data.use_auto_smooth = True
    for polygon in getattr(obj.data, "polygons", []):
        polygon.use_smooth = True
    return obj


def oval(name, group, loc, scale, mat, tilt=0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    obj = assign(bpy.context.object, name, group, mat)
    obj.scale = scale
    obj.rotation_euler[0] = radians(tilt)
    return obj


def rounded(name, group, loc, scale, mat, radius=0.15):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = assign(bpy.context.object, name, group, mat)
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = obj.modifiers.new("Soft_blockout_edges", "BEVEL")
    bevel.width = radius
    bevel.segments = 4
    obj.modifiers.new("Balanced_normals", "WEIGHTED_NORMAL")
    return obj


def segment(name, group, start, end, radius, mat):
    a, b = Vector(start), Vector(end)
    obj = oval(name, group, (a + b) / 2,
               (radius, radius, (b - a).length / 2 + radius * 0.55), mat)
    obj.rotation_euler = (b - a).to_track_quat('Z', 'Y').to_euler()
    return obj


def build_base(m):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.65, depth=0.22,
                                      location=(0, 0, 0.11))
    obj = assign(bpy.context.object, "BASE", "BASE", m['base'])
    bevel = obj.modifiers.new("Rounded_rim", "BEVEL")
    bevel.width, bevel.segments = 0.07, 3
    obj.modifiers.new("Balanced_normals", "WEIGHTED_NORMAL")


def build_torso(m):
    oval("TORSO", "TORSO", (0, -0.12, 2.66), (.57, .38, .69), m['cloth'], -12)
    oval("TORSO_NECK", "TORSO", (0, -.25, 3.3), (.26, .24, .32), m['skin'])
    oval("TORSO_NECKLINE", "TORSO", (0, -.46, 3.05), (.3, .065, .22), m['skin'])
    for side in (-1, 1):
        segment("TORSO_STRAP_" + str(side), "TORSO",
                (side * .37, -.35, 2.9), (side * .35, -.24, 3.23), .12, m['cloth'])


def build_head(m):
    oval("HEAD", "HEAD", (0, -.35, 4.16), (1.0, .79, .98), m['skin'])
    for side in (-1, 1):
        oval("HEAD_EAR_" + str(side), "HEAD", (side * .98, -.3, 4.05),
             (.18, .16, .27), m['skin'])
        oval("HEAD_CHEEK_" + str(side), "HEAD", (side * .49, -.96, 3.96),
             (.35, .17, .25), m['skin'])
        segment("HEAD_BROW_" + str(side), "HEAD",
                (side * .18, -1.015, 4.52), (side * .67, -.94, 4.54), .075, m['hair'])
    oval("HEAD_NOSE", "HEAD", (0, -1.13, 4.1), (.19, .22, .22), m['skin'])
    oval("HEAD_SMILE", "HEAD", (0, -1.064, 3.79), (.35, .05, .115), m['mouth'])
    oval("HEAD_SMILE_TEETH", "HEAD", (0, -1.10, 3.825), (.28, .025, .045), m['teeth'])


def build_hair(m):
    oval("HAIR", "HAIR", (0, -.25, 4.77), (1.03, .8, .48), m['hair'])
    # Broad overlapping locks: no individual strands or microscopic texture.
    for index, x in enumerate((-.8, -.48, -.12, .24, .6, .85)):
        z = 4.85 + .22 * (1 - abs(x))
        lock = oval("HAIR_SWEEP_%02d" % index, "HAIR", (x, -.69, z),
                    (.27, .38, .28), m['hair'])
        lock.rotation_euler[1] = radians(-28)
    for side in (-1, 1):
        oval("HAIR_SIDE_" + str(side), "HAIR", (side * .89, -.16, 4.49),
             (.19, .56, .44), m['hair'])
        oval("HAIR_TEMPLE_" + str(side), "HAIR", (side * .9, -.5, 4.32),
             (.105, .16, .27), m['hair'])


def build_glasses(m):
    for side, tag in ((-1, "L"), (1, "R")):
        rounded("GLASSES" if tag == "L" else "GLASSES_FRAME_R", "GLASSES",
                (side * .48, -1.075, 4.33), (.87, .19, .64), m['black'], .16)
        rounded("GLASSES_LENS_" + tag, "GLASSES", (side * .48, -1.182, 4.33),
                (.64, .065, .42), m['lens'], .12)
        segment("GLASSES_TEMPLE_" + tag, "GLASSES", (side * .89, -.99, 4.47),
                (side * .98, -.12, 4.42), .075, m['black'])
    segment("GLASSES_BRIDGE", "GLASSES", (-.16, -1.1, 4.4), (.16, -1.1, 4.4),
            .09, m['black'])


def build_arm(tag, shoulder, elbow, hand, m):
    group = "ARM_" + tag
    segment(group, group, shoulder, elbow, .19, m['skin'])
    oval(group + "_ELBOW", group, elbow, (.2, .2, .2), m['skin'])
    segment(group + "_FOREARM", group, elbow, hand, .17, m['skin'])
    oval(group + "_HAND", group, hand, (.23, .22, .25), m['skin'])


def build_shorts(m):
    oval("SHORTS", "SHORTS", (0, .03, 2.03), (.56, .4, .36), m['cloth'])
    for x, tag, y in ((-.3, "L", -.16), (.3, "R", .23)):
        oval("SHORTS_" + tag, "SHORTS", (x, y, 1.91), (.3, .35, .34), m['cloth'])


def build_leg(tag, hip, knee, ankle, m):
    group = "LEG_" + tag
    segment(group, group, hip, knee, .245, m['skin'])
    oval(group + "_KNEE", group, knee, (.235, .24, .23), m['skin'])
    segment(group + "_CALF", group, knee, ankle, .195, m['skin'])


def build_shoe(tag, center, tilt, m):
    group = "KICHUTE_" + tag
    # All local shoe values describe appearance only; they are not dimensions.
    oval(group, group, (0, -.09, .22), (.33, .61, .25), m['black'])
    rounded(group + "_SOLE", group, (0, -.07, .015), (.69, 1.24, .2), m['sole'], .14)
    oval(group + "_TOE", group, (0, -.43, .17), (.33, .33, .18), m['black'])
    oval(group + "_HEEL_PANEL", group, (0, .27, .25), (.3, .25, .24), m['black'])
    oval(group + "_TONGUE", group, (0, -.2, .43), (.2, .29, .07), m['sole'])
    for i, y in enumerate((-.45, -.15, .16, .43)):
        for side in (-1, 1):
            rounded(group + "_SOLE_SEG_%s_%s" % (i, side), group,
                    (side * .31, y, .005), (.1, .18, .18), m['sole'], .025)
    for i, (y, z) in enumerate(((-.4, .46), (-.26, .51), (-.12, .53))):
        segment(group + "_LACE_%s" % i, group, (-.18, y, z),
                (.18, y + .04, z), .05, m['lace'])
    from mathutils import Matrix
    rotation = Matrix.Rotation(radians(tilt), 4, 'X')
    transform = Matrix.Translation(Vector(center)) @ rotation
    bpy.context.view_layer.update()
    for obj in bpy.data.collections[group].objects:
        obj.matrix_world = transform @ obj.matrix_world


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 48
    scene.cycles.seed = 0
    # This build produced a black Combined pass with denoising enabled.
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 900
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = str(RENDER)
    scene.world.color = (.22, .22, .22)
    bpy.ops.object.camera_add(location=(8, -14, 8))
    camera = bpy.context.object
    camera.name = "EVIDENCE_CAMERA"
    camera.rotation_euler = (Vector((0, 0, 2.6)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = 6.7
    scene.camera = camera
    for name, loc, power, size in (
        ("KEY", (-4, -7, 9), 500, 5),
        ("FILL", (5, -3, 6), 300, 4),
        ("RIM", (1, 4, 8), 600, 3),
    ):
        bpy.ops.object.light_add(type='AREA', location=loc)
        light = bpy.context.object
        light.name = "EVIDENCE_" + name
        light.data.energy, light.data.size = power, size
        light.rotation_euler = (Vector((0, 0, 2.5)) - light.location).to_track_quat('-Z', 'Y').to_euler()


def render_evidence():
    """Direct Cycles evidence; color management remains environment-dependent."""
    bpy.ops.render.render(write_still=True)


def main():
    if (BLEND.exists() or RENDER.exists()) and '--replace-draft' not in sys.argv:
        raise RuntimeError("Versioned output already exists; refusing overwrite.")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene.unit_settings.system = 'NONE'
    scene['purpose'] = 'T-015 relative visual blockout; not manufacturing'
    for name in MODULES:
        scene.collection.children.link(bpy.data.collections.new(name))
    m = {
        'skin': material("SKIN_LIGHT", (.68, .4, .25)),
        'hair': material("HAIR_WHITE_GRAY", (.74, .75, .77)),
        'cloth': material("DARK_APPAREL", (.023, .027, .033)),
        'black': material("BLACK_SHOE_FRAME", (.012, .014, .018)),
        'sole': material("SEGMENTED_SOLE", (.025, .028, .033)),
        'lace': material("BROAD_LACES", (.09, .095, .1)),
        'lens': material("DARK_LENSES", (.035, .048, .06), .18),
        'base': material("DISCREET_BASE", (.06, .065, .075)),
        'mouth': material("SMILE", (.08, .024, .02)),
        'teeth': material("TEETH", (.83, .8, .73)),
    }
    build_base(m)
    build_torso(m)
    build_head(m)
    build_hair(m)
    build_glasses(m)
    build_arm("L", (-.53, -.21, 3.05), (-.82, .38, 2.58), (-.78, .65, 2.33), m)
    build_arm("R", (.53, -.21, 3.05), (.84, -.54, 2.64), (.79, -1.02, 3.04), m)
    build_shorts(m)
    build_leg("L", (-.3, -.1, 1.95), (-.43, -.72, 1.3), (-.44, -.81, .56), m)
    build_leg("R", (.3, .19, 1.96), (.44, .72, 1.43), (.49, 1.13, 1.39), m)
    build_shoe("L", (-.44, -.85, .32), 0, m)
    build_shoe("R", (.49, 1.15, 1.14), -28, m)
    setup_render()
    bpy.context.preferences.filepaths.save_version = 0
    render_evidence()
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    print("BLOCKOUT_V001_OK", bpy.app.version_string, "modules", len(MODULES))


if __name__ == '__main__':
    main()
