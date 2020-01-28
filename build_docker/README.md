# สร้าง Text to Speech ภาษาไทย (และภาษาอื่น ๆ ) ง่าย ๆ ด้วยตัวคุณเอง

**Text to speech นี้เป็นโปรเจคที่ผมทำในช่วงฝึกงานที่ สำนักวิชาวิทยาศาสตร์และเทคโนโลยีสารสนเทศ (School of Information Science and Technology: IST) สถาบันวิทยสิริเมธี**

licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](http://creativecommons.org/licenses/by/4.0).

หลังจากที่ผมล้มเหลวมานับไม่ถ้วนกับ Text to speech (ก่อนหน้านี้ลองกับ Tacotron ล้มเหลว) ผมไปค้น GitHub นับหลายวัน จนไปเจอว่า Google ทำ TTS จากภาษาที่มีทรัพยากรต่ำ https://github.com/google/language-resources

เมื่อผมเข้าไปศึกษาพบว่า หลายภาษากูเกิลใช้ IPA ในการกำกับเสียงในการทำ Text to speech ผมเลยเกิดความคิด ถ้านำมาใช้กับภาษาไทยล่ะ ? ภาษาไทยเรามีข้อมูลทำ G2P ที่น้อยมาก ผมเลยนึกถึง IPA กับภาษาไทย น่าจะใช้ทดแทน G2P ภาษาไทยได้

บทความนี้ผมจะใช้ชุดข้อมูลเสียงชื่อ TSynC-1 ของเนคเทค ซึ่งเป็น CC-BY-SA-NC 3.0 ซึ่งอนุญาตให้งานได้ โดยต้องอ้างอิง ไม่ใช้ในทางการค้า

ดังนั้น Text to speech นี้ สามารถใช้งานได้เฉพาะที่ไม่ใช้เชิงการค้า หากคุณต้องการทำหรือทดลองสร้าง text to speech ทดลองทำตามบทความนี้ได้เลยครับ

**ความต้องการของบทความนี้**

- รันบน Linux
- แรมขั้นต่ำ 12 GB
- เนื้อที่ว่างมากกว่า 20 GB ขึ้นไป
- CPU 2 GHz ขึ้นไป
- สามารถรันได้ต่อเนื่องมากกว่า 6 ชั่วโมง
- Docker , python
- อินเทอร์เน็ต สำหรับติดตั้งเครื่องมือทำ Text to speech

ผมจึงศึกษารูปแบบข้อมูลที่กูเกิลใช้งาน โดยผลการศึกษาได้ข้อมูลว่ากูเกิลสร้างโฟลเดอร์เป็นรหัสภาษา เช่น ภาษา Bangla ใช้รหัส bn

สำหรับภาษาไทย เราจะสร้างโฟลเดอร์ชื่อ th ภายในประกอบไปด้วยโฟลเดอร์หลายอัน แต่อันที่เกี่ยวข้องกับ Text to speech มีดังนี้ 

- data - ใช้เก็บไฟล์ข้อมูล 
- festvox – สำหรับใช้ train tts โดยเก็บไฟล์ตั้งค่า ipa 

ภายใน data เป็นส่วนที่สำคัญ ประกอบไปด้วย 

- BUILD.bazel
- lexicon.tsv เป็นไฟล์เอาไว้บรรจุคำศัพท์ 
- prompts.tsv เป็นไฟล์กำกับว่าไฟล์อะไรพูดอะไร 

ก่อนที่เราจะไปสร้าง TTS ก่อนอื่น เรามารู้จักกับไฟล์ในโฟลเดอร์ festvox กันก่อน 

- BUILD.bazel 
- lexicon.scm - ไฟล์คำศัพท์ที่ส่งออกมาจาก data 
- phonology.json - เป็นไฟล์สำหรับใช้กำหนดการออกเสียงตามสัทวิทยา 
- txt.done.data - ไฟล์กำกับเสียงว่าพูดอะไร ส่งออกมาจาก data 

สำหรับขั้นตอนในการทำ Text to speech ค่อนข้าง Geek (**คำเตือน ถ้าคุณไม่เข้าใจ อย่าเศร้า !!!**) มีขั้นตอนมากมายกว่าจะได้ Text to speech นี้

1. โหลดข้อมูล
2. สร้างไฟล์ prompts.tsv
3. สร้าง phonology.json
4. สร้างไฟล์ lexicon.tsv
5. สร้างไฟล์ lexicon.scm และ txt.done.data
6. สร้างไฟล์ BUILD.bazel
7. ติดตั้ง Docker สำหรับทำ Text to speech ภาษาไทย
8. ทดสอบไฟล์
9. Train
10. สังเคราะห์เสียง

------

**โหลดข้อมูล**

โหลดได้ที่ https://www.nectec.or.th/corpus/index.php?league=sa สร้างโฟลเดอร์ตั้งชื่อว่า wavs ใช้เก็บไฟล์เสียง .wav แล้วทำการเปลี่ยน sample rate เสียงทั้งหมดให้เป็น 16000 Hz โดยใช้โค้ดดังนี้

```python
from subprocess import call
import glob
path_old="./wavs-old/" # โพลเดอร์เสียง
path_new="./wavs/" # โฟลเดอร์ที่ต้องการเก็บเสียงที่ผ่านการแปลง sample rate
for file in glob.glob(path_old+"*.wav"):
 call(['ffmpeg','-i',file,'-ar','16000',path_new+file.replace(path_old,'')])
```

ไฟล์กำกับข้อความ โหลดได้ที่ http://vaja.nectec.or.th/tsync_data.txt หรือ โหลดไฟล์ที่กำกับคำอ่านไว้แล้ว ได้ที่  https://gist.github.com/wannaphong/47b9b3618b2e54d88be39d5425be3795

------

**สร้างไฟล์ prompts.tsv**

เริ่มแรกให้สร้างไฟล์ prompts.tsv ขึ้นมาให้ได้ก่อน (ตัดคำให้กับข้อความที่กำกับเสียงด้วย) โดยให้มีรูปแบบดังนี้ 

ชื่อไฟล์\tข้อความที่ตัดคำโดยเว้นวรรคแต่ละคำ 

```
ชื่อไฟล์	ข้อความที่ตัดคำโดยเว้นวรรคแต่ละคำ 
```

ตัวอย่าง 

```
1_100_129_11 ผิว ชุบ เคลือบ ใน ระดับ จุลภาค จึง เรียบ ขึ้น 
```

และขึ้นบรรทัดใหม่ด้วย \n 

ผมจึงนำไฟล์ข้อมูลข้อความกำกับเสียง TSynC-1 (http://vaja.nectec.or.th/tsync_data.txt) ทำการเปลี่ยนข้อความเหล่านั้นให้กลายเป็นคำอ่าน เช่น พ.ศ. -> พอศอ ไม่ให้เหลืออักษรพิเศษหรือตัวเลข เสร็จแล้วมาตัดคำโดยใช้ PyThaiNLP และเว้นชื่อไฟล์ตามรูปแบบของ prompts.tsv

แต่ถ้าไม่อยากกำกับเอง ผมทำไว้แล้วที่ https://gist.github.com/wannaphong/47b9b3618b2e54d88be39d5425be3795 เป็นไฟล์ csv แบ่งด้วย | ประกอบด้วย ชื่อไฟล์|ข้อความ|ข้อความคำอ่าน และแปลงเป็นไฟล์ prompts.tsv ได้ด้วยโค้ด

```python
from pythainlp.tokenize import word_tokenize
import pandas as pd
file=pd.read_csv('metadata.csv',sep='|',names=['id','text','text2'])
wordall=[]
text=""
for _,i in file.iterrows():
    text+=i['id']+'	'+' '.join(word_tokenize(i['text2'].replace('"','').replace(')','').replace('(','').replace("'",'')))+'\n'
with open("prompts.tsv","w",encoding="utf-8") as f:
 f.write(text)
```

------

**สร้าง phonology.json**

ต่อมา เรามาสร้าง phonology.json ในโฟลเดอร์ festvox โดยไฟล์นี้ถือเป็นไฟล์ที่สำคัญมาก เป็นไฟล์ไว้กำหนด Phoneset หากไม่มีจะไม่สามารถสร้างการสังเคราะห์เสียงได้

phonology เป็นไฟล์ json ในเอกสารกูเกิลเรียกมันว่า "JSON Phonology" อ่านเอกสารได้ที่ https://github.com/google/language-resources/blob/master/docs/JSON_PHONOLOGY.md 

ผมกำกับ IPA ภาษาไทยลงไปในไฟล์ โดยศึกษาจากภาษาอื่น ๆ ใน GitHub ของโปรเจค จนผมได้ IPA นี้มา ด้วยท่าพิเศษ ผมศึกษาจากวิกิพีเดีย จากนั้นเอา IPA  ทีละตัวไปค้นข้อมูลว่าการออกเสียงเป็นแบบใด โทนเสียง และอื่น ๆ พอมาพวก tone และสระผสม ผมกำหนดคุณสมบัติ โดยกำหนด tone หรือ วรรณยุกต์เป็นรหัส 1 2 3 4 โดย เอก 1 โท 2 ตรี 3 จัตวา 4 แทน โดยเสียงสามัญ ผมไม่ใส่  โดยใส่ระดับเสียงวรรณยุกต์ในตอนกำกับไว้

ส่วนสระผสม ผมใส่ตำแหน่งการออกเสียงไว้ ตัวอย่างเช่น ["iaʔ","diph","front","diphthong"]

เสร็จแล้วจะได้ไฟล์ตามไฟล์ใน th/festvox

ดูไฟล์ phonology.json ได้จาก th/festvox/phonology.json

สำหรับแหล่งข้อมูลที่ผมใช้กำกับ IPA คือ https://en.wikipedia.org/wiki/Help:IPA/Thai_and_Lao

------

**สร้างไฟล์ lexicon.tsv**

เสร็จแล้วต่อมาเรามาสร้างไฟล์ lexicon.tsv ซึ่งเป็นไฟล์เอาไว้บรรจุคำศัพท์ เราจะต้องบรรจุคำศัพท์ให้ได้มากที่สุด อย่างน้อยให้ครอบคลุมทุกคำในข้อมูลที่เราจะใช้เทรนข้อความทำ text to speech ของเรา โดยมีรูปแบบดังนี้ 

```
แมว	m ɛː  w 
```

หากมีหลายพยางค์ ให้เว้นระหว่างพยางค์ด้วย . ตัวอย่างเช่น 

```
ความเลว	kʰ w aː m . l eː w 
```

หากเป็นตัวอักษรที่ไม่มีการออกเสียง ให้กำกับดังนี้

```
์	 
```

และขึ้นบรรทัดใหม่ด้วย \n 

แน่นอนว่าถ้ากำกับเองควรเสียเวลาหลายเดือน ผมจึงใช้วิธีดึง IPA ของคำมาจากวิกิพจนานุกรม ส่วนที่เหลือผมใช้ TLTK มากำกับและเช็กดูอีกรอบ รวมถึงปรับ IPA ที่ได้ให้ตรงตามที่กำหนดไว้ใน phonology.json และ IPA แต่ละตัวจะติดกัน ผมจึงสร้างตัวตัด IPA ขึ้นมา โดยใช้ newmm ของ PyThaiNLP กำหนด Dict ตามที่กำหนดไว้ใน phonology.json มาตัด แล้วแยกแต่ละเสียง IPA กัน ดูโค้ดดึง IPA จากวิกิพจนานุกรมได้ที่ https://colab.research.google.com/drive/1NdTkIBDxS7kjbK7yiIiRIzERy9hAtaZW

พอเราทำเสร็จแล้ว คำศัพท์ของเราจะต้องห้ามซ้ำกันและเรียงลำดับตามรหัส unicode เนื่องจากไม่มีวิธีง่าย ๆ ผมจึงพัฒนาเครื่องมือสำหรับใช้เรียงลำดับและลบคำศัพท์ของไฟล์ lexicon.tsv ขึ้นมา โหลดไฟล์ clean_lexicon.py ได้จากโฟลเดอร์ th/data

โดยเรียกใช้งานดังนี้ 

```
python clean_lexicon.py
```

------

**สร้างไฟล์ lexicon.scm และ txt.done.data**

จากนั้นเรามาสร้างไฟล์ lexicon.scm และ txt.done.data โดยใช้เครื่องมือที่ทางกูเกิลพัฒนาขึ้นมาบน GitHub https://github.com/google/language-resources/tree/master/festival_utils โหลดไฟล์ festival_lexicon_from_tsv.py และ festival_prompts_from_tsv.py มาไว้ในโฟลเดอร์ th ที่สร้าง เสร็จแล้วรันด้วยคำสั่ง

```
cat data/lexicon.tsv | python festival_lexicon_from_tsv.py > festvox/lexicon.scm
cat data/prompts.tsv | python festival_prompts_from_tsv.py > festvox/txt.done.data
```

------

**สร้างไฟล์ BUILD.bazel**

พอได้ไฟล์แล้ว จะนั้นเรามาสร้างไฟล์ BUILD.bazel กัน

ในโฟลเดอร์ data สร้างไฟล์ BUILD.bazel แล้วใส่โค้ดนี้ลงไป

```
exports_files([
    "lexicon.tsv",
    "prompts.tsv",
])
```

จากนั้น สร้างไฟล์ BUILD.bazel ในโฟลเดอร์ แล้วใส่โค้ดดังนี้

```
package(default_visibility = ["//visibility:public"])

load("//festival_utils:festvox.bzl", "festvox")

festvox(
    language = "th",
    phonology = "phonology.json",
)
```

------

**ติดตั้ง Docker สำหรับทำ Text to speech ภาษาไทย**

พอทุกอย่างเสร็จแล้ว ต่อไปได้เวลา train กัน เนื่องจากที่กูเกิลทำไว้ค่อนข้างติดตั้งยาก กูเกิลเลยทำ docker แต่ docker ของกูเกิลที่มีให้ ไม่ได้อัพเดตมานาน จน debian เลิกสนับสนุน os ที่กูเกิลทำไว้ใน docker ผมจึงนำ docker ของกูเกิลมาพัฒนาต่อ โดยเป็นไฟล์ Dockerfile ให้สามารถเรียกใช้งานและ build ได้ง่าย ๆ

โดย zip ไฟล์โฟลเดอร์ที่เก็บไฟล์เสียงทั้งหมด รวมกันเป็นไฟล์เดียวกัน ชื่อ wavs.zip

ส่วนโฟลเดอร์ th ให้ zip เป็น th.zip

เสร็จแล้วเอามาไว้ในโฟลเดอร์ build_docker จากนั้น เปิดคอมมาไลน์เข้าไปยังโฟลเดอร์ build_docker แล้ว build ด้วยคำสั่ง

```
sudo docker build -t tts:1 .
```

เราจะได้ container ชื่อ tts:1 พร้อมให้ train โดยผมสร้างให้มันโหลดไฟล์เข้าไปและตั้งค่า path ให้

รันด้วยคำสั่ง

```
docker run -it tts:1
```

หากไม่ต้องการรันด้วย docker จะต้องทำตามขั้นตอนดังนี้ (แนะนำให้ใช้ docker ดีกว่าติดตั้งเอง)

clone https://github.com/google/language-resources มา แล้วรันคำสั่ง ./festival_utils/setup_festival.sh

ตั้งค่า path ให้เรียบร้อย

```
export FESTIVAL_SUIT_PATH=<your desired path to install Festival>
```

เอาโฟลเดอร์ th ไปไว้ในโฟลเดอร์ language-resources จากนั้น เอาโฟลเดอร์เสียงไปไว้ แล้วตั้งค่า path

```
export WAV_FOLDER=<your desired path to store downloaded wav files>
```

และตั้งค่า path output TTS ที่ต้องการ

```
export OUTPUT_VOICE_FOLDER=<your desired path to store output voice>
```

แต่ระวัง ช่วงติดตั้งอาจจะมีปัญหาไม่สามารถรันได้ (ใช้ docker ที่จัดเตรียมไว้สะดวกและง่ายกว่าเยอะ)

รายละเอียดเพิ่มเติม https://github.com/google/language-resources/tree/master/bn/festvox

------

**ทดสอบไฟล์**

ว่าสามารถ build ได้หรือไม่

- Lexicon - ```bazel build //th/festvox:make_lexicon_scm```
- Festival prompts -  ```bazel build //th/festvox:make_festvox_prompts```

------

**Train**

รอประมาณ 6 ชั่วโมง โดยใช้คำสั่ง

```
./festival_utils/build_festvox_voice.sh ${WAV_FOLDER} th ${OUTPUT_VOICE_FOLDER}
```

------

**สังเคราะห์เสียง**

หลังจากที่ train เสร็จสิ้น มาลองสังเคราะห์เสียงด้วยคำสั่ง 

```
cd ${OUTPUT_VOICE_FOLDER}
echo 'ประเทศไทย ได้ มี การ ปรับ เปลี่ยน' |${FESTIVALDIR}/bin/text2wave -eval festvox/goog_th_unison_cg.scm -eval '(voice_goog_th_unison_cg)' -o a.wav 
```

เมื่อรันเสร็จจะได้ไฟล์ a.wav แล้วลองฟัง

ถ้าได้ยินเสียง ยินดีด้วยครับ คุณเพิ่งสร้าง text to speech ด้วยตัวเองสำเร็จ !!! (ผมทำเสร็จวันที่ 30 มิถุนายน 2562 พอดี ตอนนั้นดีใจและตื่นเต้นมาก หลังจากล้มเหลวมาหลายสัปดาห์)

------

### ทำไมเสียงที่ได้จึงเพี้ยน

แน่นอน เสียงที่ได้มา หากจะยังไม่ถูกใจ แนะนำให้ลองอัดเสียง โดยอัดเสียงตามข้อความในคลัง และเพิ่มเติมคำศัพท์พร้อมข้อความเข้าไปด้วย หากไม่มีคำในคลังคำศัพท์ อาจจะมีข้อผิดพลาดไม่สามารถสังเคราะห์เสียงได้

โดยสเปคไฟล์เสียงที่ต้องการ sample rate ต้องเป็น 16000 Hz จึงจะเหมาะสม (ถ้าเกินให้ลด sample rate ลงมา)  และนามสกุลไฟล์จะต้องเป็น .wav

ส่วนชุดข้อมูล TSynC-1 ของเนคเทค ที่เราใช้ในบทความนี้ มี sample rate เป็น 8000 Hz ทำให้ผมต้องเพิ่ม sample rate เข้าไปให้เป็น 16000 Hz เพราะถ้าใช้ sample rate เป็น 8000 Hz เสียงจะเพี้ยนมากจนฟังไม่รู้เรื่อง และข้อมูลเสียงยังไม่มาก ไม่ครอบคลุมคำบางโดเมน เพราะ ชุดข้อมูล TSynC-1 อยู่ในโดเมนบทความวิชาการ สารานุกรม ถ้าจะทำจริง ต้องให้หลากหลายโดเมน แถมเรายังไม่ได้ปรับปรุงโมเดลเสียง

นอกจากนั้น เราสามารถปรับปรุงคุณภาพของเสียงได้ โดยทำตามเอกสารที่กูเกิลทำไว้ที่ https://sites.google.com/site/sltututorial/tutorial

ส่วนโมเดลเสียงเราใช้ Hidden Markov Model-based speech synthesis (HMM) ในการทำ text to speech และในเอกสารของกูเกิลมีสอนทำ Text to speech ด้วย Merlin TTS หากสนใจเข้าไปศึกษาได้จาก https://github.com/google/language-resources

------

หากท่านใดทำ text to speech อย่าลืมส่ง pull request กลับมาให้ PyThaiNLP เพื่อพัฒนา text to speech ภาษาไทยกันต่อไปครับ (เรายังต้องการผู้ร่วมพัฒนาและผู้บริจาคเสียง !!!)



ขอขอบคุณสถาบันวิทยสิริเมธี

ขอขอบคุณกูเกิล สำหรับโปรเจคดี ๆ ที่เผยแพร่แก่สาธารณะ

ขอขอบคุณเนคเทคสำหรับชุดข้อมูลเสียง



วรรณพงษ์ ภัททิยไพบูลย์

wannaphong@kkumail.com

นักศึกษา สาขาวิทยาการคอมพิวเตอร์และสารสนเทศ

คณะวิทยาศาสตร์ประยุกต์และวิศวกรรมศาสตร์

มหาวิทยาลัยขอนแก่น วิทยาเขตหนองคาย

------

### แหล่งอ้างอิง

- Language Resources and Tools - Google https://github.com/google/language-resources
- How to build phonology.json (consonant , vowel , tone marke) with IPA? - https://github.com/google/language-resources/issues/14
- I can't train thai language. - https://github.com/google/language-resources/issues/25
- SLTU 2016 Tutorial - https://sites.google.com/site/sltututorial/overview
- Text Normalization for Bangla, Khmer, Nepali, Javanese, Sinhala, and Sundanese TTS Systems - https://ai.google/research/pubs/pub47344
- A Step-by-Step Process for Building TTS Voices Using Open Source Data and Framework for Bangla, Javanese, Khmer, Nepali, Sinhala, and Sundanese - https://ai.google/research/pubs/pub47347
