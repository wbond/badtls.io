#!/usr/bin/env bash

NGINX=$(which nginx)
if [[ !$NGINX ]]; then
    for n in "/usr/local/nginx/sbin/nginx" "/opt/nginx/sbin/nginx" "/usr/local/sbin/nginx" "/usr/sbin/nginx"; do
        if [[ -x $n ]]; then
            NGINX=$n
            break
        fi
    done
fi

if [[ $NGINX == "" ]]; then
    >&2 echo "nginx could not be found"
    exit 1
fi

SOCAT=$(which socat)
if [[ $SOCAT == "" ]]; then
    >&2 echo "socat could not be found"
    exit 2
fi

$NGINX -p ./nginx &
NGINX_PID=$!

sleep 0.5

$SOCAT tcp:localhost:9990 openssl-listen:10003,reuseaddr,fork,cipher=EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH:DES-CBC3-SHA,cert=./certs/auth.crt,key=./certs/host.key,dhparam=./certs/dhparam.pem,cafile=./certs/ca.crt,verify=1 &
SOCAT_PID=$!

wait

cleanup() {
    kill $NGINX 2> /dev/null
    kill $SOCAT_PID 2> /dev/null
}

trap 'cleanup' 1 2 3 15 EXIT
