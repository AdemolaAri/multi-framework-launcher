
# Multi-Framework Launcher — Embed Apps with iframes via nginx proxy

This repo contains a launcher page (`launcher/index.html`) that embeds five framework apps (React, Angular, Vue, Flask, Django) through iframes using a reverse proxy (`nginx`). The launcher assumes each app is reachable through nginx paths:

- `/react/`  → proxied to React app (default internal: react:3000)
- `/angular/` → proxied to Angular app (internal: angular:4200)
- `/vue/` → proxied to Vue app (internal: vue:5173)
- `/flask/` → proxied to Flask app (internal: flask:5000)
- `/django/` → proxied to Django app (internal: django:8000)

## Quick start (Docker Compose)

1. Build or run your framework apps as Docker services with names matching the compose file (`react`, `angular`, `vue`, `flask`, `django`) **OR** update `nginx/nginx.conf` to proxy to the correct host:port for each service.
2. Start the launcher (and placeholders) with:
   ```bash
   docker compose up
   ```
   This will start `nginx` on port `8080` and several placeholder static containers. Open `http://localhost:8080` to view the launcher.

3. Replace the placeholder services in `docker-compose.yml` with your actual application services (or run your dev servers on the ports listed and adjust compose / nginx accordingly).

## Why use nginx proxy?

Modern dev servers often set `X-Frame-Options` or other headers that prevent embedding in iframes. By proxying each app under the same origin (the nginx host) and letting nginx set a permissive `X-Frame-Options: SAMEORIGIN`, you avoid modifying each dev server's headers and enable embedding securely.

## Enabling embedding without nginx (alternative)

If you don't want to use nginx and prefer to run dev servers directly, you must configure each dev server to allow framing:

- **Vite (React / Vue)**: in `vite.config.js`:
```js
export default {
  server: {
    host: true,
    port: 3001,
    headers: {
      'X-Frame-Options': 'ALLOWALL'
    }
  }
}
```
(Repeat for other Vite instances with their ports.)

- **Angular CLI (`ng serve`)**:
Angular CLI doesn't expose header settings directly. Use a local reverse proxy (nginx) or configure your dev machine's web server for proxying.

- **Flask**: in your Flask app, set a response header:
```py
from flask import Flask, after_this_request

app = Flask(__name__)

@app.after_request
def set_frame_options(response):
    response.headers.pop('X-Frame-Options', None)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
```

- **Django**: in `settings.py`:
```py
X_FRAME_OPTIONS = 'SAMEORIGIN'
# or to allow all framing (not recommended):
# X_FRAME_OPTIONS = None
```

## Notes & tips

- Serving under the same origin (same host and port) is the simplest approach for embedding and for avoiding many CORS/X-Frame issues.
- If you host the apps remotely, update the `nginx` proxy to point to the correct upstream hosts.
- The launcher's quick links open each app path in a new tab, useful when debugging the app directly.
- The included placeholder images/resume are minimal. Replace `shared/assets/` with your real assets.

## Structure

- `launcher/index.html` — the main launcher page (iframe tab UI).
- `nginx/nginx.conf` — nginx proxy config used by compose.
- `docker-compose.yml` — starts nginx + placeholder services.
- `shared/` — contains `content.json` and placeholder `assets/`.

## Next steps I can help with:
- Replace placeholders with the full per-framework codebases (React, Angular, Vue, Flask, Django) and produce a ready-to-run multi-service docker-compose that builds each.
- Create a single-page "embedder" that lazy-loads apps only when selected.
- Add auth, session sync, or postMessage-based communication between launcher and iframe apps.

