#!/bin/bash
set -e

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "=== SCAMEATER Backup ==="

# Backup PostgreSQL
echo "Backing up PostgreSQL..."
docker exec scameater-db pg_dump -U ${DB_USER} ${DB_NAME} > "$BACKUP_DIR/db.sql"

# Backup MinIO audio files
echo "Backing up audio files from MinIO..."
docker run --rm --network scameater_net \
    -e MINIO_ENDPOINT=minio:9000 \
    -e MINIO_ACCESS_KEY=${MINIO_USER} \
    -e MINIO_SECRET_KEY=${MINIO_PASSWORD} \
    minio/mc:latest \
    mc alias set local http://minio:9000 ${MINIO_USER} ${MINIO_PASSWORD} 2>/dev/null || true
docker run --rm --network scameater_net \
    -v "$BACKUP_DIR/audio:/backup/audio" \
    minio/mc:latest \
    mc cp --recursive local/call-recordings/ /backup/audio/ 2>/dev/null || true

# Backup Redis
echo "Backing up Redis..."
docker exec scameater-redis redis-cli -a ${REDIS_PASSWORD} SAVE > /dev/null
docker cp scameater-redis:/data/dump.rdb "$BACKUP_DIR/redis.rdb" 2>/dev/null || true

echo "Backup complete: $BACKUP_DIR"