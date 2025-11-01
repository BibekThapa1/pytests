#!/bin/sh

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Optional: wait for DB
wait_for_db() {
    host="$1"
    port="$2"
    timeout="${3:-30}"
    echo "Waiting for PostgreSQL on $host:$port..."

    end=$(( $(date +%s) + timeout ))
    while ! python - <<END
import socket, sys
s = socket.socket()
try:
    s.connect(("$host", $port))
except:
    sys.exit(1)
END
    do
        if [ $(date +%s) -ge $end ]; then
            echo "Timeout reached, PostgreSQL not available."
            exit 1
        fi
        sleep 1
    done
    echo "PostgreSQL is up!"
}

wait_for_db "$DATABASE_HOST" "$DATABASE_PORT"

# Run migrations if you want Celery to ensure DB is ready
python manage.py migrate

# Start Celery with whatever command is passed
exec "$@"
