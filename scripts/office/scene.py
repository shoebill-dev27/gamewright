"""The virtual office in Blender: run by make_assets.py as
`blender -b --factory-startup -P scene.py -- <textures> <out> <only> [preview]`.

Everything is built from code: a round studio floor, a glass Goal hub, seven desk pods and seven
seated characters. One fixed camera renders the base picture (every Role idle), one busy layer per
Role (its pod with lit screens and a working pose, everything else held out), a portrait per Role,
and layout.json with the screen positions of what the page draws on top.
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

# pod centres on the floor (x right, y away from the camera); the hub is at HUB
PODS = {
    "game-director": (0.0, 4.6),
    "game-designer": (-3.45, 2.9),
    "technical-director": (3.45, 2.9),
    "art-director": (-4.25, -0.75),
    "gameplay-engineer": (4.25, -0.75),
    "qa": (-2.15, -3.95),
    "playtester": (2.15, -3.95),
}
HUB = (0.0, 0.35)
CHAR_SCALE = 1.28
POD_R = 1.62

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def lin(hex_color):
    h = hex_color.lstrip("#")
    c = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


# --- materials ----------------------------------------------------------------------------------

_mats = {}


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
    key = (name, color, rough, metal, emit, strength, coat, transmission, alpha)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = transmission
    b.inputs["Alpha"].default_value = alpha
    if emit:
        b.inputs["Emission Color"].default_value = (*lin(emit), 1)
        b.inputs["Emission Strength"].default_value = strength
    _mats[key] = m
    return m


def image_mat(name, path, strength=0.0, rough=0.4, repeat=None):
    """A textured material; with strength > 0 the texture also glows (screens, windows)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(path), check_existing=True)
    if repeat:
        tc, mp = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (*repeat, 1)
        nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if strength:
        nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
        b.inputs["Emission Strength"].default_value = strength
    return m


def outline_mat():
    if "outline" in bpy.data.materials:
        return bpy.data.materials["outline"]
    m = bpy.data.materials.new("outline")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mix = nt.nodes.new("ShaderNodeMixShader")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*lin("#1d1622"), 1)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs["Fac"])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return m


def skin_face_mat(role, spec):
    """Skin with the face texture projected across the front of the head (object space)."""
    m = bpy.data.materials.new(f"head-{role}")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Subsurface Weight"].default_value = 0.15
    b.inputs["Subsurface Radius"].default_value = (0.3, 0.12, 0.08)
    b.inputs["Subsurface Scale"].default_value = 0.02
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    # u = x / (2R) + 0.5, v = z / (2R) + 0.5 with R = HEAD_R
    for axis, socket in (("X", "X"), ("Z", "Y")):
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY_ADD"
        mul.inputs[1].default_value = 1 / (2 * HEAD_R)
        mul.inputs[2].default_value = 0.5
        nt.links.new(sep.outputs[axis], mul.inputs[0])
        nt.links.new(mul.outputs[0], comb.inputs[socket])
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(TEX / f"face-{role}.png"), check_existing=True)
    tex.extension = "CLIP"
    nt.links.new(comb.outputs["Vector"], tex.inputs["Vector"])
    front = nt.nodes.new("ShaderNodeMath")
    front.operation = "LESS_THAN"
    front.inputs[1].default_value = 0.0
    nt.links.new(sep.outputs["Y"], front.inputs[0])
    fac = nt.nodes.new("ShaderNodeMath")
    fac.operation = "MULTIPLY"
    nt.links.new(tex.outputs["Alpha"], fac.inputs[0])
    nt.links.new(front.outputs[0], fac.inputs[1])
    mixc = nt.nodes.new("ShaderNodeMix")
    mixc.data_type = "RGBA"
    mixc.inputs["A"].default_value = (*lin(spec["skin"]), 1)
    nt.links.new(fac.outputs[0], mixc.inputs["Factor"])
    nt.links.new(tex.outputs["Color"], mixc.inputs["B"])
    nt.links.new(mixc.outputs["Result"], b.inputs["Base Color"])
    return m


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


def arc_slab(name, r0, r1, a0, a1, z0, z1, m, seg=40, bev=0.012):
    """An annular sector between radii r0..r1 and angles a0..a1 (degrees), from z0 to z1."""
    bm = bmesh.new()
    rings = []
    for i in range(seg + 1):
        a = math.radians(a0 + (a1 - a0) * i / seg)
        c, s = math.cos(a), math.sin(a)
        rings.append(
            [
                bm.verts.new((r * c, r * s, z))
                for r, z in ((r0, z0), (r1, z0), (r1, z1), (r0, z1))
            ]
        )
    for i in range(seg):
        for k in range(4):
            bm.faces.new(
                (
                    rings[i][k],
                    rings[i + 1][k],
                    rings[i + 1][(k + 1) % 4],
                    rings[i][(k + 1) % 4],
                )
            )
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    obj = mesh_from_bm(name, bm)
    link(obj, m)
    if bev:
        bevel(obj, bev, 2)
    return obj


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
    return smooth(obj)


def outline(obj, thickness=0.012):
    if "nooutline" in argv[3:]:
        return obj
    obj.data.materials.append(outline_mat())
    mod = obj.modifiers.new("outline", "SOLIDIFY")
    mod.thickness, mod.offset, mod.use_flip_normals = thickness, 1.0, False
    mod.material_offset = len(obj.data.materials) - 1
    mod.use_rim = False
    return obj


