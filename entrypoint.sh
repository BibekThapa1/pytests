#!/bin/sh

# ===============================
# Function: Wait for PostgreSQL
# ===============================
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

# ===============================
# Load environment variables
# ===============================
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# ===============================
# Wait for DB
# ===============================
wait_for_db "$DATABASE_HOST" "$DATABASE_PORT"

# ===============================
# Database migrations
# ===============================

echo "Making database migrations..."
python manage.py makemigrations

echo "Migrating database"
python manage.py migrate

echo "Collecting static files"
python manage.py collectstatic --noinput 

# ===============================
# Start server
# ===============================
echo "Starting server..."
if [ "$ENVIRONMENT" = "production" ]; then
    exec gunicorn core.wsgi:application \
        --bind 0.0.0.0:8003 \
        --workers 2 \
        --log-level=info \
        --access-logfile - \
        --error-logfile -
else
    # Development server
    echo "python -u manage.py runserver"
    exec python -u manage.py runserver 0.0.0.0:8003
fi
