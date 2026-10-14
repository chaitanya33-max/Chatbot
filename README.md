# Northstar Athletics

A responsive sports directory with separate Sports, Teams, and Players pages
and a chat assistant powered by the local Ollama model `qwen2.5:3B`.

## Run locally

1. Make sure Ollama is running and the model is installed:

   ```powershell
   ollama list
   ```

2. From this project folder, start the site:

   ```powershell
   py server.py
   ```

3. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

The built-in Python server serves the website and proxies `/api/chat` to
Ollama's `http://127.0.0.1:11434/api/chat` endpoint. It uses only the Python
standard library; no Node.js packages or third-party backend dependencies are
required.

To use another Ollama endpoint or web-server port, set `OLLAMA_URL` or `PORT`
before running `py server.py`. The model is intentionally pinned to
`qwen2.5:3B`.

## Sports data and image sources

- Football and NBA team rosters are fetched from ESPN's public JSON endpoints.
  This is a third-party, undocumented feed, not an official league API. Each
  roster entry displays the upstream season and timestamp and links to ESPN's
  player/statistics page and the team's official roster page. The roster
  response does not include statistical tables or biographies, so the site
  links those rather than estimating values.
- Cricket teams, players, rankings and fixtures link to the ICC and IPL. No
  cricket API is configured; the site does not represent linked pages as a
  locally verified live roster or invent current statistics.
- World Athletics and Yoga Alliance do not provide a public data API suitable
  for copying their profiles into this app. Their athlete/teacher directories
  are linked directly. Yoga credentials are not inferred. RIMYI's dated
  institute reference is linked to its official site.
- Portraits are looked up on Wikimedia Commons and displayed only when the
  response includes an accepted CC BY, CC BY-SA, CC0, or public-domain license.
  The image credit, license, and source page are shown next to each image. If no
  matching licensed image is found, the site uses initials instead.
- Fixture and class schedules link to their source pages. They are not
  fabricated or presented as Northstar events.

Use the official source links to verify current information. ESPN's public feed
can change or become unavailable; failed feeds are reported rather than treated
as empty or current rosters. A published deployment should use providers whose
API terms and image licences explicitly permit the intended use.