def parent(child, par):
    child.parent = par
    child.matrix_parent_inverse = par.matrix_world.inverted()


def place(objs, origin, yaw):
    """Move a group of objects built around (0, 0) to origin, turned by yaw (degrees)."""
    bpy.context.view_layer.update()
    m = Matrix.Translation((*origin, 0)) @ Matrix.Rotation(math.radians(yaw), 4, "Z")
    for o in objs:
        o.matrix_world = m @ o.matrix_world


# --- characters ---------------------------------------------------------------------------------

HEAD_R = 0.30
HEAD_Z = 1.26


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
    shirt = mat(f"shirt-{role}", spec["shirt"], rough=0.75)
    pants = mat("pants", "#2b3142", rough=0.8)
    skin = mat(f"skin-{role}", spec["skin"], rough=0.55)
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
    if spec["acc"] == "tie":  # a blazer over a white shirt: shirt front and a tie
        objs.append(
            box(
                f"shirtfront-{role}",
                (0.13, 0.02, 0.2),
                (0, -0.2, 0.86),
                mat("white", "#f4f6fa", 0.6),
                rot=(0.1, 0, 0),
                bev=0.01,
            )
        )
        objs.append(
            box(
                f"tie-{role}",
                (0.045, 0.02, 0.17),
                (0, -0.215, 0.84),
                mat("tie", "#c0392b", 0.5),
                rot=(0.1, 0, 0),
                bev=0.008,
            )
        )
    if spec["acc"] == "scarf":
        objs.append(
            torus(
                f"scarf-{role}",
                0.15,
                0.05,
                (0, -0.01, 1.0),
                mat("scarf", spec["accent"], 0.8),
                minor=10,
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
                mat("shoe", "#3a3f4f", 0.6),
                scale=(1, 1.5, 0.7),
            )
        )
    for h in hands:
        objs.append(
            outline(sphere(f"hand-{role}", 0.062, h, skin, scale=(1, 1.1, 0.85)), 0.008)
        )
    objs.append(cyl(f"neck-{role}", 0.07, 0.14, (0, 0, 1.0), skin))
    # head with face, ears and hair, as children of a pivot so the head can tilt
    pivot = bpy.data.objects.new(f"headpivot-{role}", None)
    link(pivot)
    pivot.location = (0, -0.05 if busy else 0.05, HEAD_Z - (0.02 if busy else 0))
    turn = 14 if (sum(map(ord, role)) % 2) else -14
    pivot.rotation_euler = (
        math.radians(-4 if busy else -18),
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
    outline(head, 0.012)
    hair = metaball(
        f"mbHair{role}",
        hair_elems(spec["style"]),
        mat(f"hair-{role}", spec["hair"], rough=0.62),
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
        dark = mat("hp", "#1b1f2a", 0.35, 0.3)
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
                    mat("beret", "#7c3aed", 0.8),
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
                mat("beret", "#7c3aed", 0.8),
            )
        )
    if acc == "cap":
        capm = mat("cap", "#3f7d20", 0.6)
        c = sphere(
            f"cap-{role}", R * 1.18, (0, 0.05, 0.12), capm, scale=(1, 1.04, 0.88)
        )
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
                    f"visor-{role}", 0.19, 0.025, (0, 0.4, 0.13), capm, rot=(0.25, 0, 0)
                ),
                0.008,
            )
        )
        parts[-1].scale = (1, 0.8, 1)
        parts.append(
            sphere(
                f"capbadge-{role}",
                0.035,
                (0, -0.26, 0.3),
                mat("badge", "#a3e635", 0.4, emit="#a3e635", strength=1.5),
                scale=(1, 0.3, 1),
            )
        )
    for p in parts:
        p.parent = pivot
    objs += parts + [pivot]
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


