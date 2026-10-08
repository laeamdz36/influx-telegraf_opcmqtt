#!/usr/bin/env bash
# Elimina los archivos WAL de 0 bytes que deja un corte de energia en InfluxDB 3 Core.
# Esos archivos provocan el error "persist a WAL file that already exists" al arrancar.
# Ver docs/README.md -> "Troubleshooting: InfluxDB 3 Core WAL Crash After Power Outage".
#
# Variables:
#   INFLUXDB3_DATA_DIR  Ruta del data-dir DENTRO del contenedor (default: /var/lib/influxdb3/data)
#   INFLUXDB3_NODE_ID   Debe coincidir con --node-id de influxdb3 serve (default: node0)
#   WAL_CLEAN_DRY_RUN   "true" para solo listar los archivos sin borrarlos (default: false)

set -Eeuo pipefail

DATA_DIR="${INFLUXDB3_DATA_DIR:-/var/lib/influxdb3/data}"
NODE_ID="${INFLUXDB3_NODE_ID:-node0}"
WAL_DIR="${DATA_DIR}/${NODE_ID}/wal"
DRY_RUN="${WAL_CLEAN_DRY_RUN:-false}"

log() { printf '%s [clean-wal] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

trap 'log "ERROR en linea ${LINENO}: ${BASH_COMMAND}"' ERR

if [[ ! -d "$WAL_DIR" ]]; then
  log "No existe ${WAL_DIR} (primer arranque o node-id distinto). Nada que limpiar."
  exit 0
fi

# Solo archivos *.wal vacios del directorio WAL del nodo, sin recorrer subdirectorios.
find_empty_wal() {
  find "$WAL_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.wal' -empty "$@"
}

count="$(find_empty_wal -printf '.' | wc -c)"

if (( count == 0 )); then
  log "Sin archivos WAL de 0 bytes en ${WAL_DIR}."
  exit 0
fi

if [[ "$DRY_RUN" == "true" ]]; then
  log "DRY RUN: ${count} archivo(s) WAL de 0 bytes que se eliminarian:"
  find_empty_wal -print
  exit 0
fi

log "Eliminando ${count} archivo(s) WAL de 0 bytes en ${WAL_DIR}:"
find_empty_wal -print -delete
log "Limpieza completada."
