"""The virtual office in Blender: run by make_assets.py as
`blender -b --factory-startup -P scene.py -- <textures> <out> <only> [preview] [guide]`.

Everything is built from code: an open-plan office with two rows of desks and the Goal display on
the back wall. The characters are 2D sprites (make_sprites.py), so each seat holds a stand-in board
instead of a person. One fixed camera renders the base picture (every Role idle), one busy layer
per Role (its desk lit, everything else held out), a seat mask per Role (where the desk stands in
front of the sprite), and layout.json with the screen positions of what the page draws on top.
With `guide` the seats hold placeholder 3D figures instead, for make_sprites.py to paint over.
"""

import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1 :]
TEX, OUT, ONLY = Path(argv[0]), Path(argv[1]), argv[2]
PREVIEW = "preview" in argv[3:]
ROLES = json.loads((TEX / "roles.json").read_text())
W, H = (1280, 700) if PREVIEW else (2560, 1400)

# Where each character sits (x right, y away from the camera): an open-plan office with a back
# row of four desks and a front row of three in its gaps, a walkway between, so every face shows.
BACK_Y, FRONT_Y, GAP = 2.4, 0.0, 2.1
PODS = {
    "game-designer": (-1.5 * GAP, BACK_Y),
    "game-director": (-0.5 * GAP, BACK_Y),
    "technical-director": (0.5 * GAP, BACK_Y),
    "art-director": (1.5 * GAP, BACK_Y),
    "qa": (-GAP, FRONT_Y),
    "gameplay-engineer": (0.0, FRONT_Y),
    "playtester": (GAP, FRONT_Y),
}
CHAR_SCALE = 1.1  # the character, its chair and its desk, against the room
DESK_Z = 0.74
RUG_R, RUG_DY = (
    0.95,
    -0.35,
)  # the round rug under chair and desk; its edge is the state ring
WALL_Y = 4.3
GOAL_W, GOAL_H, GOAL_Z = 2.6, 0.78, 2.65  # the Goal display on the back wall


bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def lin(hex_color):
    h = hex_color.lstrip("#")
    c = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


# --- materials ----------------------------------------------------------------------------------
# Every surface is drawn the same way, like a flat illustration: the light reaching it picks one of
# three tones of its colour (shadow, half-tone, lit), and Freestyle draws the outlines. Glowing
# things (screens, lights, the state rings) are flat colour and get no outline.

SHADE = ("#b4bbe4", "#dde1f5")  # shadow and half-tone multipliers
SKIN_SHADE = ("#ecb4a6", "#f7dad0")
LIGHT_REF = 1.5  # the light on a fully lit surface; tones split at fractions of it
TONES = (0.6, 0.8)
LINE = "#1b2236"

_mats = {}


def new_mat(name, glow=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.remove(m.node_tree.nodes["Principled BSDF"])
    m["glow"] = glow
    return m


def flat(nt, color):
    """Self-lit flat colour (a socket)."""
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(color, em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])


def cel(nt, color, shade=SHADE):
    """Three tones of `color` (a socket), chosen by the light reaching the surface."""
    n = nt.nodes
    diff = n.new("ShaderNodeBsdfDiffuse")
    s2r = n.new("ShaderNodeShaderToRGB")
    nt.links.new(diff.outputs["BSDF"], s2r.inputs["Shader"])
    bw = n.new("ShaderNodeRGBToBW")
    nt.links.new(s2r.outputs["Color"], bw.inputs["Color"])
    level = n.new("ShaderNodeMath")
    level.operation = "MULTIPLY"
    level.inputs[1].default_value = 1 / LIGHT_REF
    nt.links.new(bw.outputs["Val"], level.inputs[0])
    ramp = n.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position, cr.elements[0].color = 0.0, (*lin(shade[0]), 1)
    cr.elements[1].position, cr.elements[1].color = TONES[1], (1, 1, 1, 1)
    half = cr.elements.new(TONES[0])
    half.color = (*lin(shade[1]), 1)
    nt.links.new(level.outputs[0], ramp.inputs["Fac"])
    tone = n.new("ShaderNodeMix")
    tone.data_type, tone.blend_type = "RGBA", "MULTIPLY"
    tone.inputs["Factor"].default_value = 1.0
    nt.links.new(color, tone.inputs["A"])
    nt.links.new(ramp.outputs["Color"], tone.inputs["B"])
    flat(nt, tone.outputs["Result"])


def rgb_node(nt, color):
    node = nt.nodes.new("ShaderNodeRGB")
    node.outputs[0].default_value = (*lin(color), 1)
    return node.outputs[0]


def mat(
    name,
    color,
    rough=0.5,
    metal=0.0,
    emit=None,
    strength=0.0,
    coat=0.0,
    transmission=0.0,
    alpha=1.0,
):
    """A cel material; with emit and strength >= 2 it glows as flat `emit` instead. The other
    arguments are kept from the physically based version and ignored."""
    glow = bool(emit) and strength >= 2
    key = (name, color, emit if glow else None)
    if key in _mats:
        return _mats[key]
    m = new_mat(name, glow)
    if glow:
        flat(m.node_tree, rgb_node(m.node_tree, emit))
    else:
        cel(m.node_tree, rgb_node(m.node_tree, color))
    _mats[key] = m
    return m


def image_mat(name, path, strength=0.0, rough=0.4, repeat=None):
    """A textured material; with strength > 0 the texture glows (screens), brighter when busy."""
    m = new_mat(name, strength > 0)
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(path), check_existing=True)
    if repeat:
        tc, mp = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (*repeat, 1)
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
    if strength:
        dim = nt.nodes.new("ShaderNodeMix")
        dim.data_type, dim.blend_type = "RGBA", "MULTIPLY"
        dim.inputs["Factor"].default_value = 1.0
        k = min(1.0, 0.72 + 0.07 * strength)
        dim.inputs["B"].default_value = (k, k, k, 1)
        nt.links.new(tex.outputs["Color"], dim.inputs["A"])
        flat(nt, dim.outputs["Result"])
    else:
        cel(nt, tex.outputs["Color"])
    return m


def toon_mat(name, color, shadow="#8a90c0"):
    """A character's cel material with its own shadow tint."""
    if name in _mats:
        return _mats[name]
    m = new_mat(name)
    cel(
        m.node_tree,
        rgb_node(m.node_tree, color),
        (shadow, mix_hex(shadow, "#ffffff", 0.55)),
    )
    _mats[name] = m
    return m


def skin_face_mat(role, spec):
    """Skin with the face texture over it, through the head's UV map (see character)."""
    m = new_mat(f"head-{role}")
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(TEX / f"face-{role}.png"), check_existing=True)
    tex.extension = "CLIP"  # (Cubic hangs EEVEE on the software GL renderer)
    mixc = nt.nodes.new("ShaderNodeMix")
    mixc.data_type = "RGBA"
    mixc.inputs["A"].default_value = (*lin(spec["skin"]), 1)
    nt.links.new(tex.outputs["Alpha"], mixc.inputs["Factor"])
    nt.links.new(tex.outputs["Color"], mixc.inputs["B"])
    cel(nt, mixc.outputs["Result"], SKIN_SHADE)
    return m


SKIN_SHADOW = SKIN_SHADE[0]


# --- geometry helpers -----------------------------------------------------------------------------

COLL = {}


def coll(name):
    if name not in COLL:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        COLL[name] = c
    return COLL[name]


CURRENT = ["room"]


def link(obj, *mats):
    coll(CURRENT[0]).objects.link(obj)
    for m in mats:
        obj.data.materials.append(m)
    if any(m.get("glow") for m in mats) and obj.type == "MESH":
        mark = obj.data.attributes.new("freestyle_face", "BOOLEAN", "FACE")
        mark.data.foreach_set("value", [True] * len(obj.data.polygons))
    return obj


def smooth(obj):
    for p in obj.data.polygons:
        p.use_smooth = True
    return obj


def bevel(obj, width=0.015, segments=3):
    mod = obj.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method = width, segments, "ANGLE"
    return obj