def chair(role, color):
    seat = mat("chairfab", "#2a3040", 0.8)
    acc = mat(f"chairacc-{role}", color, 0.5)
    metalm = mat("chairmetal", "#9aa3b5", 0.3, 0.8)
    objs = [box(f"seat-{role}", (0.56, 0.52, 0.1), (0, 0.05, 0.44), seat, bev=0.04)]
    objs.append(
        box(
            f"back-{role}",
            (0.58, 0.12, 0.78),
            (0, 0.33, 0.9),
            seat,
            rot=(math.radians(-10), 0, 0),
            bev=0.05,
        )
    )
    objs.append(
        box(
            f"backstripe-{role}",
            (0.1, 0.13, 0.7),
            (0, 0.33, 0.9),
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


def desk_pod(role, spec, screens_glow):
    """The pod around a character at the origin: platform, ring light, rear console with monitors,
    front desk with keyboard and props, and role-specific items."""
    color = spec["color"]
    objs = []
    objs.append(
        cyl(
            f"plat-{role}",
            POD_R,
            0.16,
            (0, 0, 0.08),
            mat("plattop", "#aeb8c8", 0.4, coat=0.3),
            verts=96,
            bev=0.02,
        )
    )
    objs.append(
        cyl(
            f"platbase-{role}",
            POD_R + 0.06,
            0.06,
            (0, 0, 0.03),
            mat("platbase", "#56627a", 0.5),
            verts=96,
        )
    )
    ring_strength = 14 if screens_glow > 2 else 3
    objs.append(
        torus(
            f"ring-{role}",
            POD_R + 0.03,
            0.022,
            (0, 0, 0.12),
            mat(
                f"ring-{role}-{ring_strength}",
                color,
                0.3,
                emit=color,
                strength=ring_strength,
            ),
            major=128,
            minor=8,
        )
    )
    wood = mat("wood", "#c9a27a", 0.45, coat=0.2)
    white = mat("deskwhite", "#e9edf3", 0.4)
    led = mat(
        f"led-{role}", color, 0.3, emit=color, strength=6 if screens_glow > 2 else 2
    )
    # rear console: a curved desk behind the chair carrying the monitors
    objs.append(arc_slab(f"console-top-{role}", 0.98, 1.5, 25, 155, 0.78, 0.83, wood))
    objs.append(
        arc_slab(f"console-body-{role}", 1.38, 1.48, 27, 153, 0.16, 0.78, white)
    )
    objs.append(
        arc_slab(f"console-led-{role}", 1.0, 1.03, 30, 150, 0.765, 0.78, led, bev=0)
    )
    for a in (30, 150):
        objs.append(
            box(
                f"console-leg{a}-{role}",
                (0.06, 0.4, 0.62),
                (
                    math.cos(math.radians(a)) * 1.22,
                    math.sin(math.radians(a)) * 1.22,
                    0.47,
                ),
                white,
                rot=(0, 0, math.radians(a - 90)),
                bev=0.01,
            )
        )
    for k, a in enumerate((58, 90, 122)):
        r = 1.26
        x, y = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        big = k == 1
        objs += monitor(
            f"mon{k}-{role}",
            0.72 if big else 0.6,
            0.44 if big else 0.37,
            (x, y, 1.13 if big else 1.08),
            a - 90,
            TEX / f"screen-{role}-{k}.png",
            screens_glow,
            tilt=-4,
        )
    objs += plant(
        f"plant-a-{role}",
        (math.cos(math.radians(160)) * 1.33, math.sin(math.radians(160)) * 1.33, 0.83),
        0.85,
    )
    objs += plant(
        f"plant-b-{role}",
        (math.cos(math.radians(22)) * 1.33, math.sin(math.radians(22)) * 1.33, 0.83),
        0.7,
    )
    # a rug under the chair and a warm desk lamp at the console end
    objs.append(
        cyl(
            f"rug-{role}",
            1.05,
            0.012,
            (0, -0.05, 0.166),
            mat(f"rug-{role}", "#26314d", 0.9),
            verts=64,
        )
    )
    objs.append(
        torus(
            f"rugedge-{role}",
            1.05,
            0.012,
            (0, -0.05, 0.17),
            mat(f"rugedge-{role}", color, 0.6),
            major=96,
            minor=6,
        )
    )
    lx, ly = math.cos(math.radians(140)) * 1.2, math.sin(math.radians(140)) * 1.2
    lampm = mat("lamp", "#2b3142", 0.35, 0.5)
    objs.append(cyl(f"lampbase-{role}", 0.07, 0.025, (lx, ly, 0.845), lampm))
    objs.append(
        cyl(
            f"lamparm-{role}",
            0.012,
            0.42,
            (lx + 0.06, ly - 0.03, 1.04),
            lampm,
            rot=(0.25, 0.35, 0),
        )
    )
    objs.append(
        cyl(
            f"lamphead-{role}",
            0.07,
            0.09,
            (lx + 0.15, ly - 0.09, 1.24),
            mat("lamphead", "#fff3d6", 0.3, emit="#ffd9a0", strength=6),
            r2=0.03,
            rot=(-0.6, 0.4, 0),
        )
    )
    lt = bpy.data.lights.new(f"lamp-{role}", "POINT")
    lt.color, lt.energy, lt.shadow_soft_size = lin("#ffc98a"), 22, 0.15
    lo = bpy.data.objects.new(f"lamp-{role}", lt)
    lo.location = (lx + 0.15, ly - 0.12, 1.18)
    link(lo)
    objs.append(lo)
    # a low shelf behind the console end with binders and a little figure
    sx, sy = math.cos(math.radians(118)) * 1.72, math.sin(math.radians(118)) * 1.72
    shelf = mat("shelf", "#e3e7ee", 0.45)
    objs.append(
        box(
            f"shelf-{role}",
            (0.62, 0.3, 0.62),
            (sx, sy, 0.47),
            shelf,
            rot=(0, 0, math.radians(28)),
            bev=0.012,
        )
    )
    for i, col in enumerate(("#ef4444", "#3b82f6", "#22c55e", "#f59e0b", color)):
        ox = (i - 2) * 0.1
        objs.append(
            box(
                f"binder{i}-{role}",
                (0.07, 0.22, 0.26),
                (
                    sx + math.cos(math.radians(28)) * ox,
                    sy + math.sin(math.radians(28)) * ox,
                    0.93,
                ),
                mat(f"binder{i}", col, 0.55),
                rot=(0, 0, math.radians(28 + (i - 2) * 3)),
                bev=0.006,
            )
        )
    objs.append(
        sphere(
            f"figure-{role}",
            0.06,
            (sx + 0.22, sy + 0.12, 0.85),
            mat(f"fig-{role}", color, 0.35, coat=0.6),
        )
    )
    objs.append(
        sphere(
            f"figurehead-{role}",
            0.05,
            (sx + 0.22, sy + 0.12, 0.95),
            mat("figskin", "#f6d2b8", 0.5),
        )
    )
    for i, col in enumerate(("#fde047", "#f9a8d4", "#86efac")):
        a_ = math.radians(90)
        objs.append(
            box(
                f"sticky{i}-{role}",
                (0.07, 0.006, 0.07),
                (
                    math.cos(a_) * 1.26 - 0.36 + i * 0.08,
                    math.sin(a_) * 1.26 - 0.035,
                    0.95 + (i % 2) * 0.05,
                ),
                mat(f"sticky{i}", col, 0.8),
                rot=(0, (i - 1) * 0.15, 0),
                bev=0,
            )
        )
    for i, col in enumerate(("#ef4444", "#3b82f6", "#f59e0b")):
        objs.append(
            box(
                f"book{i}-{role}",
                (0.2, 0.28, 0.035),
                (
                    math.cos(math.radians(40)) * 1.18,
                    math.sin(math.radians(40)) * 1.18,
                    0.85 + i * 0.037,
                ),
                mat(f"book{i}", col, 0.7),
                rot=(0, 0, 0.5 + i * 0.12),
                bev=0.004,
            )
        )
    objs += role_props(role, spec)
    return objs


def front_desk(role, spec, screens_glow):
    """A small curved desk in front of the character with the keyboard, mouse and mug."""
    color = spec["color"]
    wood = mat("wood", "#c9a27a", 0.45, coat=0.2)
    white = mat("deskwhite", "#e9edf3", 0.4)
    led = mat(
        f"led-{role}", color, 0.3, emit=color, strength=6 if screens_glow > 2 else 2
    )
    objs = []
    objs.append(arc_slab(f"front-top-{role}", 0.5, 0.92, 232, 308, 0.7, 0.74, wood))
    objs.append(arc_slab(f"front-body-{role}", 0.84, 0.92, 234, 306, 0.16, 0.7, white))
    objs.append(
        arc_slab(f"front-led-{role}", 0.92, 0.93, 236, 304, 0.6, 0.62, led, bev=0)
    )
    kb = box(
        f"kb-{role}",
        (0.42, 0.14, 0.02),
        (0, -0.62, 0.755),
        image_mat("keyboard", TEX / "keyboard.png", 0.0, 0.5),
        bev=0.004,
    )
    cork_uv(kb, "xy")
    objs.append(kb)
    objs.append(
        sphere(
            f"mouse-{role}",
            0.03,
            (0.3, -0.62, 0.76),
            mat("mouse", "#e5e7eb", 0.3),
            scale=(1, 1.5, 0.6),
        )
    )
    mug = mat(f"mug-{role}", color, 0.35, coat=0.5)
    objs.append(cyl(f"mug-{role}", 0.045, 0.1, (-0.36, -0.56, 0.79), mug, bev=0.004))
    objs.append(
        torus(
            f"mughandle-{role}",
            0.03,
            0.009,
            (-0.41, -0.56, 0.79),
            mug,
            rot=(math.pi / 2, 0, 0),
            minor=6,
        )
    )
    return objs


def role_props(role, spec):
    c = spec["color"]
    objs = []
    if role == "game-director":
        objs += monitor(
            "wall-dir",
            1.5,
            0.82,
            (0, 1.75, 1.95),
            0,
            TEX / "screen-game-director-1.png",
            1.6,
            stand=False,
        )
        objs.append(
            box(
                "wall-dir-post",
                (0.08, 0.08, 1.6),
                (0, 1.8, 0.95),
                mat("post", "#3a4358", 0.4),
                bev=0.01,
            )
        )
        objs.append(
            cyl(
                "trophy",
                0.06,
                0.16,
                (0.42, -0.58, 0.82),
                mat("gold", "#f5b942", 0.25, 1.0),
                r2=0.03,
            )
        )
        objs.append(
            sphere(
                "trophy-cup",
                0.07,
                (0.42, -0.58, 0.95),
                mat("gold", "#f5b942", 0.25, 1.0),
                scale=(1, 1, 0.8),
            )
        )
    if role == "game-designer":
        objs.append(
            box(
                "corkboard",
                (1.3, 0.04, 0.85),
                (-0.1, 1.72, 1.8),
                image_mat("cork", TEX / "board.png", 0.0, 0.8),
                bev=0.0,
            )
        )
        cork_uv(objs[-1])
        for i, col in enumerate(("#fde047", "#f9a8d4", "#86efac")):
            objs.append(
                box(
                    f"sketch{i}",
                    (0.2, 0.28, 0.01),
                    (0.2 + i * 0.05, -0.55 + i * 0.01, 0.75 + i * 0.006),
                    mat(f"paper{i}", col, 0.8),
                    rot=(0, 0, 0.3 * i - 0.2),
                    bev=0.0,
                )
            )
    if role == "technical-director":
        rack = mat("rack", "#1c2232", 0.35, 0.4)
        objs.append(box("rack", (0.42, 0.4, 1.1), (1.25, 0.95, 0.72), rack, bev=0.02))
        for i in range(6):
            objs.append(
                box(
                    f"rackled{i}",
                    (0.3, 0.01, 0.04),
                    (1.25, 0.745, 0.35 + i * 0.15),
                    mat(
                        f"rackled{i % 2}",
                        "#818cf8" if i % 2 else "#34d399",
                        0.3,
                        emit="#818cf8" if i % 2 else "#34d399",
                        strength=5,
                    ),
                    bev=0.0,
                )
            )
        objs += monitor(
            "wall-tech",
            1.1,
            0.62,
            (-0.15, 1.75, 1.85),
            0,
            TEX / "screen-technical-director-0.png",
            1.4,
            stand=False,
        )
    if role == "art-director":
        objs.append(
            box(
                "tablet",
                (0.42, 0.3, 0.015),
                (0.08, -0.6, 0.765),
                mat("tablet", "#1a1d29", 0.3),
                rot=(0, 0, 0.2),
                bev=0.004,
            )
        )
        objs.append(
            cyl(
                "pen",
                0.008,
                0.18,
                (0.3, -0.58, 0.78),
                mat("pen", "#f472b6", 0.4),
                rot=(0, math.pi / 2, 0.6),
            )
        )
        objs.append(
            box(
                "easel-board",
                (0.8, 0.03, 0.62),
                (-1.15, 0.85, 1.5),
                image_mat("easel", TEX / "screen-art-director-0.png", 0.6, 0.6),
                rot=(math.radians(-8), 0, math.radians(40)),
                bev=0.0,
            )
        )
        cork_uv(objs[-1])
        objs.append(
            box(
                "easel-leg",
                (0.05, 0.05, 1.3),
                (-1.15, 0.88, 0.8),
                mat("easelwood", "#a0784f", 0.6),
                rot=(0, 0, math.radians(40)),
                bev=0.01,
            )
        )
    if role == "gameplay-engineer":
        can = mat("can", "#22c55e", 0.25, 0.8)
        objs.append(cyl("can", 0.035, 0.12, (0.42, -0.6, 0.8), can))
        objs += monitor(
            "mon-extra-eng",
            0.5,
            0.32,
            (1.25, 0.6, 1.02),
            30,
            TEX / "screen-gameplay-engineer-2.png",
            1.2,
            tilt=-4,
        )
    if role == "qa":
        objs.append(
            box(
                "clipboard",
                (0.22, 0.3, 0.015),
                (0.32, -0.58, 0.765),
                mat("clip", "#e2e8f0", 0.6),
                rot=(0, 0, -0.3),
                bev=0.004,
            )
        )
        objs.append(
            torus(
                "magnifier",
                0.05,
                0.01,
                (-0.12, -0.5, 0.77),
                mat("frame", "#1f2430", 0.3, 0.6),
                minor=8,
            )
        )
        objs.append(
            box(
                "bugboard",
                (0.9, 0.04, 0.6),
                (1.0, 1.25, 1.55),
                image_mat("bugs", TEX / "screen-qa-0.png", 1.0, 0.4),
                rot=(0, 0, math.radians(-35)),
                bev=0.0,
            )
        )
        cork_uv(objs[-1])
    if role == "playtester":
        pad = mat("pad", "#2d3346", 0.4)
        objs.append(
            box("controller", (0.2, 0.12, 0.04), (0.05, -0.6, 0.77), pad, bev=0.02)
        )
        for sx in (-1, 1):
            objs.append(
                sphere(
                    f"grip{sx}",
                    0.05,
                    (0.05 + sx * 0.1, -0.64, 0.765),
                    pad,
                    scale=(1, 1.3, 0.6),
                )
            )
        objs.append(
            sphere(
                "padbutton",
                0.015,
                (0.11, -0.6, 0.795),
                mat("btn", "#a3e635", 0.3, emit="#a3e635", strength=3),
            )
        )
        objs += monitor(
            "tv-play",
            1.3,
            0.74,
            (0, 1.75, 1.9),
            0,
            TEX / "screen-playtester-1.png",
            1.8,
            stand=False,
        )
    return objs


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
    m = bpy.data.materials.new("floor")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.offset = 0.0
    brick.inputs["Color1"].default_value = (*lin("#1e2c4b"), 1)
    brick.inputs["Color2"].default_value = (*lin("#22325a"), 1)
    brick.inputs["Mortar"].default_value = (*lin("#33497a"), 1)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Brick Width"].default_value = 1.2
    brick.inputs["Row Height"].default_value = 1.2
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.22
    b.inputs["Coat Weight"].default_value = 0.4
    return m


def build_room():
    CURRENT[0] = "room"
    floor = cyl("floor", 16, 0.1, (0, 0, -0.05), floor_mat(), verts=128)
    floor.data.polygons.foreach_set("use_smooth", [False] * len(floor.data.polygons))
    # walkway rings and spokes of light on the floor
    cyan = mat("floorline", "#38bdf8", 0.3, emit="#38bdf8", strength=2.5)
    torus("walk-inner", 1.95, 0.02, (*HUB, 0.01), cyan, major=128, minor=6)
    torus(
        "walk-outer",
        7.6,
        0.025,
        (0, 0.2, 0.01),
        mat("floorline2", "#6366f1", 0.3, emit="#6366f1", strength=1.5),
        major=192,
        minor=6,
    )
    for role, (x, y) in PODS.items():
        dx, dy = x - HUB[0], y - HUB[1]
        d = math.hypot(dx, dy)
        length = d - 1.95 - POD_R - 0.1
        mid = (
            HUB[0] + dx / d * (1.95 + length / 2),
            HUB[1] + dy / d * (1.95 + length / 2),
            0.008,
        )
        box(
            f"spoke-{role}",
            (0.05, length, 0.01),
            mid,
            mat(
                f"spoke-{role}",
                ROLES[role]["color"],
                0.3,
                emit=ROLES[role]["color"],
                strength=1.2,
            ),
            rot=(0, 0, math.atan2(dy, dx) - math.pi / 2),
            bev=0,
        )
    # the back wall: panels, windows, shelves and planters
    wall = mat("wall", "#17223d", 0.6)
    trim = mat("trim", "#2b3d66", 0.4)
    arc_slab("wall", 9.4, 9.8, 0, 180, 0, 3.6, wall, seg=96, bev=0)
    arc_slab("wall-trim", 9.2, 9.45, 0, 180, 3.45, 3.6, trim, seg=96, bev=0)
    arc_slab(
        "wall-strip",
        9.37,
        9.4,
        1,
        179,
        2.95,
        3.0,
        mat("wallstrip", "#38bdf8", 0.3, emit="#38bdf8", strength=4),
        seg=96,
        bev=0,
    )
    arc_slab(
        "wall-base",
        9.15,
        9.4,
        0,
        180,
        0,
        0.25,
        mat("wallbase", "#0f1830", 0.5),
        seg=96,
        bev=0,
    )
    winms = [
        image_mat(f"window{i}", TEX / f"window-{i}.png", 0.9, 0.15) for i in range(3)
    ]
    for k, a in enumerate(range(12, 172, 14)):
        if 76 < a < 104:
            continue
        ar = math.radians(a)
        x, y = math.cos(ar) * 9.35, math.sin(ar) * 9.35
        win = box(
            f"window{k}",
            (1.7, 0.03, 1.9),
            (x, y, 1.75),
            winms[k % 3],
            rot=(0, 0, ar - math.pi / 2),
            bev=0,
        )
        cork_uv(win)
        box(
            f"winframe{k}",
            (1.82, 0.05, 2.02),
            (x * 1.002, y * 1.002, 1.75),
            trim,
            rot=(0, 0, ar - math.pi / 2),
            bev=0.01,
        )
    for k, a in enumerate(range(6, 178, 12)):
        ar = math.radians(a)
        plant(f"wallplant{k}", (math.cos(ar) * 9.6, math.sin(ar) * 9.6, 3.6), 1.6)
    # sign above the back wall
    sign_bg = box(
        "sign",
        (6.4, 0.12, 1.25),
        (0, 9.0, 3.85),
        mat("signbg", "#101a33", 0.4, coat=0.5),
        bev=0.06,
    )
    box(
        "sign-edge",
        (6.5, 0.1, 1.35),
        (0, 9.06, 3.85),
        mat("signedge", "#38bdf8", 0.3, emit="#38bdf8", strength=3),
        bev=0.06,
    )
    for text, size, z, color, strength in (
        ("VIRTUAL  AI  GAME  STUDIO", 0.48, 3.95, "#eef4ff", 6),
        ("CREATE  ·  PLAY  ·  TOGETHER", 0.22, 3.45, "#7dd3fc", 4),
    ):
        cu = bpy.data.curves.new(f"text-{z}", "FONT")
        cu.body, cu.size, cu.align_x, cu.extrude = text, size, "CENTER", 0.01
        t = bpy.data.objects.new(f"text-{z}", cu)
        t.location, t.rotation_euler = (0, 8.92, z - size * 0.35), (math.pi / 2, 0, 0)
        t.visible_glossy = False
        link(t, mat(f"signtext-{z}", color, 0.4, emit=color, strength=strength))
    # side wall screens and big plants at the corners (mostly under the page's side panels)
    for sx in (-1, 1):
        for k, a in enumerate((25, 40)):
            ar = math.radians(90 + sx * (90 - a))
            x, y = math.cos(ar) * 9.3, math.sin(ar) * 9.3
            monitor(
                f"wallscreen{sx}{k}",
                1.8,
                1.05,
                (x, y, 1.9),
                math.degrees(ar) - 90,
                TEX / f"screen-{'qa' if sx > 0 else 'game-director'}-{k}.png",
                1.3,
                stand=False,
            )
        for k, (px_, py_) in enumerate(
            ((sx * 8.0, 4.4), (sx * 8.6, 1.0), (sx * 8.3, -3.4))
        ):
            plant(f"bigplant{sx}{k}", (px_, py_, 0), 2.6, pot="#d9dee8")
    # the hub: stepped base, ring light, glass dome, wire globe and an orbit ring
    hx, hy = HUB
    cyl(
        "hub-base",
        1.5,
        0.12,
        (hx, hy, 0.06),
        mat("hubbase", "#2a3a5e", 0.4, coat=0.4),
        verts=96,
        bev=0.02,
    )
    cyl(
        "hub-step",
        1.22,
        0.22,
        (hx, hy, 0.17),
        mat("hubstep", "#7d8cab", 0.35, coat=0.3),
        verts=96,
        bev=0.02,
    )
    torus(
        "hub-ring",
        1.24,
        0.03,
        (hx, hy, 0.28),
        mat("hubring", "#38bdf8", 0.3, emit="#38bdf8", strength=6),
        major=128,
        minor=8,
    )
    torus(
        "hub-ring2",
        1.52,
        0.02,
        (hx, hy, 0.12),
        mat("hubring2", "#38bdf8", 0.3, emit="#38bdf8", strength=6),
        major=128,
        minor=8,
    )
    dome = sphere("hub-dome", 1.0, (hx, hy, 0.28), dome_mat(), seg=64)
    bm = bmesh.new()
    bm.from_mesh(dome.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.02], context="VERTS")
    bm.to_mesh(dome.data)
    bm.free()
    globe = bpy.data.objects.new("hub-globe", bpy.data.meshes.new("hub-globe"))
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.58)
    bm.to_mesh(globe.data)
    bm.free()
    globe.location = (hx, hy, 1.05)
    link(globe, mat("globe", "#7dd3fc", 0.3, emit="#7dd3fc", strength=4))
    wf = globe.modifiers.new("wire", "WIREFRAME")
    wf.thickness = 0.012
    sphere(
        "hub-core",
        0.3,
        (hx, hy, 1.05),
        mat("core", "#1d4ed8", 0.3, emit="#2563eb", strength=1.2),
        seg=32,
    )
    torus(
        "hub-orbit",
        0.8,
        0.012,
        (hx, hy, 1.05),
        mat("orbit", "#a5f3fc", 0.3, emit="#a5f3fc", strength=8),
        rot=(math.radians(72), math.radians(12), 0),
        major=128,
        minor=6,
    )
    light = bpy.data.lights.new("hub-light", "POINT")
    light.color, light.energy, light.shadow_soft_size = lin("#7dd3fc"), 220, 0.8
    lo = bpy.data.objects.new("hub-light", light)
    lo.location = (hx, hy, 1.2)
    link(lo)


