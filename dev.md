# เอกสารการพัฒนา

เราทำตามเอกสารที่ Google แนะนำไว้ใน https://sites.google.com/site/sltututorial/tutorial โดยใช้ https://github.com/googlei18n/language-resources เป็นเครื่องมือสำหรับสร้าง TTS ภาษาไทย

## ไฟล์ lexicon.scm

เป็นไฟล์สำหรับกำหนด G2P ของคำที่รับเข้ามาในระบบ โดยขึ้นอยู่กับจำนวนพยางค์

("ไง" nil (((aɪ ŋ) 1)))

โดย 0 or 1 is the stress level ส่วน () ใส่ตามจำนวนพยางค์ให้ครบทุกอัน
