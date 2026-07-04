# สร้าง circuit.glb — ESP32 devkit บนเบรดบอร์ด ต่อสายจัมป์ไปโมดูลเซนเซอร์ + LED
# ใช้: python make_model.py  (ต้องมี trimesh)  แล้วแปลงเป็น usdz ด้วย make_usdz.html
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals

S = 0.02  # หน่วยโมเดล = cm, ส่งออกเป็นเมตร x2 ของจริง (เบรดบอร์ด ~33cm ใน AR)
parts = []

def add(mesh, color, metal=0.0, rough=0.7, emissive=None):
    mesh.visual = TextureVisuals(material=PBRMaterial(
        baseColorFactor=[*color, 1.0], metallicFactor=metal, roughnessFactor=rough,
        emissiveFactor=list(emissive) if emissive else None))
    parts.append(mesh)

def box(sx, sy, sz, x, y, z, color, **kw):
    b = trimesh.creation.box(extents=[sx, sy, sz])
    b.unmerge_vertices()  # flat shading — ขอบกล่องคม ไม่โดนเฉลี่ยแสงมน
    b.apply_translation([x, y, z])
    add(b, color, **kw)

def seg(a, b, r, color, **kw):
    add(trimesh.creation.cylinder(radius=r, segment=[list(a), list(b)], sections=12), color, **kw)

def wire(pts, r, color):
    for i in range(len(pts) - 1):
        seg(pts[i], pts[i + 1], r, color, rough=0.45)

# ---- เบรดบอร์ด ----
box(16.5, 5.6, 0.9, 0, 0, 0.45, (0.93, 0.93, 0.91), rough=0.85)
box(16.5, 0.3, 0.08, 0, 0, 0.92, (0.72, 0.72, 0.72))                       # ร่องกลาง
for y, col in [(2.45, (0.85, 0.15, 0.15)), (2.15, (0.15, 0.3, 0.85)),
               (-2.45, (0.15, 0.3, 0.85)), (-2.15, (0.85, 0.15, 0.15))]:   # เส้นราง +/-
    box(15.8, 0.12, 0.04, 0, y, 0.93, col)

# ---- ESP32 DevKit (คร่อมร่องกลาง) ----
px, pz = -4.0, 1.62
box(5.2, 2.9, 0.16, px, 0, pz, (0.05, 0.05, 0.08), rough=0.5)              # PCB ดำ
box(1.55, 1.7, 0.30, px - 1.6, 0, pz + 0.23, (0.8, 0.82, 0.85), metal=0.95, rough=0.25)  # ฝาโลหะ WiFi
box(0.5, 2.0, 0.06, px - 2.45, 0, pz + 0.12, (0.02, 0.02, 0.02))           # โซนเสาอากาศ
box(0.75, 1.1, 0.35, px + 2.35, 0, pz + 0.20, (0.75, 0.75, 0.78), metal=0.9, rough=0.3)  # micro-USB
for sy in (1.25, -1.25):
    box(4.6, 0.24, 0.55, px, sy, pz - 0.38, (0.15, 0.15, 0.15))            # แถวขา
for sy in (0.95, -0.95):
    box(0.3, 0.3, 0.12, px + 1.9, sy, pz + 0.14, (0.1, 0.1, 0.1))          # ปุ่ม EN/BOOT
box(0.28, 0.28, 0.1, px + 0.9, 0.7, pz + 0.13, (1, 0.1, 0.1), emissive=(1, 0.05, 0.05))   # LED ไฟเข้า
box(0.28, 0.28, 0.1, px + 0.9, -0.7, pz + 0.13, (0.2, 0.4, 1), emissive=(0.1, 0.3, 1.0))  # LED ฟ้า

# ---- โมดูลเซนเซอร์ (PCB น้ำเงิน) ----
mx, my, mz = 4.8, -1.3, 1.45
box(1.7, 1.5, 0.14, mx, my, mz, (0.05, 0.25, 0.6), rough=0.5)
box(0.65, 0.65, 0.14, mx, my, mz + 0.14, (0.05, 0.05, 0.05))
for i in range(4):                                                          # ขาโมดูลปักบอร์ด
    x = mx - 0.6 + i * 0.4
    seg((x, my - 0.85, 0.9), (x, my - 0.85, mz), 0.05, (0.8, 0.8, 0.8), metal=0.9, rough=0.3)

# ---- สายจัมป์ 4 เส้น ESP32 -> โมดูล ----
for i, col in enumerate([(0.9, 0.1, 0.1), (0.1, 0.1, 0.1), (0.95, 0.8, 0.1), (0.1, 0.7, 0.2)]):
    x0 = -2.9 + i * 0.55
    wire([np.array(p) for p in [
        (x0, -1.25, 1.4), (x0 + 0.5, -2.3, 2.7 + 0.2 * i), (1.0 + i * 0.3, -2.7, 3.3 + 0.25 * i),
        (3.6, -2.3, 2.7 + 0.2 * i), (4.1 + i * 0.18, -1.7, mz + 0.15)]], 0.09, col)

# ---- LED แดงติดสว่างบนบอร์ด (วงจรกำลังทำงาน) ----
lx, ly = 7.3, 1.3
for dx in (-0.12, 0.12):
    seg((lx + dx, ly, 0.9), (lx + dx, ly, 1.7), 0.035, (0.8, 0.8, 0.8), metal=0.9, rough=0.3)
body = trimesh.creation.cylinder(radius=0.3, height=0.5, sections=24)
body.apply_translation([lx, ly, 1.95])
add(body, (1, 0.15, 0.1), emissive=(1, 0.1, 0.05))
dome = trimesh.creation.icosphere(subdivisions=2, radius=0.3)
dome.apply_translation([lx, ly, 2.2])
add(dome, (1, 0.15, 0.1), emissive=(1, 0.1, 0.05))
wire([np.array(p) for p in [(5.6, -1.0, 1.6), (6.3, -0.1, 2.5), (7.0, 0.9, 2.1), (lx - 0.12, ly, 1.25)]],
     0.09, (0.95, 0.8, 0.1))

scene = trimesh.Scene(parts)
T = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]) @ np.diag([S, S, S, 1.0])  # Z-up cm -> Y-up m
scene.apply_transform(T)
scene.export('circuit.glb', include_normals=True)
print('parts:', len(parts), '| bounds(m):', scene.bounds.round(3).tolist())