def dome_mat():
    m = bpy.data.materials.new("dome")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*lin("#3aa0ff"), 1)
    em.inputs["Strength"].default_value = 1.1
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    tr.inputs["Color"].default_value = (*lin("#bfe9ff"), 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    gl = nt.nodes.new("ShaderNodeBsdfGlossy")
    gl.inputs["Roughness"].default_value = 0.05
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(lw.outputs["Facing"], mix.inputs["Fac"])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], add.inputs[0])
    gm = nt.nodes.new("ShaderNodeMixShader")
    gm.inputs["Fac"].default_value = 0.92
    nt.links.new(gl.outputs["BSDF"], gm.inputs[1])
    nt.links.new(tr.outputs["BSDF"], gm.inputs[2])
    nt.links.new(add.outputs["Shader"], out.inputs["Surface"])
    return m


# --- pods, camera, light, render ------------------------------------------------------------------


def yaw_of(role):
    """Pods face the camera, turned a little toward the hub."""
    x, y = PODS[role]
    return max(-22, min(22, -x * 4.0))


POD_OBJS = {}


def build_pod(role, pose, glow):
    CURRENT[0] = f"pod-{role}"
    spec = ROLES[role]
    near = (
        chair(role, spec["color"])
        + front_desk(role, spec, glow)
        + character(role, spec, pose)
    )
    pod = desk_pod(role, spec, glow)
    bpy.context.view_layer.update()  # matrix_world is stale until the scene updates
    for o in near:
        if o.parent is None:
            o.matrix_world = Matrix.Scale(CHAR_SCALE, 4) @ o.matrix_world
    for o in pod:  # role props lying on the front desk move up with it
        if (
            o.parent is None
            and Vector(o.location[:2]).length < 0.95
            and o.location.z > 0.5
        ):
            o.matrix_world = Matrix.Scale(CHAR_SCALE, 4) @ o.matrix_world
    objs = pod + near
    roots = [o for o in objs if o.parent is None]
    place(roots, PODS[role], yaw_of(role))
    POD_OBJS[role] = objs
    if (
        glow > 2
    ):  # a spotlight on the working desk, and light from the screens on the face
        sp = bpy.data.lights.new(f"spot-{role}", "SPOT")
        sp.color, sp.energy, sp.spot_size, sp.spot_blend, sp.shadow_soft_size = (
            lin("#fff4e0"),
            650,
            math.radians(42),
            0.6,
            0.3,
        )
        so = bpy.data.objects.new(f"spot-{role}", sp)
        so.location = (*PODS[role], 4.2)
        link(so)
        lt = bpy.data.lights.new(f"screenlight-{role}", "AREA")
        lt.color, lt.energy, lt.size = lin(spec["color"]), 120, 1.2
        lo = bpy.data.objects.new(f"screenlight-{role}", lt)
        m = Matrix.Translation((*PODS[role], 0)) @ Matrix.Rotation(
            math.radians(yaw_of(role)), 4, "Z"
        )
        lo.matrix_world = m @ (
            Matrix.Translation((0, 0.9, 1.5))
            @ Euler((math.radians(-70), 0, 0)).to_matrix().to_4x4()
        )
        link(lo)


