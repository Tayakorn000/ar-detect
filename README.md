# AR Detect

เปิดกล้องแล้วตีกรอบวัตถุเรียลไทม์แบบ YOLO detect — HTML ไฟล์เดียว ไม่ต้อง build

## รัน

```bash
python3 -m http.server 8787
# เปิด http://localhost:8787 แล้วกด Allow กล้อง
```

มือถือต้องเข้าผ่าน HTTPS (กล้องใช้ได้เฉพาะ secure context) เช่น Tailscale funnel หรือ ngrok

## โหมด

- **เร็ว (80 ชนิด)** — COCO-SSD (tfjs) เรียลไทม์ ป้ายภาษาไทย
- **พิมพ์เอง 🐢** — OWLv2 zero-shot (transformers.js) พิมพ์ชื่อของที่อยากหาเอง คั่นด้วยจุลภาค พิมพ์ไทยได้ (เช่น `ปลั๊กไฟ, esp32, raspberry pi`) โหลดครั้งแรก ~200MB ช้าระดับวินาทีต่อเฟรม

โมเดลโหลดจาก CDN — ต้องมีเน็ต

## เทส

```
http://localhost:8787/?img=test.jpg                 # โหมด COCO
http://localhost:8787/?img=pi.jpg&labels=pi,บอร์ด    # โหมด zero-shot
```

ผลออกทาง console เป็น `TEST_RESULT [...]`

## เครดิตรูปเทส

- `test.jpg` — จาก [ultralytics/yolov5](https://github.com/ultralytics/yolov5) sample images
- `pi.jpg` — Raspberry Pi 4 Model B, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Raspberry_Pi_4_Model_B_-_Side.jpg)
