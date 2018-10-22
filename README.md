# Setting up Thai TTS

## Festvox Environment

Run the following command (This should be executed while in the cloned language-resources folder)

```
export FESTIVAL_SUIT_PATH=<your desired path to install Festival>
mkdir ${FESTIVAL_SUIT_PATH} && ./third_party/festvox/setup.sh
```

## Preparing the data

- Lexicon - ```bazel build //th/festvox:make_lexicon_scm```
- Festival prompts -  ```bazel build //th/festvox:make_txt_done_data ```


## Training the Voice 

1. Download recordings from ____
  ```
  export WAV_FOLDER=<your desired path to store downloaded wav files>
  mkdir -p ${WAV_FOLDER} && wget _____ && tar xzf th.tar.gz -C ${WAV_FOLDER}
  ```

2. The setup script from 1) would give out instruction to put export commands under bash.
Please follow them strictly or always export them by yourself before running the next step.

3. Train TTS Voice (This should be executed while in the cloned language-resources folder).
This step will take couple of hours to finish.

  ```
  export OUTPUT_VOICE_FOLDER=<your desired path to store output voice>
  ./festival_utils/build_festvox_voice.sh ${WAV_FOLDER} af ${OUTPUT_VOICE_FOLDER}
  ```

4. Synthesize one example sentence (This always needs to be run from the produced output voice directory).

  ```
    cd ${OUTPUT_VOICE_FOLDER}
    echo 'hoeveel geld het sy nou en'|
    ${FESTIVALDIR}/bin/text2wave \
      -eval festvox/goog_af_unison_cg.scm \
      -eval '(voice_goog_af_unison_cg)' \
      > example.wav
  ```
