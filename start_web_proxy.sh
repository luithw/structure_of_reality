#!/usr/bin/env bash
set -u

log() {
  echo "[start_web_proxy] $*" >&2
}

# Detect whether _site/ is stale compared to _posts/ using newest mtime.
# If newest(_posts) > newest(_site), we treat _site as stale.
read -r STALE NEWEST_POSTS NEWEST_SITE < <(python3 - <<'PY'
from pathlib import Path

def newest_mtime(p: Path):
    latest = None
    if not p.exists():
        return None
    for f in p.rglob('*'):
        if f.is_file():
            m = f.stat().st_mtime
            if latest is None or m > latest:
                latest = m
    return latest

posts_dir = Path('_posts')
site_dir = Path('_site')

new_posts = newest_mtime(posts_dir)
new_site = newest_mtime(site_dir)

stale = (new_site is None) or (new_posts is None) or (new_posts > new_site)

def to_int(x):
    return int(x) if x is not None else -1

print(int(stale), to_int(new_posts), to_int(new_site))
PY
)

if [ "$STALE" -eq 1 ]; then
  log "_site/ looks STALE vs _posts/ (newest_posts_mtime=${NEWEST_POSTS}, newest_site_mtime=${NEWEST_SITE})."

  if command -v bundle >/dev/null 2>&1; then
    log "bundle detected; attempting rebuild (best-effort): bundle exec jekyll build"
    if bundle exec jekyll build; then
      log "Rebuild succeeded."
    else
      rc=$?
      log "WARNING: Rebuild failed (exit_code=${rc}); starting anyway (may serve stale content)."
    fi
  else
    log "WARNING: 'bundle' not found; skipping rebuild and starting anyway (may serve stale content)."
  fi
else
  log "_site/ appears fresh vs _posts/ (newest_posts_mtime=${NEWEST_POSTS}, newest_site_mtime=${NEWEST_SITE}); skipping rebuild."
fi

log "Starting web_proxy.py"
exec python3 web_proxy.py
