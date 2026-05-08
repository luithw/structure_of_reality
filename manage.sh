#!/bin/bash
# Manage the Jekyll site and comments backend.
#
# Usage:
#   ./manage.sh start     - start jekyll (watch+serve) and comments server
#   ./manage.sh stop      - stop both
#   ./manage.sh restart   - stop + start
#   ./manage.sh rebuild   - one-shot clean rebuild of _site
#   ./manage.sh status    - show what's running
#   ./manage.sh logs [jekyll|comments]   - tail a log
#
# Env overrides:
#   JEKYLL_HOST (default 127.0.0.1)
#   JEKYLL_PORT (default 4000)
#   COMMENTS_PORT (default 8080)

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$PROJECT_ROOT/.run"
mkdir -p "$RUN_DIR"

JEKYLL_PID_FILE="$RUN_DIR/jekyll.pid"
JEKYLL_LOG="$RUN_DIR/jekyll.log"
COMMENTS_PID_FILE="$RUN_DIR/comments.pid"
COMMENTS_LOG="$RUN_DIR/comments.log"

JEKYLL_HOST="${JEKYLL_HOST:-127.0.0.1}"
JEKYLL_PORT="${JEKYLL_PORT:-4000}"
COMMENTS_PORT="${COMMENTS_PORT:-8080}"

# ── helpers ──

is_running() {
  local pid_file="$1"
  [ -f "$pid_file" ] || return 1
  local pid
  pid=$(cat "$pid_file" 2>/dev/null || echo "")
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

stop_pid_file() {
  local name="$1"
  local pid_file="$2"
  if is_running "$pid_file"; then
    local pid
    pid=$(cat "$pid_file")
    echo "Stopping $name (pid $pid)..."
    kill "$pid" 2>/dev/null || true
    for _ in $(seq 1 20); do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.25
    done
    if kill -0 "$pid" 2>/dev/null; then
      echo "  $name didn't exit, sending SIGKILL"
      kill -9 "$pid" 2>/dev/null || true
    fi
  else
    echo "$name not running."
  fi
  rm -f "$pid_file"
}

start_jekyll() {
  if is_running "$JEKYLL_PID_FILE"; then
    echo "Jekyll already running (pid $(cat "$JEKYLL_PID_FILE"))."
    return
  fi
  if ! command -v bundle >/dev/null 2>&1; then
    echo "Error: 'bundle' not found. Install Ruby + bundler first."
    exit 1
  fi
  echo "Starting Jekyll on http://$JEKYLL_HOST:$JEKYLL_PORT ..."
  cd "$PROJECT_ROOT"
  nohup bundle exec jekyll serve \
    --host "$JEKYLL_HOST" \
    --port "$JEKYLL_PORT" \
    --livereload \
    >"$JEKYLL_LOG" 2>&1 &
  echo $! >"$JEKYLL_PID_FILE"
  sleep 1
  if is_running "$JEKYLL_PID_FILE"; then
    echo "  pid $(cat "$JEKYLL_PID_FILE"), log: $JEKYLL_LOG"
  else
    echo "  Jekyll failed to start. Last log lines:"
    tail -20 "$JEKYLL_LOG" || true
    rm -f "$JEKYLL_PID_FILE"
    exit 1
  fi
}

start_comments() {
  if is_running "$COMMENTS_PID_FILE"; then
    echo "Comments server already running (pid $(cat "$COMMENTS_PID_FILE"))."
    return
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: 'python3' not found."
    exit 1
  fi
  echo "Starting comments server on http://0.0.0.0:$COMMENTS_PORT ..."
  cd "$PROJECT_ROOT"
  COMMENTS_PORT="$COMMENTS_PORT" nohup python3 comments_server.py \
    >"$COMMENTS_LOG" 2>&1 &
  echo $! >"$COMMENTS_PID_FILE"
  sleep 0.5
  if is_running "$COMMENTS_PID_FILE"; then
    echo "  pid $(cat "$COMMENTS_PID_FILE"), log: $COMMENTS_LOG"
  else
    echo "  Comments server failed to start. Last log lines:"
    tail -20 "$COMMENTS_LOG" || true
    rm -f "$COMMENTS_PID_FILE"
    exit 1
  fi
}

cmd_start() {
  start_comments
  start_jekyll
  echo
  echo "Both services up. Site: http://$JEKYLL_HOST:$JEKYLL_PORT"
}

cmd_stop() {
  stop_pid_file "Jekyll" "$JEKYLL_PID_FILE"
  stop_pid_file "Comments server" "$COMMENTS_PID_FILE"
}

cmd_restart() {
  cmd_stop
  cmd_start
}

cmd_rebuild() {
  if ! command -v bundle >/dev/null 2>&1; then
    echo "Error: 'bundle' not found. Install Ruby + bundler first."
    exit 1
  fi
  echo "Cleaning _site/ ..."
  rm -rf "$PROJECT_ROOT/_site"
  echo "Building..."
  cd "$PROJECT_ROOT"
  bundle exec jekyll build
  echo "Done. Output in _site/"
}

cmd_status() {
  for entry in "Jekyll:$JEKYLL_PID_FILE" "Comments:$COMMENTS_PID_FILE"; do
    name="${entry%%:*}"
    pid_file="${entry#*:}"
    if is_running "$pid_file"; then
      echo "$name: running (pid $(cat "$pid_file"))"
    else
      echo "$name: stopped"
    fi
  done
}

cmd_logs() {
  local target="${1:-}"
  case "$target" in
    jekyll)   tail -f "$JEKYLL_LOG" ;;
    comments) tail -f "$COMMENTS_LOG" ;;
    "")
      echo "Usage: $0 logs [jekyll|comments]"
      exit 1
      ;;
    *)
      echo "Unknown log: $target (use 'jekyll' or 'comments')"
      exit 1
      ;;
  esac
}

# ── dispatch ──

case "${1:-}" in
  start)   cmd_start ;;
  stop)    cmd_stop ;;
  restart) cmd_restart ;;
  rebuild) cmd_rebuild ;;
  status)  cmd_status ;;
  logs)    shift; cmd_logs "$@" ;;
  *)
    echo "Usage: $0 {start|stop|restart|rebuild|status|logs [jekyll|comments]}"
    exit 1
    ;;
esac
