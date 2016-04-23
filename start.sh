#!/bin/bash 

diango_server='myweb/manage.py'
websocket_server='websocket_server/WebSocket_Server.py'

case $1 in
    start)
        python $diango_server runserver 0.0.0.0:8080 >/dev/null &
        python $websocket_server >/dev/null &
        [ $? -eq 0 ] && echo "Start success!" || \
            echo "Start fail!"
    ;;

    stop)
        PID=`ps -ef | grep -v grep | egrep 'manage.py|WebSocket_Server.py' | awk '{print $2}'`
        [ -n "$PID" ] && kill -9 $PID && echo "Stop done!" || echo 'Websocket Has been stoped!'
    ;;

    restart)
        
    ;;
    
    *)
        
    ;;
esac
