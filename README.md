# samcday.com

A single page of plain HTML, CSS and SVG. The deployable website is `public/`;
there is no generator, JavaScript framework or build step.

## Edit and preview

Edit the files in `public/`, then run:

```sh
python3 scripts/check.py
python3 -m http.server 8000 --directory public
```

Open <http://localhost:8000>. Any static web server or CDN can serve `public/`.

## GitHub Actions and Cloudflare Pages

The `Site` workflow checks each pull request and push to `main`, then saves the
ready-to-serve files as a `site` artifact. Deployment uses Cloudflare Pages Direct
Upload, project `samcday-site`, production branch `main`.

Deployments are **disabled by default**. To configure them:

1. In Cloudflare, create a custom API token with **Account → Cloudflare Pages →
   Edit**, restricted to the account containing `samcday-site`.
2. Add it directly in this GitHub repository's **Settings → Secrets and variables
   → Actions** as the repository secret `CLOUDFLARE_API_TOKEN`. Do not put the token
   in source files, chat or workflow logs.
3. In **Actions → Site → Run workflow**, select `main` and enable **Deploy to
   Cloudflare Pages** for a manual deployment.
4. Optionally add the repository variable `CLOUDFLARE_DEPLOY_ENABLED` with value
   `true` to deploy future pushes to `main` automatically. Leave it unset to keep
   deployment manual.

The workflow's Cloudflare account ID is a public identifier, not a credential.
Actions are pinned to commit SHAs and Wrangler to an exact version. The deploy
command is `wrangler pages deploy public --project-name samcday-site --branch main`.
Pull requests cannot deploy. Missing credentials stop an explicitly requested
deployment with a clear error; validation still works without credentials.

Cloudflare's [Direct Upload CI guide](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)
describes the token and deployment setup. Connecting a custom domain is a
separate hosting step; this repository does not modify DNS.
