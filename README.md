# Thai Text to Speech (Thai TTS)

*Open Source Thai Text to speech*

I build Thai text to speech from [Language Resources (Google) tools](https://github.com/google/language-resources). You can use Thai TTS in docker.

## Build

Build own Thai text to speech (Thai language) : https://github.com/wannaphongcom/tts-thai/tree/master/build_docker

## Use

### Docker

by docker :

```
docker pull wannaphong/thaitts
docker run -d -p 5000:5000 wannaphong/thaitts
```

use :

```
http://127.0.0.1:5000/tts?text=ทดสอบ ระบบ
```



Thank you VISTEC.

Thank you Google.



Wannaphong Phatthiyaphaibun

wannaphong@kkumail.com