def mesh_from_bm(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return bpy.data.objects.new(name, me)


def box(name, size, loc, m, rot=(0, 0, 0), bev=0.015):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    obj = mesh_from_bm(name, bm)
    obj.location, obj.rotation_euler = loc, rot
    link(obj, m)
    if bev:
        bevel(obj, bev)
    return obj


def cyl(name, r, h, loc, m, verts=48, r2=None, rot=(0, 0, 0), bev=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        segments=verts,
        radius1=r,
        radius2=r if r2 is None else r2,
        depth=h,
    )
    obj = mesh_from_bm(name, bm)
    obj.location, obj.rotation_euler = loc, rot
    link(obj, m)
    smooth(obj)
    for p in obj.data.polygons:  # flat caps
        if abs(p.normal.z) > 0.99:
            p.use_smooth = False
    if bev:
        bevel(obj, bev)
    return obj


def sphere(name, r, loc, m, scale=(1, 1, 1), seg=32, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    obj = mesh_from_bm(name, bm)
    obj.location, obj.scale, obj.rotation_euler = loc, scale, rot
    link(obj, m)
    return smooth(obj)


def torus(name, R, r, loc, m, rot=(0, 0, 0), major=64, minor=12, half=False):
    bm = bmesh.new()
    steps = major // 2 if half else major
    rings = []
    for i in range(steps + (1 if half else 0)):
        a = (math.pi if half else 2 * math.pi) * i / steps
        rings.append(
            [
                bm.verts.new(
                    (
                        (R + r * math.cos(b)) * math.cos(a),
                        (R + r * math.cos(b)) * math.sin(a),
                        r * math.sin(b),
                    )
                )
                for b in [2 * math.pi * j / minor for j in range(minor)]
            ]
        )
    for i in range(steps if not half else steps):
        nxt = rings[(i + 1) % len(rings)]
        for j in range(minor):
            bm.faces.new(
                (rings[i][j], nxt[j], nxt[(j + 1) % minor], rings[i][(j + 1) % minor])
            )
    obj = mesh_from_bm(name, bm)
    obj.location, obj.rotation_euler = loc, rot
    link(obj, m)
    return smooth(obj)


def metaball(name, elems, m, res=0.02):
    """Smooth organic shapes (hair, bodies): a metaball converted to a mesh."""
    mb = bpy.data.metaballs.new(name)
    mb.resolution = mb.render_resolution = res
    mb.threshold = 0.6
    for e in elems:
        el = mb.elements.new()
        el.co = e["co"]
        el.radius = e["r"]
        if "size" in e:
            el.type = "ELLIPSOID"
            el.size_x, el.size_y, el.size_z = e["size"]
        if "rot" in e:
            el.rotation = Euler(e["rot"]).to_quaternion()
    tmp = bpy.data.objects.new(name, mb)
    scene.collection.objects.link(tmp)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp)
    bpy.data.metaballs.remove(mb)
    obj = bpy.data.objects.new(name, me)
    link(obj, m)
    calm = obj.modifiers.new("smooth", "SMOOTH")  # even normals give clean tone edges
    calm.factor, calm.iterations = 0.6, 6
    return smooth(obj)


def outline(obj, thickness=0.012):
    return obj  # Freestyle draws every outline


def parent(child, par):
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()


def place(objs, origin, yaw):
    """Move a group of objects built around (0, 0) to origin, turned by yaw (degrees)."""
    bpy.context.view_layer.update()
    m = Matrix.Translation((*origin, 0)[:3]) @ Matrix.Rotation(
        math.radians(yaw), 4, "Z"
    )
    for o in objs:
        o.matrix_world = m @ o.matrix_world


# --- characters ---------------------------------------------------------------------------------

HEAD_R = 0.30
HEAD_Z = 1.26
HEAD_SCALE = 0.84


def hair_elems(style):
    """Hair as a few large, overlapping metaball shapes so it reads as one smooth mass."""
    R = HEAD_R
    cap = [dict(co=(0, 0.075, 0.075), r=R * 1.62, size=(1.08, 1.0, 1.0))]
    fringe = [dict(co=(0, -0.17, 0.2), r=0.34, size=(1.0, 0.5, 0.5))]
    strands = [
        dict(
            co=(x, -0.235, 0.11),
            r=0.15,
            size=(0.55, 0.4, 0.85),
            rot=(0.35, 0, -x * 1.5),
        )
        for x in (-0.13, 0.0, 0.13)
    ]
    sides = [
        dict(co=(sx * 0.255, 0.01, -0.02), r=0.2, size=(0.5, 0.95, 1.2))
        for sx in (-1, 1)
    ]
    if style == "neat":  # side-parted
        return (
            cap
            + [
                dict(
                    co=(0.06, -0.16, 0.21),
                    r=0.34,
                    size=(1.05, 0.5, 0.5),
                    rot=(0, 0.25, 0),
                )
            ]
            + sides
        )
    if style == "fluffy":
        volume = [
            dict(co=(sx * 0.24, 0.06, -0.12), r=0.24, size=(0.65, 0.9, 1.0))
            for sx in (-1, 1)
        ]
        return (
            cap
            + fringe
            + strands
            + sides
            + volume
            + [dict(co=(0, 0.2, -0.06), r=0.4, size=(1.1, 0.7, 1.0))]
        )
    if style == "spiky":
        spikes = [
            dict(
                co=(math.sin(a) * 0.17, 0.04 + math.cos(a) * 0.12, 0.27),
                r=0.2,
                size=(0.42, 0.42, 1.25),
                rot=(math.cos(a) * -0.7, math.sin(a) * 0.7, 0),
            )
            for a in (-1.7, -0.85, 0, 0.85, 1.7, 2.6, -2.6)
        ]
        front = [
            dict(
                co=(x, -0.215, 0.15),
                r=0.16,
                size=(0.45, 0.42, 1.05),
                rot=(0.6, 0, -x * 2.0),
            )
            for x in (-0.12, 0.0, 0.12)
        ]
        return cap + fringe + spikes + front + sides
    if style == "long":
        back = [dict(co=(0, 0.15, -0.3), r=0.46, size=(1.0, 0.55, 1.4))]
        long_sides = [
            dict(co=(sx * 0.245, -0.02, -0.3), r=0.22, size=(0.45, 0.6, 1.8))
            for sx in (-1, 1)
        ]
        return cap + fringe + strands + sides + back + long_sides
    if style == "messy":
        tufts = [
            dict(
                co=(math.sin(a) * 0.18, 0.06 + math.cos(a) * 0.15, 0.24),
                r=0.2,
                size=(0.6, 0.6, 0.85),
                rot=(math.cos(a) * -0.5, math.sin(a) * 0.5, a),
            )
            for a in [i * 1.05 for i in range(6)]
        ]
        front = [
            dict(
                co=(x, -0.22, 0.13),
                r=0.16,
                size=(0.5, 0.42, 0.95),
                rot=(0.45, 0, -x * 1.8 + 0.25),
            )
            for x in (-0.13, 0.0, 0.13)
        ]
        return cap + fringe + tufts + front + sides
    if style == "short":
        return (
            cap
            + [
                dict(
                    co=(0.02, -0.17, 0.21),
                    r=0.32,
                    size=(1.0, 0.48, 0.45),
                    rot=(0, 0.15, 0),
                )
            ]
            + sides
        )
    if style == "cap":
        small = [dict(co=(0, 0.07, 0.0), r=R * 1.38, size=(1.08, 1.0, 0.9))]
        return (
            small
            + [
                dict(co=(x, -0.22, 0.08), r=0.13, size=(0.6, 0.45, 0.9))
                for x in (-0.13, 0.0, 0.13)
            ]
            + sides
        )
    return cap + fringe + strands + sides


def character(role, spec, pose):
    """A seated chibi character at the origin facing -y; returns its objects."""
    R = HEAD_R
    objs = []
    shirt = toon_mat(f"shirt-{role}", spec["shirt"])
    inner = toon_mat(f"inner-{role}", spec["inner"])
    pants = toon_mat("pants", "#2b3142")
    skin = toon_mat(f"skin-{role}", spec["skin"], SKIN_SHADOW)
    busy = pose == "busy"
    # body: hips, torso and sleeves blend into one shape
    torso = [
        dict(co=(0, 0.04, 0.6), r=0.26, size=(1.1, 0.95, 0.75)),
        dict(co=(0, 0.02, 0.82), r=0.28, size=(1.0, 0.78, 1.05)),
    ]
    sh = [(sx * 0.2, 0.0, 0.94) for sx in (-1, 1)]
    if busy:
        elbows, hands = [(sx * 0.26, -0.26, 0.77) for sx in (-1, 1)], [
            (sx * 0.13, -0.56, 0.79) for sx in (-1, 1)
        ]
    else:
        elbows, hands = [(sx * 0.27, -0.06, 0.68) for sx in (-1, 1)], [
            (sx * 0.15, -0.28, 0.6) for sx in (-1, 1)
        ]
    sleeves = []
    for s, e, h in zip(sh, elbows, hands):
        for t in (0.0, 0.33, 0.66, 1.0):
            sleeves.append(
                dict(co=tuple(a + (b - a) * t for a, b in zip(s, e)), r=0.12)
            )
        for t in (0.33, 0.66, 0.9):
            sleeves.append(
                dict(co=tuple(a + (b - a) * t for a, b in zip(e, h)), r=0.105)
            )
    body = metaball(f"mbBody{role}", torso + sleeves, shirt, res=0.018)
    objs.append(outline(body, 0.01))
    outfit = spec["outfit"]
    if outfit in ("blazer", "cardigan"):  # open front over the shirt, with lapels
        objs.append(
            box(
                f"shirtfront-{role}",
                (0.13, 0.02, 0.2),
                (0, -0.2, 0.86),
                inner,
                rot=(0.1, 0, 0),
                bev=0.01,
            )
        )
        for sx in (-1, 1):
            objs.append(
                box(
                    f"lapel{sx}-{role}",
                    (0.05, 0.025, 0.24),
                    (sx * 0.08, -0.205, 0.86),
                    shirt,
                    rot=(0.1, sx * 0.3, 0),
                    bev=0.008,
                )
            )
        if outfit == "cardigan":
            for k in range(3):
                objs.append(
                    sphere(
                        f"button{k}-{role}",
                        0.014,
                        (0.045, -0.235, 0.7 + k * 0.07),
                        toon_mat("button", "#6b4a2e"),
                        seg=12,
                    )
                )
    if outfit == "hoodie":  # a hood bunched behind the neck and two drawstrings
        objs.append(
            outline(
                torus(
                    f"hood-{role}",
                    0.15,
                    0.07,
                    (0, 0.07, 1.0),
                    shirt,
                    rot=(0.45, 0, 0),
                    minor=12,
                ),
                0.008,
            )
        )
        for sx in (-1, 1):
            objs.append(
                cyl(
                    f"string{sx}-{role}",
                    0.009,
                    0.16,
                    (sx * 0.05, -0.215, 0.86),
                    inner,
                    verts=8,
                    rot=(0.1, 0, 0),
                )
            )
    if outfit in ("sweater", "tee", "blouse"):  # a collar in the inner colour
        objs.append(
            torus(
                f"collar-{role}",
                0.105,
                0.032 if outfit == "blouse" else 0.022,
                (0, -0.01, 1.0),
                inner,
                rot=(0.2, 0, 0),
                minor=10,
            )
        )
    if spec["acc"] == "tie":
        objs.append(
            box(
                f"tie-{role}",
                (0.045, 0.02, 0.17),
                (0, -0.215, 0.84),
                toon_mat("tie", "#c0392b"),
                rot=(0.1, 0, 0),
                bev=0.008,
            )
        )
    if spec["acc"] == "scarf":
        objs.append(
            outline(
                torus(
                    f"scarf-{role}",
                    0.15,
                    0.05,
                    (0, -0.01, 1.0),
                    toon_mat("scarf", spec["accent"]),
                    minor=10,
                ),
                0.008,
            )
        )
    legs = []
    for sx in (-1, 1):
        for t in (0.0, 0.5, 1.0):
            legs.append(dict(co=(sx * 0.11, 0.05 - 0.4 * t, 0.53), r=0.13))
        for t in (0.3, 0.7, 1.0):
            legs.append(dict(co=(sx * 0.12, -0.36, 0.53 - 0.42 * t), r=0.105))
    objs.append(outline(metaball(f"mbLegs{role}", legs, pants), 0.01))
    for sx in (-1, 1):
        objs.append(
            sphere(
                f"shoe{sx}-{role}",
                0.075,
                (sx * 0.12, -0.42, 0.08),
                toon_mat("shoe", "#3a3f4f"),
                scale=(1, 1.5, 0.7),
            )
        )
    for h in hands:
        objs.append(
            outline(
                sphere(f"hand-{role}", 0.058, h, skin, scale=(0.9, 1.3, 0.7)), 0.008
            )
        )
    objs.append(cyl(f"neck-{role}", 0.07, 0.14, (0, 0, 1.0), skin))
    # head with face, ears and hair, as children of a pivot so the head can tilt
    pivot = bpy.data.objects.new(f"headpivot-{role}", None)
    link(pivot)
    pivot.location = (0, -0.05 if busy else 0.05, HEAD_Z - (0.02 if busy else 0) - 0.03)
    pivot.scale = (HEAD_SCALE,) * 3
    turn = 14 if (sum(map(ord, role)) % 2) else -14
    pivot.rotation_euler = (
        math.radians(16 if busy else -18),  # at work the head bows over the laptop
        math.radians(0 if busy else turn * 0.4),
        math.radians(0 if busy else turn),
    )
    head = sphere(
        f"head-{role}",
        R,
        (0, 0, 0),
        skin_face_mat(role, spec),
        scale=(1, 0.96, 0.95),
        seg=48,
    )
    # the face texture is projected straight onto the front half; the back maps outside it
    uv = head.data.uv_layers.new().data
    for li, loop in enumerate(head.data.loops):
        co = head.data.vertices[loop.vertex_index].co
        front = co.y < 0.02
        uv[li].uv = (co.x / (2 * R) + 0.5 + (0 if front else 4), co.z / (2 * R) + 0.5)
    hair = metaball(
        f"mbHair{role}",
        hair_elems(spec["style"]),
        toon_mat(f"hair-{role}", spec["hair"], "#6c6a96"),
        res=0.014,
    )
    outline(hair, 0.012)
    parts = [head, hair]
    for sx in (-1, 1):
        parts.append(
            outline(
                sphere(
                    f"ear{sx}-{role}",
                    0.06,
                    (sx * R * 0.95, 0.02, -0.03),
                    skin,
                    scale=(0.6, 1, 1.1),
                ),
                0.008,
            )
        )
    acc = spec["acc"]
    if acc == "glasses":
        frame = mat("frame", "#1f2430", 0.3, 0.6)
        for sx in (-1, 1):
            parts.append(
                torus(
                    f"lens{sx}-{role}",
                    0.075,
                    0.009,
                    (sx * 0.11, -0.305, -0.03),
                    frame,
                    rot=(math.pi / 2, 0, 0),
                    minor=8,
                )
            )
        parts.append(
            box(
                f"bridge-{role}",
                (0.06, 0.012, 0.012),
                (0, -0.31, -0.02),
                frame,
                bev=0.0,
            )
        )
    if acc == "headphones":
        dark = toon_mat("hp", "#2a2f3d")
        parts.append(
            torus(
                f"band-{role}",
                R * 1.1,
                0.022,
                (0, 0, 0),
                dark,
                rot=(math.pi / 2, 0, 0),
                half=True,
                minor=10,
            )
        )
        for sx in (-1, 1):
            parts.append(
                cyl(
                    f"cup{sx}-{role}",
                    0.085,
                    0.07,
                    (sx * R * 1.08, 0, -0.02),
                    dark,
                    rot=(0, math.pi / 2, 0),
                )
            )
            parts.append(
                torus(
                    f"cupring{sx}-{role}",
                    0.07,
                    0.012,
                    (sx * R * 1.12, 0, -0.02),
                    mat("hpglow", "#38bdf8", 0.3, emit="#38bdf8", strength=4),
                    rot=(0, math.pi / 2, 0),
                    minor=8,
                )
            )
    if acc == "beret":
        parts.append(
            outline(
                sphere(
                    f"beret-{role}",
                    0.21,
                    (-0.07, 0.02, 0.36),
                    toon_mat("beret", "#2a2733"),
                    scale=(1.0, 1.0, 0.32),
                    rot=(0.25, -0.3, 0),
                ),
                0.01,
            )
        )
        parts.append(
            cyl(
                f"beretstem-{role}",
                0.018,
                0.05,
                (-0.09, 0.03, 0.44),
                toon_mat("beret", "#2a2733"),
            )
        )
    if acc == "cap":  # a snug cap worn backwards: the strap shows at the front
        capm = toon_mat("cap", "#2b303c")
        c = sphere(f"cap-{role}", R * 1.06, (0, 0.03, 0.1), capm, scale=(1, 1.03, 0.8))
        bm = bmesh.new()
        bm.from_mesh(c.data)
        bmesh.ops.delete(
            bm, geom=[v for v in bm.verts if v.co.z < 0.0], context="VERTS"
        )
        bm.to_mesh(c.data)
        bm.free()
        parts.append(outline(c, 0.01))
        parts.append(
            outline(
                cyl(
                    f"visor-{role}",
                    0.17,
                    0.022,
                    (0, -0.31, 0.16),
                    capm,
                    rot=(-0.35, 0, 0),
                ),
                0.008,
            )
        )
        parts[-1].scale = (1, 0.7, 1)
        parts.append(
            sphere(
                f"capbutton-{role}",
                0.03,
                (0, 0.03, 0.35),
                toon_mat("capbutton", "#a3e635"),
                seg=12,
            )
        )
        parts.append(
            box(
                f"cappatch-{role}",
                (0.11, 0.02, 0.07),
                (0, -0.275, 0.25),
                toon_mat("capbutton", "#a3e635"),
                rot=(-0.6, 0, 0),
                bev=0.01,
            )
        )
    for p in parts:
        p.parent = pivot
    objs += parts + [pivot]
    for (
        o
    ) in (
        objs
    ):  # self-shadowing on small round shapes shows up as stripes in the flat tones
        o.visible_shadow = False
    return objs


# --- props ----------------------------------------------------------------------------------------


def monitor(name, w, h, loc, yaw, screen_path, glow, tilt=0.0, stand=True):
    bezel = mat("bezel", "#0c0f16", 0.25, 0.4, coat=0.5)
    objs = [
        box(f"{name}-bezel", (w + 0.03, 0.03, h + 0.03), (0, 0, 0), bezel, bev=0.008)
    ]
    plane = bpy.data.meshes.new(f"{name}-screen")
    hw, hh = w / 2, h / 2
    plane.from_pydata(
        [(-hw, 0, -hh), (hw, 0, -hh), (hw, 0, hh), (-hw, 0, hh)], [], [(0, 1, 2, 3)]
    )
    plane.uv_layers.new().data.foreach_set("uv", [0, 0, 1, 0, 1, 1, 0, 1])
    scr = bpy.data.objects.new(f"{name}-screen", plane)
    scr.location = (0, -0.017, 0)
    link(scr, image_mat(f"{name}-screen", screen_path, glow, rough=0.2))
    objs.append(scr)
    if stand:
        objs.append(
            box(
                f"{name}-neck",
                (0.04, 0.03, h / 2 + 0.06),
                (0, 0.03, -h / 2 - 0.02),
                bezel,
                bev=0.005,
            )
        )
        objs.append(
            box(
                f"{name}-foot",
                (0.2, 0.14, 0.015),
                (0, 0.03, -h / 2 - 0.09),
                bezel,
                bev=0.005,
            )
        )
    pivot = bpy.data.objects.new(f"{name}-pivot", None)
    link(pivot)
    for o in objs:
        parent(o, pivot)
    pivot.location, pivot.rotation_euler = loc, (
        math.radians(tilt),
        0,
        math.radians(yaw),
    )
    return objs + [pivot]


def plant(name, loc, s=1.0, pot="#e8ebf0"):
    seed = sum(map(ord, name))
    spin, n, wide = (seed % 37) * 0.17, 11 + seed % 6, 0.28 + (seed % 5) * 0.04
    objs = [
        cyl(
            f"{name}-pot",
            0.14 * s,
            0.26 * s,
            (loc[0], loc[1], loc[2] + 0.13 * s),
            mat("pot", pot, 0.5),
            r2=0.11 * s,
            bev=0.01,
        )
    ]
    objs.append(
        cyl(
            f"{name}-soil",
            0.13 * s,
            0.02 * s,
            (loc[0], loc[1], loc[2] + 0.25 * s),
            mat("soil", "#3b2a20", 0.9),
        )
    )
    greens = [
        mat("leaf1", "#2f9e4f", 0.5, coat=0.2),
        mat("leaf2", "#46c26a", 0.5, coat=0.2),
        mat("leaf3", "#1f7a3c", 0.5, coat=0.2),
    ]
    for i in range(n):
        a = i * 2.4 + spin
        lean = 0.35 + 0.5 * ((i * 7) % 5) / 5
        length = (0.22 + 0.12 * ((i * 3) % 4) / 4) * s
        cx = loc[0] + math.cos(a) * math.sin(lean) * length * 0.55
        cy = loc[1] + math.sin(a) * math.sin(lean) * length * 0.55
        cz = loc[2] + 0.26 * s + math.cos(lean) * length * 0.55
        leaf = sphere(
            f"{name}-leaf{i}",
            length / 2,
            (cx, cy, cz),
            greens[(i + seed) % 3],
            scale=(wide, 1, 0.07),
            seg=16,
        )
        leaf.rotation_euler = (math.pi / 2 - lean, 0, a - math.pi / 2)
        objs.append(leaf)
    return objs


WOOD = ("wood", "#a77b55", 0.42)
DESK_BODY = ("deskbody", "#394154", 0.5)


def mug_at(name, loc, color):
    m = mat(f"mug-{color}", color, 0.35, coat=0.5)
    return [
        cyl(name, 0.045, 0.1, (loc[0], loc[1], loc[2] + 0.05), m, bev=0.004),
        torus(
            f"{name}-h",
            0.03,
            0.009,
            (loc[0] - 0.05, loc[1], loc[2] + 0.05),
            m,
            rot=(math.pi / 2, 0, 0),
            minor=6,
        ),
    ]


def book_stack(name, loc, yaw, colors):
    return [
        box(
            f"{name}{i}",
            (0.22, 0.3, 0.04),
            (loc[0], loc[1], loc[2] + 0.02 + i * 0.042),
            mat(f"book-{col}", col, 0.7),
            rot=(0, 0, math.radians(yaw + i * 9 - 8)),
            bev=0.004,
        )
        for i, col in enumerate(colors)
    ]


def poster(name, path, loc, yaw, w, h, glow=0.0, frame="#2a3142"):
    face = box(
        name,
        (w, 0.012, h),
        loc,
        image_mat(f"{name}-img", path, glow, 0.6),
        rot=(0, 0, math.radians(yaw)),
        bev=0,
    )
    cork_uv(face)
    fr = box(
        f"{name}-frame",
        (w + 0.04, 0.01, h + 0.04),
        (loc[0], loc[1], loc[2]),
        mat("frame-" + frame, frame, 0.4),
        rot=(0, 0, math.radians(yaw)),
        bev=0.004,
    )
    return [face, fr]


def chair(role, color, kind):
    seat = mat("chairfab", "#2a3040", 0.8)
    acc = mat(f"chairacc-{role}", color, 0.5)
    metalm = mat("chairmetal", "#9aa3b5", 0.3, 0.8)
    back_h, back_w = (0.66, 0.62) if kind in ("exec", "gaming") else (0.6, 0.56)
    if kind == "exec":
        seat = acc = mat("leather", "#5a3324", 0.35, coat=0.3)
    if kind == "gaming":
        seat = mat("gamingblack", "#1c1f29", 0.5)
    objs = [box(f"seat-{role}", (0.56, 0.52, 0.1), (0, 0.05, 0.44), seat, bev=0.04)]
    objs.append(
        box(
            f"back-{role}",
            (back_w, 0.12, back_h),
            (0, 0.33, 0.5 + back_h / 2),
            seat,
            rot=(math.radians(-10), 0, 0),
            bev=0.05,
        )
    )
    if kind == "gaming":  # dark side bolsters
        for sx in (-1, 1):
            objs.append(
                box(
                    f"wing{sx}-{role}",
                    (0.1, 0.14, back_h * 0.9),
                    (sx * 0.3, 0.3, 0.5 + back_h / 2),
                    seat,
                    rot=(math.radians(-10), 0, sx * 0.25),
                    bev=0.04,
                )
            )
    else:
        objs.append(
            box(
                f"backstripe-{role}",
                (0.1, 0.13, back_h * 0.9),
                (0, 0.33, 0.5 + back_h / 2),
                acc,
                rot=(math.radians(-10), 0, 0),
                bev=0.02,
            )
        )
    objs.append(cyl(f"gas-{role}", 0.03, 0.34, (0, 0.05, 0.22), metalm))
    for i in range(5):
        a = i * 2 * math.pi / 5
        objs.append(
            box(
                f"leg{i}-{role}",
                (0.05, 0.3, 0.04),
                (math.sin(a) * 0.15, 0.05 + math.cos(a) * 0.15, 0.06),
                metalm,
                rot=(0, 0, -a),
                bev=0.01,
            )
        )
    return objs


def mix_hex(a, b, t):
    ca = [int(a.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def cork_uv(obj, axes="xz"):
    """UVs for a flat box so one face shows the whole texture: the front (xz) or the top (xy)."""
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new()
    uv = me.uv_layers.active.data
    i, j = "xyz".index(axes[0]), "xyz".index(axes[1])
    lo = [min(v.co[k] for v in me.vertices) for k in range(3)]
    hi = [max(v.co[k] for v in me.vertices) for k in range(3)]
    for li, loop in enumerate(me.loops):
        v = me.vertices[loop.vertex_index].co
        uv[li].uv = (
            (v[i] - lo[i]) / ((hi[i] - lo[i]) or 1),
            (v[j] - lo[j]) / ((hi[j] - lo[j]) or 1),
        )


# --- room -------------------------------------------------------------------------------------------


def floor_mat():
    m = new_mat("floor")
    nt = m.node_tree
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.0
    brick.inputs["Color1"].default_value = (*lin("#22304f"), 1)
    brick.inputs["Color2"].default_value = (*lin("#253455"), 1)
    brick.inputs["Mortar"].default_value = (*lin("#33477a"), 1)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Brick Width"].default_value = 1.2
    brick.inputs["Row Height"].default_value = 1.2
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], brick.inputs["Vector"])
    cel(nt, brick.outputs["Color"])
    return m


def front_desk(role, spec, screens_glow):
    """The desk in front of a seated character at the origin (facing -y): a laptop whose lid hides
    the typing hands, a second monitor at the side, a mug, and a light strip in the Role's colour
    along the front edge (bright at work). Scaled with the character."""
    color = spec["color"]
    busy = screens_glow > 2
    wood, body = mat(*WOOD, coat=0.2), mat(*DESK_BODY)
    objs = [
        box(
            f"desk-top-{role}", (1.24, 0.72, 0.04), (0, -0.61, DESK_Z), wood, bev=0.008
        ),
        box(
            f"desk-front-{role}",
            (1.2, 0.03, DESK_Z - 0.06),
            (0, -0.95, (DESK_Z - 0.04) / 2),
            body,
            bev=0.006,
        ),
        box(
            f"desk-led-{role}",
            (1.1, 0.01, 0.025),
            (0, -0.968, DESK_Z - 0.09),
            mat(f"led-{role}", color, emit=color, strength=7 if busy else 1),
            bev=0,
        ),
    ]
    for sx in (-1, 1):
        objs.append(
            box(
                f"desk-leg{sx}-{role}",
                (0.04, 0.66, DESK_Z - 0.04),
                (sx * 0.58, -0.61, (DESK_Z - 0.04) / 2),
                body,
                bev=0.006,
            )
        )
    # the laptop: keyboard toward the character, the lid's back (with a logo) toward the camera
    shell = mat("laptop", "#3a4152", 0.35)
    objs.append(
        box(f"laptop-{role}", (0.44, 0.28, 0.02), (0, -0.58, DESK_Z + 0.03), shell)
    )
    lid = box(
        f"lid-{role}",
        (0.44, 0.015, 0.3),
        (0, -0.74, DESK_Z + 0.17),
        shell,
        rot=(math.radians(-12), 0, 0),
        bev=0.006,
    )
    objs.append(lid)
    objs.append(
        cyl(
            f"logo-{role}",
            0.035,
            0.004,
            (0, -0.752, DESK_Z + 0.19),
            mat(f"logo-{role}", color, emit=color, strength=3 if busy else 1),
            verts=24,
            rot=(math.radians(78), 0, 0),
        )
    )
    objs += monitor(
        f"mon-{role}",
        0.5,
        0.31,
        (-0.42, -0.72, DESK_Z + 0.29),
        150,
        TEX / f"screen-{role}-0.png",
        screens_glow,
        tilt=-4,
    )
    objs += mug_at(f"mug-{role}", (0.42, -0.5, DESK_Z + 0.02), color)
    return objs


def station(role, spec, glow):
    """The workstation around a seated character at the origin facing the camera (-y): a round rug
    whose edge is the state ring, low screens beside the desk, and the Role's own things.
    """
    color = spec["color"]
    busy = glow > 2
    s = CHAR_SCALE  # the desk is scaled with the character; the screens follow its edges
    objs = [
        cyl(
            f"rug-{role}",
            RUG_R,
            0.012,
            (0, RUG_DY, 0.006),
            mat("rug", "#3c4762", 0.95),
            verts=96,
        ),
        torus(
            f"ring-{role}",
            RUG_R,
            0.028,
            (0, RUG_DY, 0.02),
            # bright at work; idle only a faint line in the rug, not a stage ring
            mat(
                f"ring-{role}",
                color if busy else mix_hex(color, "#3c4762", 0.7),
                emit=color,
                strength=16 if busy else 0.5,
            ),
            major=128,
            minor=8,
        ),
    ]
    panel = mat("deskscreen", "#7e889e", 0.9)
    for sx in (-1, 1):
        x = sx * (0.62 * s + 0.04)
        objs.append(
            box(
                f"screen{sx}-{role}",
                (0.04, 0.74 * s, 1.18),
                (x, -0.61 * s, 0.59),
                panel,
            )
        )
        objs.append(
            box(
                f"screencap{sx}-{role}",
                (0.05, 0.74 * s, 0.035),
                (x, -0.61 * s, 1.19),
                mat(f"cap-{role}", color, emit=color, strength=2.5),
                bev=0.004,
            )
        )
    objs += station_props(role, spec, glow)
    return objs


def station_props(role, spec, glow):
    """What makes each workstation the Role's own: on the desk's right corner (placed in desk
    coordinates, scaled with it), on the floor to the right of the chair, and on the wall behind
    the back row."""
    c = spec["color"]
    s = CHAR_SCALE
    objs = []
    dz = DESK_Z * s + 0.02  # the desk top
    corner = (0.42 * s, -0.78 * s)  # desk top, right front corner
    floor = (1.04, 0.15)  # the gap to the right of the chair
    lit = 1.2 if glow > 2 else 0.5
    back = PODS[role][1] > 1
    if back:  # a board on the wall behind, with the Role's work on it
        objs += poster(
            f"wallboard-{role}",
            TEX / f"screen-{role}-1.png",
            (0, WALL_Y - PODS[role][1] - 0.04, 1.95),
            0,
            0.9,
            0.56,
            0.9 if glow > 2 else 0.5,
        )
    gold = mat("gold", "#f5b942", 0.25, 1.0)
    if role == "game-director":
        objs.append(
            cyl(
                "trophy",
                0.045,
                0.13,
                (corner[0], corner[1], dz + 0.065),
                gold,
                r2=0.022,
            )
        )
        objs.append(
            sphere(
                "trophycup",
                0.055,
                (corner[0], corner[1], dz + 0.16),
                gold,
                scale=(1, 1, 0.8),
            )
        )
        objs += plant("dir-plant", (*floor, 0), 1.25)
    if role == "game-designer":
        for i, col in enumerate(("#fde047", "#f9a8d4", "#86efac")):
            objs.append(
                box(
                    f"sketch{i}",
                    (0.16, 0.22, 0.008),
                    (corner[0] - 0.04 + i * 0.04, corner[1] + 0.06, dz + i * 0.006),
                    mat(f"paper{i}", col, 0.8),
                    rot=(0, 0, 0.3 * i - 0.2),
                    bev=0,
                )
            )
        objs.append(
            box(
                "planboard",
                (0.6, 0.04, 0.9),
                (floor[0], floor[1] + 0.15, 1.05),
                image_mat("planboard", TEX / "board.png", 0.0, 0.8),
                bev=0,
            )
        )
        cork_uv(objs[-1])
        objs.append(
            box(
                "planboard-leg",
                (0.05, 0.05, 0.6),
                (floor[0], floor[1] + 0.17, 0.3),
                mat("post", "#3a4358", 0.4),
            )
        )
    if role == "technical-director":
        rack = mat("rack", "#1c2232", 0.35, 0.4)
        objs.append(
            box("rack", (0.4, 0.4, 1.0), (floor[0], floor[1], 0.5), rack, bev=0.02)
        )
        for i in range(5):
            on = "#818cf8" if i % 2 else "#34d399"
            objs.append(
                box(
                    f"rackled{i}",
                    (0.3, 0.01, 0.03),
                    (floor[0], floor[1] - 0.205, 0.2 + i * 0.16),
                    mat(f"rackled{i % 2}", on, emit=on, strength=5),
                    bev=0,
                )
            )
        objs += book_stack(
            "td-books", (corner[0], corner[1] + 0.05, dz), 10, ("#3b82f6", "#818cf8")
        )
    if role == "art-director":
        objs.append(
            box(
                "easel-board",
                (0.56, 0.03, 0.46),
                (floor[0], floor[1] + 0.1, 1.15),
                image_mat("easel", TEX / f"screen-{role}-0.png", 0.6, 0.6),
                rot=(math.radians(-10), 0, 0),
                bev=0,
            )
        )
        cork_uv(objs[-1])
        for k, sx in enumerate((-1, 1)):
            objs.append(
                box(
                    f"easel-leg{k}",
                    (0.04, 0.04, 1.2),
                    (floor[0] + sx * 0.18, floor[1] + 0.12, 0.6),
                    mat("easelwood", "#a0784f", 0.6),
                    rot=(math.radians(-6), sx * 0.12, 0),
                    bev=0.01,
                )
            )
        for k, col in enumerate(("#f472b6", "#a78bfa", "#38bdf8")):
            objs.append(
                cyl(
                    f"paint{k}",
                    0.03,
                    0.06,
                    (corner[0] - 0.06 + k * 0.06, corner[1] + 0.04, dz + 0.03),
                    mat(f"paint-{col}", col, 0.3),
                )
            )
    if role == "gameplay-engineer":
        can = mat("can", "#22c55e", 0.25, 0.8)
        for k in range(2):
            objs.append(
                cyl(
                    f"can{k}",
                    0.03,
                    0.1,
                    (corner[0] - k * 0.07, corner[1] + 0.05, dz + 0.05),
                    can,
                )
            )
        objs.append(
            box(
                "tower",
                (0.22, 0.42, 0.46),
                (floor[0], floor[1], 0.23),
                mat("tower", "#151925", 0.3, 0.4),
                bev=0.015,
            )
        )
        objs.append(
            box(
                "tower-rgb",
                (0.2, 0.012, 0.36),
                (floor[0], floor[1] - 0.215, 0.23),
                mat("rgb", "#38bdf8", emit="#a855f7", strength=4),
                bev=0,
            )
        )
        objs.append(
            sphere(
                "duck",
                0.04,
                (corner[0] - 0.16, corner[1] + 0.04, dz + 0.04),
                mat("duck", "#facc15", 0.4),
                scale=(1.2, 1, 0.9),
            )
        )
    if role == "qa":
        objs.append(
            box(
                "clipboard",
                (0.18, 0.25, 0.012),
                (corner[0] - 0.04, corner[1] + 0.08, dz),
                mat("clip", "#e2e8f0", 0.6),
                rot=(0, 0, -0.3),
                bev=0.004,
            )
        )
        objs.append(
            box(
                "devstand",
                (0.4, 0.34, 0.7),
                (floor[0], floor[1], 0.35),
                mat(*DESK_BODY),
                bev=0.012,
            )
        )
        for k in range(3):
            dx = floor[0] - 0.12 + k * 0.12
            objs.append(
                box(
                    f"device{k}",
                    (0.08 + 0.03 * (k == 1), 0.012, 0.15 + 0.04 * (k == 1)),
                    (dx, floor[1], 0.8),
                    mat("device", "#111827", 0.3),
                    rot=(math.radians(-15), 0, 0),
                    bev=0.006,
                )
            )
            objs.append(
                box(
                    f"devscreen{k}",
                    (0.065 + 0.03 * (k == 1), 0.004, 0.13 + 0.04 * (k == 1)),
                    (dx, floor[1] - 0.008, 0.8),
                    mat(
                        f"devscreen{k}",
                        "#38bdf8",
                        emit=("#22c55e", "#38bdf8", "#f87171")[k],
                        strength=2.5 * lit,
                    ),
                    rot=(math.radians(-15), 0, 0),
                    bev=0,
                )
            )
    if role == "playtester":
        pad = mat("pad", "#2d3346", 0.4)
        objs.append(
            box(
                "controller",
                (0.18, 0.11, 0.035),
                (corner[0] - 0.05, corner[1] + 0.06, dz + 0.02),
                pad,
                bev=0.015,
            )
        )
        objs.append(
            metaball(
                "beanbag",
                [
                    dict(
                        co=(floor[0] + 0.1, floor[1], 0.3), r=0.32, size=(1.0, 1.0, 0.6)
                    ),
                    dict(
                        co=(floor[0] + 0.06, floor[1] + 0.08, 0.44),
                        r=0.24,
                        size=(1.0, 0.7, 0.8),
                    ),
                ],
                toon_mat("beanbag", "#65a30d", "#6f8a4a"),
            )
        )
        objs.append(
            box(
                "console-box",
                (0.28, 0.22, 0.07),
                (floor[0] + 0.05, floor[1] - 0.3, 0.035),
                mat("consolebox", "#f1f5f9", 0.3),
                bev=0.015,
            )
        )
        objs.append(
            box(
                "console-led",
                (0.16, 0.01, 0.012),
                (floor[0] + 0.05, floor[1] - 0.415, 0.035),
                mat("consoleled", c, emit=c, strength=5),
                bev=0,
            )
        )
    return objs + desk_extras(role, glow)


def desk_extras(role, glow):
    """Two more things of the Role's own, low and in front of the laptop and the side monitor, so
    each desk reads as its owner's at a glance without covering the face."""
    s = CHAR_SCALE
    dz = DESK_Z * s + 0.02
    lx, ly = -0.36 * s, -0.94 * s  # front left, before the side monitor's foot
    rx, ry = 0.17 * s, -0.95 * s  # front, before the laptop's right half
    lit = 4 if glow > 2 else 2.2
    gold = mat("gold", "#f5b942", 0.25, 1.0)
    objs = []
    if role == "game-director":  # a gold name block and a leather folder of plans
        objs.append(
            box(
                "dir-name",
                (0.26, 0.06, 0.07),
                (lx, ly, dz + 0.035),
                mat("dirname", "#2b3a63", 0.4),
                rot=(0, 0, 0.12),
                bev=0.01,
            )
        )
        objs.append(
            box(
                "dir-nameplate",
                (0.2, 0.004, 0.04),
                (lx - 0.004, ly - 0.032, dz + 0.04),
                gold,
                rot=(0, 0, 0.12),
                bev=0,
            )
        )
        objs.append(
            box(
                "dir-folder",
                (0.26, 0.19, 0.025),
                (rx, ry + 0.02, dz + 0.012),
                mat("folder", "#5b3a26", 0.6),
                rot=(0, 0, -0.18),
                bev=0.008,
            )
        )
        objs.append(
            box(
                "dir-folder-band",
                (0.04, 0.195, 0.03),
                (rx + 0.06, ry + 0.03, dz + 0.012),
                gold,
                rot=(0, 0, -0.18),
                bev=0,
            )
        )
    if role == "game-designer":  # a twenty-sided die and an open sketchbook
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.085)
        die = mesh_from_bm("d20", bm)
        die.location, die.rotation_euler = (lx + 0.04, ly, dz + 0.06), (0.4, 0.2, 0.5)
        link(die, mat("d20", "#34d399", 0.4))
        objs.append(die)
        for k, sx in enumerate((-1, 1)):
            objs.append(
                box(
                    f"sketchpage{k}",
                    (0.15, 0.2, 0.012),
                    (rx + sx * 0.075, ry + 0.03, dz + 0.006 + 0.012 * (k == 1)),
                    mat("page", "#f8fafc", 0.8),
                    rot=(0, sx * 0.08, -0.1),
                    bev=0.003,
                )
            )
        objs.append(
            box(
                "sketch-line",
                (0.1, 0.012, 0.004),
                (rx + 0.08, ry + 0.03, dz + 0.022),
                mat("ink", "#34d399", 0.5),
                rot=(0, 0, 0.3),
                bev=0,
            )
        )
    if (
        role == "technical-director"
    ):  # a bare circuit board with a glowing chip, and a flask
        objs.append(
            box(
                "pcb",
                (0.22, 0.15, 0.012),
                (lx, ly, dz + 0.006),
                mat("pcb", "#15803d", 0.5),
                rot=(0, 0, 0.15),
                bev=0.003,
            )
        )
        for k in range(3):
            chip = (
                mat("chip-on", "#818cf8", emit="#a5b4fc", strength=lit)
                if k == 1
                else mat("chip", "#111827", 0.4)
            )
            objs.append(
                box(
                    f"chip{k}",
                    (0.045, 0.045, 0.018),
                    (lx - 0.06 + k * 0.06, ly + 0.01 * (k - 1), dz + 0.02),
                    chip,
                    rot=(0, 0, 0.15),
                    bev=0.003,
                )
            )
        objs.append(
            cyl(
                "flask",
                0.04,
                0.2,
                (rx + 0.06, ry + 0.06, dz + 0.1),
                mat("flask", "#4338ca", 0.3, 0.6),
                bev=0.01,
            )
        )
    if (
        role == "art-director"
    ):  # a pen tablet with its stylus, and a fan of colour swatches
        objs.append(
            box(
                "tablet",
                (0.3, 0.2, 0.012),
                (lx + 0.03, ly + 0.01, dz + 0.006),
                mat("tablet", "#1f2433", 0.4),
                rot=(0, 0, -0.12),
                bev=0.006,
            )
        )
        objs.append(
            box(
                "tablet-face",
                (0.22, 0.14, 0.004),
                (lx + 0.04, ly + 0.012, dz + 0.014),
                mat("tablet-face", "#f472b6", emit="#f9a8d4", strength=lit),
                rot=(0, 0, -0.12),
                bev=0,
            )
        )
        objs.append(
            cyl(
                "stylus",
                0.01,
                0.2,
                (lx + 0.04, ly - 0.08, dz + 0.012),
                mat("stylus", "#e5e7eb", 0.3),
                rot=(0, math.radians(90), 0.25),
            )
        )
        for k, col in enumerate(("#f472b6", "#a78bfa", "#38bdf8", "#fbbf24")):
            objs.append(
                box(
                    f"swatch{k}",
                    (0.06, 0.24, 0.006),
                    (rx + 0.02, ry + 0.06, dz + 0.004 + k * 0.004),
                    mat(f"swatch-{col}", col, 0.6),
                    rot=(0, 0, -0.6 + k * 0.3),
                    bev=0,
                )
            )
    if (
        role == "gameplay-engineer"
    ):  # a pizza box from the night shift, and sticky notes
        objs.append(
            box(
                "pizza",
                (0.32, 0.3, 0.045),
                (lx + 0.01, ly + 0.04, dz + 0.023),
                mat("pizzabox", "#e7c9a0", 0.8),
                rot=(0, 0, 0.1),
                bev=0.006,
            )
        )
        objs.append(
            cyl(
                "pizza-logo",
                0.07,
                0.004,
                (lx + 0.01, ly + 0.04, dz + 0.047),
                mat("pizzalogo", "#dc2626", 0.6),
                verts=32,
            )
        )
        for k, col in enumerate(("#fde047", "#fda4af", "#fde047")):
            objs.append(
                box(
                    f"note{k}",
                    (0.08, 0.08, 0.006),
                    (rx + k * 0.05, ry + 0.02 + 0.03 * (k % 2), dz + 0.003 + k * 0.003),
                    mat(f"note-{col}", col, 0.8),
                    rot=(0, 0, -0.2 + k * 0.25),
                    bev=0,
                )
            )
    if role == "qa":  # a magnifying glass, and the bug it caught
        objs.append(
            torus(
                "lens-rim",
                0.09,
                0.012,
                (lx, ly + 0.02, dz + 0.012),
                mat("rim", "#111827", 0.4),
                minor=8,
            )
        )
        objs.append(
            cyl(
                "lens",
                0.08,
                0.004,
                (lx, ly + 0.02, dz + 0.012),
                mat("lens", "#bae6fd", 0.1),
                verts=32,
            )
        )
        objs.append(
            box(
                "lens-handle",
                (0.13, 0.025, 0.02),
                (lx + 0.13, ly - 0.03, dz + 0.012),
                mat("handle", "#f59e0b", 0.5),
                rot=(0, 0, -0.35),
                bev=0.006,
            )
        )
        objs.append(
            sphere(
                "bug",
                0.06,
                (rx + 0.02, ry + 0.03, dz + 0.01),
                mat("bug", "#ef4444", 0.4),
                scale=(1, 1.25, 0.7),
            )
        )
        objs.append(
            sphere(
                "bug-head",
                0.03,
                (rx + 0.02, ry - 0.03, dz + 0.012),
                mat("bughead", "#111827", 0.4),
            )
        )
    if role == "playtester":  # a handheld console, screen on, and a bag of snacks
        objs.append(
            box(
                "handheld",
                (0.28, 0.12, 0.03),
                (lx + 0.02, ly + 0.02, dz + 0.015),
                mat("handheld", "#f1f5f9", 0.3),
                rot=(math.radians(8), 0, 0.1),
                bev=0.02,
            )
        )
        objs.append(
            box(
                "handheld-screen",
                (0.13, 0.085, 0.004),
                (lx + 0.02, ly + 0.02, dz + 0.032),
                mat("handheld-screen", "#a3e635", emit="#bef264", strength=lit),
                rot=(math.radians(8), 0, 0.1),
                bev=0,
            )
        )
        objs.append(
            box(
                "snacks",
                (0.16, 0.06, 0.2),
                (rx + 0.05, ry + 0.08, dz + 0.1),
                mat("snacks", "#f97316", 0.5),
                rot=(math.radians(-12), 0, -0.2),
                bev=0.02,
            )
        )
    return objs


