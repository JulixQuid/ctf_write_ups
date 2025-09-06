#!/bin/bash
HOST="the-bear-5bbdfa6610ef854b.challs.tfcctf.com"
PORT=1337
OUTFILE="output2.txt"

# Number of times to send "1"
SAMPLES=624
sleep 3
{
  for ((i=0; i<$SAMPLES; i++)); do
    echo "1"
    sleep 0.1
  done
  echo "2"
  sleep 1
} | ncat --ssl $HOST $PORT | tee $OUTFILE
#ncat --ssl the-bear-5bbdfa6610ef854b.challs.tfcctf.com 1337
