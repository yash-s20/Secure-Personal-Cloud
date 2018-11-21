#!/bin/bash

server="set_url"
config="config_edit"
observe="observe"
sync="sync"
daemon="stop_daemon"

dic_file="conf.json"

if [ "$1" == "$server" ]
then
    python3.6 startup.py empty_json "$dic_file"
    python3.6 startup.py set_server "$2" "$dic_file"
fi

if [ "$1" == "$config" ]
then
    python3.6 startup.py config "$dic_file"
fi

if [ "$1" == "$observe" ]
then
    python3.6 startup.py observe "$2" "$dic_file"
fi


if [ "$1" == "$sync" ]
then
    python3.6 startup.py sync "$dic_file"
fi


if [ "$1" == "$daemon" ]
then
    pid=$(ps -aux | grep "python3.6 daemon.py$" | sed 's/\s\+/ /g' | cut -d' ' -f2)
    kill -9 $pid
    echo Daemon Terminated
fi