def build_room():
    """An open-plan office at night: a carpet floor with a walkway between the two rows of desks,
    a back wall with windows, a shelf unit, whiteboards and the Goal display, and plants.
    """
    CURRENT[0] = "room"
    floor = cyl("floor", 16, 0.1, (0, 0, -0.05), floor_mat(), verts=128)
    floor.data.polygons.foreach_set("use_smooth", [False] * len(floor.data.polygons))
    walk = mat("walk", "#3d4a6b", 0.8)
    box(
        "walkway",
        (12.0, 1.0, 0.01),
        (0, (BACK_Y + FRONT_Y) / 2 + 0.1, 0.004),
        walk,
        bev=0,
    )
    wall = mat("wall", "#1a2644", 0.6)
    trim = mat("trim", "#2b3d66", 0.4)
    box("wall", (26, 0.3, 6.0), (0, WALL_Y + 0.15, 3.0), wall, bev=0)
    box("wall-base", (26, 0.1, 0.25), (0, WALL_Y - 0.05, 0.125), trim, bev=0)
    winms = [
        image_mat(f"window{i}", TEX / f"window-{i}.png", 0.9, 0.15) for i in range(3)
    ]
    for k, x in enumerate((-9.2, -7.0, -4.8, 4.8, 7.0, 9.2)):
        win = box(
            f"window{k}", (1.9, 0.03, 2.3), (x, WALL_Y - 0.02, 2.35), winms[k % 3]
        )
        cork_uv(win)
        box(
            f"winframe{k}",
            (2.02, 0.04, 2.42),
            (x, WALL_Y - 0.005, 2.35),
            trim,
            bev=0.01,
        )
    # a low shelf unit along the wall behind the back row, with books, boxes and plants on it
    shelf = mat(*DESK_BODY)
    box("credenza", (9.4, 0.42, 0.78), (0, WALL_Y - 0.24, 0.39), shelf, bev=0.012)
    box(
        "credenza-top",
        (9.5, 0.46, 0.04),
        (0, WALL_Y - 0.24, 0.8),
        mat(*WOOD, coat=0.2),
        bev=0.008,
    )
    # only in the gaps between the back-row seats: anything right above a head gets painted into it
    for k, x in enumerate((-4.2, -2.1, 0.0, 2.1, 4.2)):
        if k % 3 == 0:
            plant(f"shelfplant{k}", (x, WALL_Y - 0.24, 0.82), 0.9)
        elif k % 3 == 1:
            book_stack(
                f"shelfbooks{k}",
                (x, WALL_Y - 0.24, 0.82),
                0,
                ("#ef4444", "#3b82f6", "#f59e0b"),
            )
        else:
            box(
                f"shelfbox{k}",
                (0.36, 0.28, 0.26),
                (x, WALL_Y - 0.24, 0.95),
                mat("cardboard", "#b98a5a", 0.8),
                bev=0.01,
            )
    # the Goal display: a wall screen in a thin frame (the page writes the Goal on it)
    box(
        "goal-frame",
        (GOAL_W + 0.1, 0.06, GOAL_H + 0.1),
        (0, WALL_Y - 0.04, GOAL_Z),
        mat("goalframe", "#2a3550", 0.4),
        bev=0.02,
    )
    box(
        "goal-screen",
        (GOAL_W, 0.06, GOAL_H),
        (0, WALL_Y - 0.07, GOAL_Z),
        mat("goalscreen", "#0b2a5e", emit="#0d2f6b", strength=2),
        bev=0,
    )
    box(
        "goal-led",
        (GOAL_W, 0.02, 0.02),
        (0, WALL_Y - 0.1, GOAL_Z - GOAL_H / 2 - 0.08),
        mat("goalled", "#38bdf8", emit="#38bdf8", strength=4),
        bev=0,
    )
    # whiteboards with sticky notes either side of it
    for sx in (-1, 1):
        b = box(
            f"whiteboard{sx}",
            (1.5, 0.03, 0.95),
            (sx * 3.1, WALL_Y - 0.04, 2.55),
            image_mat("whiteboard", TEX / "board.png", 0.0, 0.8),
            bev=0,
        )
        cork_uv(b)
        box(
            f"wbframe{sx}",
            (1.58, 0.02, 1.03),
            (sx * 3.1, WALL_Y - 0.02, 2.55),
            trim,
            bev=0.008,
        )
    for sx in (-1, 1):
        plant(f"cornerplant{sx}", (sx * 5.3, WALL_Y - 0.6, 0), 2.4, pot="#d9dee8")
        plant(f"frontplant{sx}", (sx * 4.6, -0.9, 0), 2.0, pot="#d9dee8")
    box(
        "cooler",
        (0.36, 0.36, 1.1),
        (-5.0, 1.2, 0.55),
        mat("cooler", "#e5e9f0", 0.4),
        bev=0.03,
    )
    cyl(
        "cooler-bottle",
        0.15,
        0.36,
        (-5.0, 1.2, 1.28),
        mat("bottle", "#7dd3fc", 0.2),
        verts=24,
    )
    box(
        "printer",
        (0.6, 0.45, 0.35),
        (5.0, 1.2, 0.72),
        mat("printer", "#d6dbe4", 0.4),
        bev=0.02,
    )
    box("printer-stand", (0.62, 0.47, 0.55), (5.0, 1.2, 0.275), shelf, bev=0.01)


