#!/bin/zsh
PARAMS="-h 192.168.0.2 -P password"
PORT="/dev/ttyUSB0"
CHARS=39

stty -F $PORT 2400
echo -ne "\x1F\x14" > $PORT
#while sleep 1;	do echo -ne "\x10\x00$(printf "%-40s%s" "$(date)")$(printf "%-39s%s" "$(mpc $PARAMS current)")" > $PORT ; done

POS=0
while sleep 1
do
    TIME=$(date)
    echo "${$(mpc -h 192.168.0.2 -P password current):$POS:$CHARS}"
    #printf "\x10\x00%-40s%s%s" "$TIME" "$SONG" > $PORT
done
