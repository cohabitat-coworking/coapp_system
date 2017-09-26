NAME="coapp_system"
LOGFILE=/root/coapp_system/coapp_system/log/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
DJANGO_WSGI_MODULE=coapp_system.wsgi

USER=root
GROUP=sudo
IP=0.0.0.0
PORT=8001

echo "Starting $NAME"

cd /root/coapp_system
source /root/coappenv/bin/activate
source /root/coapp_system/sendgrid.env

test -d $LOGDIR || mkdir -p $LOGDIR

exec gunicorn ${DJANGO_WSGI_MODULE} \
 --name $NAME \
 --workers $NUM_WORKERS \
 --user=$USER --group=$GROUP \
 --log-level=debug \
 --bind=$IP:$PORT
 --log-file=$LOGFILE 2>>$LOGFILE