def remove_pod(role):
    c = COLL.pop(f"pod-{role}")
    for o in list(c.objects):
        bpy.data.objects.remove(o)
    bpy.data.collections.remove(c)


CAM_TARGET = Vector((0, -0.7, 1.3))
CAM_ELEV, CAM_DIST, CAM_LENS = 40, 24.0, 40


def build_camera():
    cam = bpy.data.cameras.new("cam")
    cam.lens = CAM_LENS
    cam.sensor_width = 36
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
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        *lin("#26324f"),
        1,
    )
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
    scene.world = world
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy, sun.angle, sun.color = 2.8, math.radians(8), lin("#ffe2bd")
    so = bpy.data.objects.new("sun", sun)
    so.rotation_euler = (math.radians(40), math.radians(-24), math.radians(-35))
    scene.collection.objects.link(so)
    fill = bpy.data.lights.new("fill", "AREA")
    fill.energy, fill.size, fill.color = 2200, 16, lin("#cfe0ff")
    fo = bpy.data.objects.new("fill", fill)
    fo.location = (0, -2, 11)
    scene.collection.objects.link(fo)


def setup_render(samples):
    r = scene.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = W, H, 100
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    r.film_transparent = False
    c = scene.cycles
    c.samples, c.use_denoising = samples, True
    c.max_bounces, c.transparent_max_bounces = 8, 16
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "CUDA"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = d.type == "CUDA"
        c.device = "GPU"
    except Exception as e:  # CPU still works, only slower
        print("GPU unavailable:", e)
    vs = scene.view_settings
    vs.view_transform = "AgX"
    for look in ("AgX - Medium High Contrast", "Medium High Contrast"):
        try:
            vs.look = look
            break
        except TypeError:
            pass
    vs.exposure = 0.7


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


