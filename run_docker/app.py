#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request,send_file
from subprocess import Popen, PIPE
from subprocess import check_output
import time
import subprocess
app = Flask(__name__)

@app.route('/tts', methods=["GET"])
def get_tts():
 text= request.args.get("text")
 print(text)
 seconds = time.time()
 p = ['echo',"'"+text+"'","|","${FESTIVALDIR}/bin/text2wave","-eval","festvox/goog_th_unison_cg.scm","-eval","'(voice_goog_th_unison_cg)'","-o",str(seconds).replace('.','')+".wav"]
 #print(p)
 process=Popen(' '.join(p), stdout=PIPE,stderr=PIPE,shell=True)
 output, err = process.communicate()
 print(' '.join(p))
 return send_file(str(seconds).replace('.','')+".wav", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True) 
"""
echo 'ประเทศไทย ได้ มี การ ปรับ เปลี่ยน' |${FESTIVALDIR}/bin/text2wave \
-eval festvox/goog_th_unison_cg.scm \
-eval '(voice_goog_th_unison_cg)' -o b.wav

echo 'แมว' |${FESTIVALDIR}/bin/text2wave -eval festvox/goog_th_unison_cg.scm -eval '(voice_goog_th_unison_cg)' -o b.wav
"""