#!/bin/bash

server="set_url"
config="config_edit"
observe="observe"
sync="sync"
daemon="stop_daemon"
setkey="set_key"

# cd $SPC_PATH

if [ "$1" == "$server" ]
then
    python3.6 startup.py empty_json
    python3.6 startup.py set_server "$2"
elif [ "$1" == "$config" ]
then
    python3.6 startup.py config
elif [ "$1" == "$observe" ]
then
    python3.6 startup.py observe "$2"
elif [ "$1" == "$sync" ]
then
    python3.6 startup.py sync
elif [ "$1" == "$daemon" ]
then
    pid=$(ps -aux | grep "daemon.py$" | sed 's/\s\+/ /g' | cut -d' ' -f2)
    sudo kill -9 $pid
    echo Daemon Terminated
elif [ "$1" == "$setkey" ]
then
    python3.6 startup.py generate_key
else
    echo "spc $1 -- command not found. For help look at the man page"
fi

cd - > /dev/null