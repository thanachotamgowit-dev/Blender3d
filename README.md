# Blender3d - Modern House BIM / BOQ Workflow

โปรเจกต์ตัวอย่างบ้านชั้นเดียว **Modern Box House 10 x 10 m (100 m²)** สำหรับ workflow:

**JSON specification -> Blender 3D -> GLB/Web Viewer -> IFC/BOQ extension**

## สิ่งที่มีใน branch นี้

- `spec/house_10x10.json` - ค่าพารามิเตอร์หลักของบ้าน
- `blender/build_house.py` - สร้างโมเดล Blender แบบ procedural
- `boq/export_boq.py` - ถอดปริมาณแนวคิดเป็น CSV
- `web/` - Three.js viewer สำหรับหมุน/ซูมโมเดล
- `.github/workflows/build.yml` - สร้าง `.blend`, `.glb`, และ `boq.csv` อัตโนมัติ

## โครงสร้างโมเดล

โมเดล Blender แยก Collection เป็น:

1. Footings
2. Foundation Beams
3. Columns
4. Slabs
5. Walls
6. Doors / Windows
7. Roof

โครงสร้างนี้ตั้งใจให้ต่อยอดไป BIM, IFC และ BOQ ได้ง่ายกว่าการทำโมเดลเป็นชิ้นเดียว

## รันบนเครื่อง

ต้องมี Blender และ Python:

```bash
python boq/export_boq.py --spec spec/house_10x10.json --output dist/boq.csv

blender --background --python blender/build_house.py -- \
  --spec spec/house_10x10.json --output-dir dist
```

ผลลัพธ์หลัก:

- `dist/house_10x10.blend`
- `dist/house_10x10.glb`
- `dist/boq.csv`

## SketchUp

GLB เหมาะสำหรับ web viewer และการแลกเปลี่ยนโมเดลทั่วไป ส่วนการนำเข้า SketchUp อาจต้องใช้รูปแบบที่รุ่น SketchUp ของคุณรองรับหรือแปลงผ่าน Blender เป็น OBJ/DAE ก่อน

## ข้อจำกัด

ค่าฐานราก เสา คาน แผ่นพื้น และปริมาณใน BOQ เป็น **concept / teaching values** เท่านั้น ไม่ใช่แบบคำนวณโครงสร้าง แบบก่อสร้าง หรือปริมาณสำหรับประมูล ต้องตรวจสอบโดยวิศวกรและผู้ออกแบบก่อนใช้งานจริง
