#!/usr/bin/env bash
nohup sudo python scan.py > out.log 2>&1 &
echo $! > /home/pi/program.pid
