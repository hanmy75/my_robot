#! /bin/bash
ENDPOINT="https://snowboy.kitt.ai/api/v1/train/"

############# MODIFY THE FOLLOWING #############
TOKEN=""
NAME="hotword"
LANGUAGE="ko"
AGE_GROUP="10_19"
GENDER="M"
MICROPHONE="usb microphone"
############### END OF MODIFY ##################


for i in {1..3}
do
    echo "Speak hotword within 5 sec"
    arecord --format=S16_LE --duration=5 --rate=16000 --file-type=wav $i.wav
done

WAV1=`base64 1.wav`
WAV2=`base64 2.wav`
WAV3=`base64 3.wav`
OUTFILE="$PWD/resources/hotword.pmdl"

cat <<EOF >data.json
{
"name": "$NAME",
"language": "$LANGUAGE",
"age_group": "$AGE_GROUP",
"token": "$TOKEN",
"gender": "$GENDER",
"microphone": "$MICROPHONE",
"voice_samples": [
    {"wave": "$WAV1"},
    {"wave": "$WAV2"},
    {"wave": "$WAV3"}
]
}
EOF

curl -H "Content-Type: application/json" -X POST -d @data.json $ENDPOINT > $OUTFILE

# Remove files
rm -rf *.wav data.json