def layout(cam):
    bpy.context.view_layer.update()
    out = {"size": [W, H], "hub": {}, "roles": {}}
    hx, hy = HUB
    out["hub"] = {
        "center": px(cam, (hx, hy, 1.05)),
        "top": px(cam, (hx, hy, 2.4)),
        "floor": px(cam, (hx, hy, 0)),
        "rx": round(px(cam, (hx + 1.55, hy, 0))[0] - px(cam, (hx, hy, 0))[0], 1),
        "ry": round(px(cam, (hx, hy - 1.55, 0))[1] - px(cam, (hx, hy, 0))[1], 1),
    }
    for role, (x, y) in PODS.items():
        ring = [
            px(
                cam,
                (
                    x + math.cos(a) * (POD_R + 0.03),
                    y + math.sin(a) * (POD_R + 0.03),
                    0.12,
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
            "front": px(cam, (x, y - POD_R - 0.1, 0.0)),
            "head": px(cam, (x, y, HEAD_Z + 0.55)),
            "box": bbox_px(cam, POD_OBJS[role]),
        }
    return out


def render_to(path):
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def set_holdout(keep):
    """Hold out every collection except `keep` (None: show everything)."""
    for lc in bpy.context.view_layer.layer_collection.children:
        lc.holdout = keep is not None and lc.name != f"pod-{keep}"


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
        3.2 if "busy" in argv[3:] else 0.7,
    )
    cam = bpy.data.cameras.new("cam")
    cam.lens = 50
    obj = bpy.data.objects.new("cam", cam)
    scene.collection.objects.link(obj)
    x, y = PODS[role]
    close = "head" in argv[3:]
    target = Vector((x, y, HEAD_Z if close else 1.0))
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
    setup_render(24 if PREVIEW else 160)
    build_lights()
    build_room()
    for role in PODS:
        build_pod(role, "idle", 0.7)
    cam = build_camera()
    lay = layout(cam)
    (OUT / "layout.json").write_text(json.dumps(lay, indent=1))
    if ONLY in ("all", "base"):
        render_to(OUT / "office.png")
    if ONLY in ("all", "busy"):
        scene.render.film_transparent = True
        for role in PODS:
            remove_pod(role)
            build_pod(role, "busy", 3.2)
            box_ = bbox_px(cam, POD_OBJS[role], pad=24)
            lay["roles"][role]["busy"] = box_
            r = scene.render
            r.use_border, r.use_crop_to_border = True, True
            r.border_min_x, r.border_max_x = box_[0] / W, (box_[0] + box_[2]) / W
            r.border_min_y, r.border_max_y = (
                1 - (box_[1] + box_[3]) / H,
                1 - box_[1] / H,
            )
            set_holdout(role)
            render_to(OUT / f"busy-{role}.png")
            set_holdout(None)
            remove_pod(role)
            build_pod(role, "idle", 0.7)
        scene.render.use_border = False
        scene.render.film_transparent = False
        (OUT / "layout.json").write_text(json.dumps(lay, indent=1))
    if ONLY in ("all", "faces"):
        portraits(cam)


def portraits(main_cam):
    """A head-and-shoulders portrait per Role for the agent card."""
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = 256
    cam = bpy.data.cameras.new("portrait")
    cam.lens = 85
    obj = bpy.data.objects.new("portrait", cam)
    scene.collection.objects.link(obj)
    scene.camera = obj
    for role, (x, y) in PODS.items():
        yaw = math.radians(yaw_of(role))
        head = Vector((x, y, HEAD_Z - 0.02))
        fwd = Vector((math.sin(yaw), -math.cos(yaw), 0))
        obj.location = head + fwd * 4.2 + Vector((0, 0, 0.5))
        obj.rotation_euler = (
            (head + Vector((0, 0, -0.05)) - obj.location)
            .to_track_quat("-Z", "Y")
            .to_euler()
        )
        set_holdout(role)
        render_to(OUT / f"face-{role}.png")
    set_holdout(None)
    scene.camera = main_cam
    scene.render.resolution_x, scene.render.resolution_y = W, H


main()