# --- pods, camera, light, render ------------------------------------------------------------------


POD_OBJS = {}
IDLE_GLOW, BUSY_GLOW = 1.1, 4.0
CHAIRS = {"game-director": "exec", "playtester": "gaming"}
SPRITES = set(PODS)  # Roles drawn as 2D character sprites (make_sprites.py)
HEADROOM = {"gameplay-engineer": 0.14}  # the cat-ear cap stands above the usual head
# `guide`: draw every Role in 3D and render busy layers only for the sprite Roles, as the
# guide make_sprites.py paints over (it sets each sprite's size, place and pose)
GUIDE = "guide" in argv[3:]
BUSY_ROLES = list(SPRITES) if GUIDE else list(PODS)
if GUIDE:
    SPRITES = set()
PROXY = {}


def build_pod(role, pose, glow):
    CURRENT[0] = f"pod-{role}"
    spec = ROLES[role]
    near = front_desk(role, spec, glow) + chair(
        role, spec["color"], CHAIRS.get(role, "task")
    )
    if role in SPRITES:
        CURRENT[0] = f"proxy-{role}"
        PROXY[role] = stand_in(role)
        near += PROXY[role]
        CURRENT[0] = f"pod-{role}"
    else:
        near += character(role, spec, pose)
    pod = station(role, spec, glow)
    bpy.context.view_layer.update()  # matrix_world is stale until the scene updates
    grow = Matrix.Scale(CHAR_SCALE, 4)
    for o in near:
        if o.parent is None:
            o.matrix_world = grow @ o.matrix_world
    objs = pod + near
    roots = [o for o in objs if o.parent is None]
    place(roots, (*PODS[role], 0), 0)
    POD_OBJS[role] = objs
    if glow > 2:  # a spotlight on the working desk
        sp = bpy.data.lights.new(f"spot-{role}", "SPOT")
        sp.color, sp.energy, sp.spot_size, sp.spot_blend, sp.shadow_soft_size = (
            lin("#fff4e0"),
            650,
            math.radians(42),
            0.6,
            0.3,
        )
        so = bpy.data.objects.new(f"spot-{role}", sp)
        so.location = (*PODS[role], 0 + 4.2)
        link(so)
    # light from the monitor wall onto the desk and face: cool when idle, the Role colour at work
    lt = bpy.data.lights.new(f"screenlight-{role}", "AREA")
    lt.color, lt.energy, lt.size = (
        (lin(spec["color"]), 120, 1.2) if glow > 2 else (lin("#bcd7ff"), 45, 1.2)
    )
    lo = bpy.data.objects.new(f"screenlight-{role}", lt)
    m = Matrix.Translation((*PODS[role], 0))
    lo.matrix_world = m @ (  # from the laptop toward the face
        Matrix.Translation((0, -0.8, 1.1))
        @ Euler((math.radians(70), 0, 0)).to_matrix().to_4x4()
    )
    link(lo)


