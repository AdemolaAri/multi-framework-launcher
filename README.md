# Multi-framework Launcher

A multi-framework personal website mono-repo that showcases the same portfolio across multiple frameworks and runtimes. Each app (React, Vue, Angular-like, Flask, Django) provides a page with engaging content and you can switch between framework implementations using the launcher (Nginx).

Key features
- Multiple framework implementations of the same portfolio site (React, Vue, Angular-like, Flask, Django).
- Central launcher (`nginx`) that proxies to each app under paths: `/react/`, `/angular/`, `/vue/`, `/flask/`, `/django/`.
- Build and deploy workflows included (GitHub Actions) — static builds are assembled under `deploy/static` for deployment to GitHub Pages.

Quick start (Docker)
1. Build and run everything locally with Docker Compose:

   docker compose up --build

2. Open the launcher in your browser:

   http://localhost:8080

   The launcher will proxy to each app at the paths above.

Run individual apps (local development)
- React: `cd react-app && yarn install && yarn build` (or use the app's Dockerfile)
- Vue: `cd vue-app && yarn install && yarn build`
- Angular-like: see `angular-app/` for local server instructions
- Flask: `cd flask-app && pip install -r requirements.txt && python app.py`
- Django: `cd django-app && pip install -r requirements.txt && python manage.py runserver`

CI / Deployment notes
- GitHub Actions workflows build static artifacts and deploy to GitHub Pages. The static deploy workflow assembles files into `deploy/static` and the deploy action publishes that directory to the `gh-pages` branch.
- If you prefer not to commit `yarn.lock` files, the workflow can generate them during CI (this repo includes a workflow that runs `yarn install` in the app directories). Keep in mind builds may be less deterministic without committed lockfiles.
- The workflow requires write permission to push to `gh-pages` — the workflow includes `permissions: contents: write` and uses the default `GITHUB_TOKEN`.

Repository layout (top-level)
- `react-app/` — React implementation
- `vue-app/` — Vue implementation
- `angular-app/` — Angular-like implementation
- `flask-app/` — Flask implementation
- `django-app/` — Django implementation
- `nginx/` — Launcher and proxy configuration
- `.github/workflows/` — CI workflows

Contributing
- Send PRs to improve content, add frameworks, or fix build/deploy issues. If adding a new framework, add a subfolder and update the launcher Nginx config and the deploy workflow.

License
- MIT
