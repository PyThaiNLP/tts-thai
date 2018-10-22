# เอกสารการพัฒนา

เราทำตามเอกสารที่ Google แนะนำไว้ใน https://sites.google.com/site/sltututorial/tutorial โดยใช้ https://github.com/googlei18n/language-resources เป็นเครื่องมือสำหรับสร้าง TTS ภาษาไทย

## ไฟล์ lexicon.scm

เป็นไฟล์สำหรับกำหนด G2P ของคำที่รับเข้ามาในระบบ โดยขึ้นอยู่กับจำนวนพยางค์

```scheme
("ไง" nil (((aɪ ŋ) 1)))
```

โดย 0 or 1 is the stress level ส่วน () ใส่ตามจำนวนพยางค์ให้ครบทุกอัน

## ไฟล์ phonology.json

เป็นไฟล์สำหรับใช้กำหนดการออกเสียงตามสัทวิทยา ตามเอกสารใน https://github.com/googlei18n/language-resources/blob/master/docs/JSON_PHONOLOGY.md

## ไฟล์ txt.done.data

เป็นไฟล์สำหรับเก็บข้อความจากเสียง โดยต้องแยกคำด้วยทุกคำตามที่ปรากฎในไฟล์ lexicon.scm

```
( ban_00737_00028634754 "สวัสดี ท่าน ผู้ชม" )
```