def remove_pod(role):
    for name in (f"pod-{role}", f"proxy-{role}"):
        if name in COLL:
            c = COLL.pop(name)
            for o in list(c.objects):
                bpy.data.objects.remove(o)
            bpy.data.collections.remove(c)


def stand_in(role):
    """Where a sprite character sits: an upright board through the body and a flat one just
    above the desk top for the hands. Rendered alone it gives the page the sprite's visible
    area: whatever stands in front of the boards (the desk, other booths) is cut out."""
    white = mat("standin", "#ffffff", emit="#ffffff", strength=2)
    me = bpy.data.meshes.new(f"standin-{role}")
    w, seat, shoulder = 0.62, 0.38, 1.28  # half width, lowest visible point, shoulders
    desk = (
        DESK_Z + 0.14
    )  # above the desk top and what lies on it (a mug's rim is at + 0.12)
    # up the right side, round over the head (to 1.78, higher for tall headwear), and down
    outline = [(w, seat), (w, shoulder), (0.5, 1.4), (0.4, 1.52)]
    outline += [
        (0.4 * math.cos(a), 1.52 + (0.26 + HEADROOM.get(role, 0)) * math.sin(a))
        for a in [math.radians(d) for d in range(15, 166, 15)]
    ]
    outline += [(-0.4, 1.52), (-0.5, 1.4), (-w, shoulder), (-w, seat)]
    board = [(x, 0.02, z) for x, z in outline]
    me.from_pydata(
        board
        + [
            (-w * 0.85, -0.7, desk),
            (w * 0.85, -0.7, desk),
            (w * 0.85, 0.02, desk),
            (-w * 0.85, 0.02, desk),
        ],
        [],
        [tuple(range(len(board))), tuple(range(len(board), len(board) + 4))],
    )
    obj = bpy.data.objects.new(f"standin-{role}", me)
    link(obj, white)
    return [obj]


