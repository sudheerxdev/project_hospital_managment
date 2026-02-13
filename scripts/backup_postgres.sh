#!/bin/sh
set -e

BACKUP_DIR=${BACKUP_DIR:-/backups}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ]; then
  echo "POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD must be set"
  exit 1
fi

export PGPASSWORD="$POSTGRES_PASSWORD"
pg_dump -h "${POSTGRES_HOST:-localhost}" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_DIR/hotel_backup_${TIMESTAMP}.sql"
echo "Backup written to $BACKUP_DIR/hotel_backup_${TIMESTAMP}.sql"