def show_stand_ins(on):
    for lc in bpy.context.view_layer.layer_collection.children:
        if lc.name.startswith("proxy-"):
            lc.exclude = not on


AMBIENT, SUN = 0.8, 2.2
CAM_TARGET = Vector((0, 1.2, 2.14))
CAM_ELEV, CAM_DIST, ORTHO_SCALE = 32, 24.0, 13.0


def build_camera():
    cam = bpy.data.cameras.new("cam")
    cam.type, cam.ortho_scale = "ORTHO", ORTHO_SCALE
    obj = bpy.data.objects.new("cam", cam)
    scene.collection.objects.link(obj)
    elev, dist = math.radians(CAM_ELEV), CAM_DIST
    obj.location = CAM_TARGET + Vector(
        (0, -math.cos(elev) * dist, math.sin(elev) * dist)
    )
    obj.rotation_euler = (CAM_TARGET - obj.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = obj
    return obj


def build_lights():
    world = bpy.data.worlds.new("world")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (1, 1, 1, 1)
    bg.inputs["Strength"].default_value = AMBIENT
    scene.world = world
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy, sun.angle = SUN, math.radians(2)
    sun.shadow_filter_radius = 2.0
    so = bpy.data.objects.new("sun", sun)
    # from the front left and above, so faces turned to the camera are lit
    so.rotation_euler = Vector((0.3, 0.8, -0.55)).to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(so)
    CURRENT[0] = "room"
    sky = cyl(
        "backdrop",
        30,
        30,
        (0, 0, 10),
        mat("sky", "#0b1222", emit="#0b1222", strength=2),
    )
    sky.data.flip_normals()
    sky.visible_shadow = False


def setup_render(samples):
    r = scene.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    r.film_transparent = False
    r.filter_size = 1.0
    scene.eevee.taa_render_samples = samples
    scene.eevee.shadow_pool_size = "1024"
    scene.eevee.use_fast_gi = (
        False  # its screen-space noise shows through the tone steps
    )
    vs = scene.view_settings
    vs.view_transform, vs.look, vs.exposure = "Standard", "None", 0.0
    setup_lines(LINE_PX * W / 2560)


def setup_lines(thickness):
    """Freestyle outlines: silhouettes, borders and creases, never on glowing surfaces."""
    r = scene.render
    r.use_freestyle, r.line_thickness_mode = True, "ABSOLUTE"
    fs = bpy.context.view_layer.freestyle_settings
    fs.crease_angle = math.radians(
        160
    )  # bevels (135-150 degrees) count, so lines never flicker
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("lines")
    ls.select_by_visibility = ls.select_by_edge_types = ls.select_by_face_marks = True
    ls.visibility = "VISIBLE"
    ls.select_silhouette = ls.select_border = ls.select_crease = True
    ls.face_mark_negation, ls.face_mark_condition = "EXCLUSIVE", "ONE"
    ls.linestyle = ls.linestyle or bpy.data.linestyles.new("lines")
    ls.linestyle.color = lin(LINE)
    ls.linestyle.thickness = thickness
    return ls


LINE_PX = 2.2


def px(cam, co):
    v = world_to_camera_view(scene, cam, Vector(co))
    return [round(v.x * W, 1), round((1 - v.y) * H, 1)]


def bbox_px(cam, objs, pad=8):
    xs, ys = [], []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type not in ("MESH", "FONT"):
            continue
        for c in o.evaluated_get(dg).bound_box:
            x, y = px(cam, o.matrix_world @ Vector(c))
            xs.append(x)
            ys.append(y)
    x0, y0 = max(0, int(min(xs)) - pad), max(0, int(min(ys)) - pad)
    x1, y1 = min(W, int(max(xs)) + pad), min(H, int(max(ys)) + pad)
    return [x0, y0, x1 - x0, y1 - y0]


def body_px(cam, x, y, z):
    """The screen box of the space a character fills, the same as a sprite's stand-in."""
    pts = [
        px(cam, (x + sx * 0.5 * CHAR_SCALE, y, z + h * CHAR_SCALE))
        for sx in (-1, 1)
        for h in (0.6, 1.78)
    ]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return [
        round(min(xs)),
        round(min(ys)),
        round(max(xs) - min(xs)),
        round(max(ys) - min(ys)),
    ]


def layout(cam):
    bpy.context.view_layer.update()
    out = {"size": [W, H], "hub": {}, "roles": {}}
    gy = WALL_Y - 0.1  # the Goal screen stands in for the old hub
    centre = px(cam, (0, gy, GOAL_Z))
    out["hub"] = {
        "center": centre,
        "top": px(cam, (0, gy, GOAL_Z + GOAL_H / 2)),
        "floor": px(cam, (0, gy, GOAL_Z - GOAL_H / 2)),
        "rx": round(px(cam, (GOAL_W / 2, gy, GOAL_Z))[0] - centre[0], 1),
        "ry": round(px(cam, (0, gy, GOAL_Z - GOAL_H / 2))[1] - centre[1], 1),
    }
    for role, (x, y) in PODS.items():
        ring = [
            px(
                cam,
                (
                    x + math.cos(a) * RUG_R,
                    y + RUG_DY + math.sin(a) * RUG_R,
                    0.02,
                ),
            )
            for a in [i * math.pi / 32 for i in range(64)]
        ]
        xs, ys = [p[0] for p in ring], [p[1] for p in ring]
        out["roles"][role] = {
            "floor": px(cam, (x, y, 0.12)),
            "ring": [
                round((min(xs) + max(xs)) / 2, 1),
                round((min(ys) + max(ys)) / 2, 1),
                round((max(xs) - min(xs)) / 2, 1),
                round((max(ys) - min(ys)) / 2, 1),
            ],
            "front": px(cam, (x, y - 0.95 * CHAR_SCALE - 0.1, 0)),
            "desk": px(cam, (x, y - 0.95 * CHAR_SCALE, DESK_Z * CHAR_SCALE / 2)),
            "row": "back" if y > 1 else "front",
            "body": body_px(cam, x, y, 0),
            "head": px(cam, (x, y, (HEAD_Z + 0.3) * CHAR_SCALE)),
            "box": bbox_px(cam, POD_OBJS[role]),
        }
        if role in SPRITES:
            sb = bbox_px(cam, PROXY[role], pad=0)
            out["roles"][role]["sprite"] = sb
            out["roles"][role]["head"] = [sb[0] + sb[2] / 2, sb[1]]
    return out


def render_to(path):
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def set_holdout(keep):
    """Hold out every collection except the one named `keep` (None: show everything)."""
    for lc in bpy.context.view_layer.layer_collection.children:
        lc.holdout = keep is not None and lc.name != keep


def debug_char(role):
    """A close-up of one pod, for tuning the characters."""
    setup_render(32)
    scene.render.resolution_x, scene.render.resolution_y = 900, 700
    build_lights()
    CURRENT[0] = "room"
    cyl("floor", 6, 0.1, (0, 0, -0.05), floor_mat())
    build_pod(
        role,
        "busy" if "busy" in argv[3:] else "idle",
        BUSY_GLOW if "busy" in argv[3:] else IDLE_GLOW,
    )
    cam = bpy.data.cameras.new("cam")
    cam.lens = 50
    obj = bpy.data.objects.new("cam", cam)
    scene.collection.objects.link(obj)
    x, y = PODS[role]
    close = "head" in argv[3:]
    target = Vector((x, y, 0 + (HEAD_Z * CHAR_SCALE if close else 1.0)))
    d = 2.2 if close else 5.5
    obj.location = target + Vector(
        (0, -math.cos(math.radians(CAM_ELEV)) * d, math.sin(math.radians(CAM_ELEV)) * d)
    )
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = obj
    render_to(OUT / f"debug-{role}.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if ONLY.startswith("char:"):
        return debug_char(ONLY[5:])
    setup_render(8 if PREVIEW else 16)
    build_lights()
    build_room()
    for role in PODS:
        build_pod(role, "idle", IDLE_GLOW)
    cam = build_camera()
    lay = layout(cam)
    if (
        OUT / "layout.json"
    ).exists():  # a partial run keeps the busy boxes it does not redo
        old = json.loads((OUT / "layout.json").read_text())["roles"]
        for role, entry in lay["roles"].items():
            if "busy" in old.get(role, {}):
                entry["busy"] = old[role]["busy"]
    show_stand_ins(False)
    (OUT / "layout.json").write_text(json.dumps(lay, indent=1))
    if ONLY in ("all", "base"):
        render_to(OUT / "office.png")
    if ONLY in ("all", "base", "masks"):
        for role in SPRITES:
            render_mask(role, lay["roles"][role]["sprite"])
    if ONLY in ("all", "busy"):
        scene.render.film_transparent = True
        for role in BUSY_ROLES:
            remove_pod(role)
            build_pod(role, "busy", BUSY_GLOW)
            show_stand_ins(False)
            box_ = bbox_px(cam, POD_OBJS[role], pad=24)
            lay["roles"][role]["busy"] = box_
            r = scene.render
            r.use_border, r.use_crop_to_border = True, True
            r.border_min_x, r.border_max_x = box_[0] / W, (box_[0] + box_[2]) / W
            r.border_min_y, r.border_max_y = (
                1 - (box_[1] + box_[3]) / H,
                1 - box_[1] / H,
            )
            set_holdout(f"pod-{role}")
            lines = bpy.context.view_layer.freestyle_settings.linesets[0]
            lines.select_by_collection, lines.collection = True, COLL[f"pod-{role}"]
            render_to(OUT / f"busy-{role}.png")
            lines.select_by_collection = False
            set_holdout(None)
            remove_pod(role)
            build_pod(role, "idle", IDLE_GLOW)
            show_stand_ins(False)
        scene.render.use_border = False
        scene.render.film_transparent = False
        (OUT / "layout.json").write_text(json.dumps(lay, indent=1))


def set_border(box_):
    r = scene.render
    r.use_border, r.use_crop_to_border = True, True
    r.border_min_x, r.border_max_x = box_[0] / W, (box_[0] + box_[2]) / W
    r.border_min_y, r.border_max_y = 1 - (box_[1] + box_[3]) / H, 1 - box_[1] / H


def render_mask(role, box_):
    """The part of a sprite's stand-in the camera sees: opaque where visible, clear where the
    desk or anything else in front covers it."""
    r = scene.render
    show_stand_ins(True)
    set_holdout(f"proxy-{role}")
    r.film_transparent, r.use_freestyle = True, False
    set_border(box_)
    render_to(OUT / f"mask-{role}.png")
    r.use_border, r.film_transparent, r.use_freestyle = False, False, True
    set_holdout(None)
    show_stand_ins(False)


main()
