import json
import html
import mimetypes
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urlsplit
from urllib.request import Request, urlopen

from sports_data import DIRECTORIES, REFERENCE_CHECKED, REFERENCE_PLAYERS, SPORTS, TEAMS


ROOT = Path(__file__).resolve().parent
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL = "qwen2.5:3B"
SYSTEM_PROMPT = (
    "You are Northstar Assist, the friendly and inclusive sports-club guide for "
    "Northstar Athletics. Help people choose a sport, prepare for a first session, "
    "and navigate the website's football, running, basketball, yoga, and cricket "
    "directories. Be warm, "
    "encouraging, concise, and practical. Do not claim to make bookings or know "
    "real-time class availability. Never invent current "
    "rosters, affiliations, statistics, results, fixtures, or yoga credentials. "
    "For current sports facts, direct people to the Players, Teams, or Sports pages "
    "and their linked sources. The website does not publish membership contact "
    "details; do not invent them."
)
MAX_BODY_BYTES = 64 * 1024
MAX_MESSAGES = 24
MAX_MESSAGE_LENGTH = 4000
ESPN_API = "https://site.api.espn.com/apis/site/v2/sports"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
CACHE_SECONDS = 300
_cache = {}
_cache_lock = threading.Lock()


def _cached_json(url):
    now = datetime.now(timezone.utc).timestamp()
    with _cache_lock:
        cached = _cache.get(url)
        if cached and cached["expires"] > now:
            return cached["value"]

    request = Request(
        url,
        headers={"User-Agent": "NorthstarAthletics/1.0 (local sports directory)"},
    )
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise URLError(f"Upstream returned HTTP {response.status}")
        data = response.read(5 * 1024 * 1024 + 1)
    if len(data) > 5 * 1024 * 1024:
        raise ValueError("Upstream response exceeded the 5 MB limit.")
    value = json.loads(data)
    with _cache_lock:
        _cache[url] = {"expires": now + CACHE_SECONDS, "value": value}
    return value


def _official_country(value, birthplace=None):
    country_codes = {
        "ARG": "Argentina", "AUS": "Australia", "BRA": "Brazil",
        "CAN": "Canada", "ENG": "England", "ESP": "Spain",
        "FRA": "France", "GER": "Germany", "IND": "India",
        "JAM": "Jamaica", "KEN": "Kenya", "NED": "Netherlands",
        "NOR": "Norway", "NZL": "New Zealand", "POR": "Portugal",
        "SCO": "Scotland", "SEN": "Senegal", "USA": "United States",
        "US": "United States", "UNITED STATES OF AMERICA": "United States",
        "WAL": "Wales",
    }
    if isinstance(value, str) and value:
        return country_codes.get(value.upper(), value)
    if isinstance(birthplace, dict):
        country = birthplace.get("country")
        if isinstance(country, str) and country:
            return country_codes.get(country.upper(), country)
    return None


def _roster_url(team):
    if team["sport"] == "Basketball":
        return f"{ESPN_API}/basketball/nba/teams/{team['espn_id']}/roster"
    return f"{ESPN_API}/soccer/{team['league_slug']}/teams/{team['espn_id']}/roster"


def _roster_record(team):
    url = _roster_url(team)
    try:
        payload = _cached_json(url)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as error:
        return {
            "team_id": team["id"],
            "error": f"Could not retrieve the ESPN roster: {error}",
        }

    source_timestamp = payload.get("timestamp")
    source_season = payload.get("season", {}).get("displayName")
    if not isinstance(payload.get("athletes"), list):
        return {
            "team_id": team["id"],
            "error": "The ESPN response did not include a roster.",
            "retrieved_at": source_timestamp,
        }

    roster = []
    for athlete in payload["athletes"]:
        if not isinstance(athlete, dict) or not isinstance(athlete.get("fullName"), str):
            continue
        links = athlete.get("links", [])
        profile_url = None
        stats_url = None
        if isinstance(links, list):
            for link in links:
                if not isinstance(link, dict) or not isinstance(link.get("href"), str):
                    continue
                relations = link.get("rel", [])
                if isinstance(relations, list):
                    if "stats" in relations and link["href"].startswith("https://www.espn.com/"):
                        stats_url = stats_url or link["href"]
                    if (
                        ("playercard" in relations or "overview" in relations)
                        and link["href"].startswith("https://www.espn.com/")
                    ):
                        profile_url = profile_url or link["href"]
        position = athlete.get("position")
        if isinstance(position, dict):
            position = position.get("displayName")
        birthplace = athlete.get("birthPlace")
        roster.append(
            {
                "id": str(athlete.get("id", athlete["fullName"])),
                "name": athlete["fullName"],
                "sport": team["sport"],
                "team_id": team["id"],
                "team": team["name"],
                "position": position if isinstance(position, str) else None,
                "number": str(athlete["jersey"]) if athlete.get("jersey") else None,
                "country": _official_country(athlete.get("citizenship"), birthplace),
                "profile_url": profile_url,
                "stats_url": stats_url,
                "season": source_season,
                "updated_at": source_timestamp,
                "source_url": url,
                "source_label": "ESPN public roster feed",
            }
        )
    return {
        "team_id": team["id"],
        "season": source_season,
        "retrieved_at": source_timestamp,
        "roster": roster,
        "source_url": url,
    }


def _sports_catalog():
    teams = []
    rosters = {}
    errors = []
    live_teams = [team for team in TEAMS if "espn_id" in team]

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_teams = {executor.submit(_roster_record, team): team for team in live_teams}
        for future in as_completed(future_teams):
            record = future.result()
            rosters[record["team_id"]] = record
            if "error" in record:
                errors.append(
                    {
                        "team": future_teams[future]["name"],
                        "message": record["error"],
                    }
                )

    for configured_team in TEAMS:
        team = dict(configured_team)
        record = rosters.get(team["id"])
        if record:
            team.update(
                {
                    "feed_status": "live" if "roster" in record else "unavailable",
                    "season": record.get("season"),
                    "updated_at": record.get("retrieved_at"),
                    "roster": record.get("roster", []),
                    "source_url": record.get("source_url"),
                    "error": record.get("error"),
                }
            )
        else:
            team.update(
                {
                    "feed_status": "official-link-only",
                    "season": None,
                    "updated_at": None,
                    "roster": [],
                    "source_url": team["official_url"],
                    "error": None,
                }
            )
        teams.append(team)

    players_by_key = {}
    for record in rosters.values():
        for player in record.get("roster", []):
            players_by_key[(player["sport"], player["id"])] = player
    players = list(players_by_key.values())

    featured = []
    for reference in REFERENCE_PLAYERS:
        player = dict(reference)
        matched = next(
            (
                current
                for current in players
                if current["name"].casefold() == player["name"].casefold()
                and current["sport"] == player["sport"]
            ),
            None,
        )
        if matched:
            matched["featured"] = True
            matched["status"] = "live-roster"
            continue
        elif player["sport"] in ("Football", "Basketball"):
            player["status"] = "not-in-selected-live-rosters"
            player["updated_at"] = datetime.now(timezone.utc).isoformat()
            player["source_label"] = "ESPN selected-team roster feeds"
        player["featured"] = True
        featured.append(player)

    all_players = players + featured
    all_players.sort(key=lambda player: (
        not player.get("featured", False),
        player["sport"],
        player["name"].casefold(),
    ))
    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "reference_checked": REFERENCE_CHECKED,
        "sports": SPORTS,
        "teams": teams,
        "players": all_players,
        "directories": DIRECTORIES,
        "errors": errors,
    }


def _clean_metadata(value):
    if not isinstance(value, str):
        return ""
    return html.unescape(re.sub(r"<[^>]*>", "", value)).strip()


def _commons_image(name):
    search = quote(f'filetype:bitmap "{name}"')
    url = (
        f"{COMMONS_API}?action=query&format=json&generator=search&gsrnamespace=6"
        f"&gsrlimit=10&gsrsearch={search}&prop=imageinfo"
        "&iiprop=url%7Cextmetadata&iiurlwidth=600"
    )
    payload = _cached_json(url)
    pages = payload.get("query", {}).get("pages", {})
    wanted = [part.casefold() for part in re.findall(r"[a-zA-Z]{2,}", name)]
    for page in sorted(pages.values(), key=lambda item: item.get("index", 100)):
        title = page.get("title", "").casefold()
        if len(wanted) > 1 and not all(part in title for part in wanted):
            continue
        image_info = page.get("imageinfo", [{}])[0]
        metadata = image_info.get("extmetadata", {})
        license_name = _clean_metadata(metadata.get("LicenseShortName", {}).get("value"))
        license_url = _clean_metadata(metadata.get("LicenseUrl", {}).get("value"))
        normalized_license = license_name.casefold()
        if not (
            normalized_license.startswith("cc by ")
            or normalized_license.startswith("cc by-sa ")
            or normalized_license.startswith("cc0")
            or "public domain" in normalized_license
        ):
            continue
        if "noncommercial" in normalized_license or "no derivatives" in normalized_license:
            continue
        artist = _clean_metadata(metadata.get("Attribution", {}).get("value"))
        if not artist:
            artist = _clean_metadata(metadata.get("Artist", {}).get("value"))
        return {
            "url": image_info.get("thumburl", image_info.get("url")),
            "source_url": image_info.get("descriptionurl"),
            "license": license_name,
            "license_url": license_url,
            "credit": artist or "Creator not listed",
        }
    return None


class AppHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        parsed_url = urlsplit(self.path)
        requested_path = unquote(parsed_url.path)
        if requested_path == "/api/catalog":
            try:
                self._send_json(200, _sports_catalog())
            except (OSError, ValueError, json.JSONDecodeError) as error:
                self._send_json(502, {"error": f"Could not build the sports catalog: {error}"})
            return
        if requested_path == "/api/image":
            name = parse_qs(parsed_url.query).get("name", [""])[0].strip()
            if not name or len(name) > 100:
                self._send_json(400, {"error": "A player name of 1-100 characters is required."})
                return
            try:
                image = _commons_image(name)
            except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as error:
                self._send_json(502, {"error": f"Could not check Wikimedia Commons for a licensed image: {error}"})
                return
            if image is None:
                self._send_json(404, {"error": "No matching image with a supported free license was found."})
                return
            self._send_json(200, image)
            return
        if requested_path == "/favicon.ico":
            requested_path = "/favicon.svg"
        if requested_path == "/":
            requested_path = "/index.html"
        elif (
            requested_path in ("/sports", "/teams", "/players")
            or requested_path.startswith("/sports/")
            or requested_path.startswith("/teams/")
            or requested_path.startswith("/players/")
        ):
            requested_path = "/index.html"
        file_path = (ROOT / requested_path.lstrip("/")).resolve()
        public_extensions = {".html", ".css", ".js", ".svg", ".ico"}
        if (
            not file_path.is_relative_to(ROOT)
            or not file_path.is_file()
            or file_path.suffix.lower() not in public_extensions
        ):
            self.send_error(404, "Not found")
            return

        content = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/chat":
            self._send_json(404, {"error": "Not found."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "Invalid request size."})
            return
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self._send_json(413, {"error": "Please send a shorter message."})
            return

        try:
            body = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "The chat request was not valid JSON."})
            return
        if not isinstance(body, dict) or not isinstance(body.get("messages"), list):
            self._send_json(400, {"error": "A messages list is required."})
            return

        messages = body["messages"][-MAX_MESSAGES:]
        if not messages:
            self._send_json(400, {"error": "Enter a message to start chatting."})
            return
        for message in messages:
            if (
                not isinstance(message, dict)
                or message.get("role") not in ("user", "assistant")
                or not isinstance(message.get("content"), str)
                or not message["content"].strip()
                or len(message["content"]) > MAX_MESSAGE_LENGTH
            ):
                self._send_json(400, {"error": "A chat message was invalid or too long."})
                return
        if messages[-1]["role"] != "user":
            self._send_json(400, {"error": "The latest chat message must be from you."})
            return

        ollama_payload = json.dumps(
            {
                "model": MODEL,
                "stream": False,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
            }
        ).encode("utf-8")
        request = Request(
            OLLAMA_URL,
            data=ollama_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=180) as response:
                result = json.loads(response.read())
            reply = result.get("message", {}).get("content")
            if not isinstance(reply, str) or not reply.strip():
                self._send_json(502, {"error": "Ollama returned an empty response. Please try again."})
                return
            self._send_json(200, {"reply": reply.strip()})
        except HTTPError as error:
            detail = error.read(2048).decode("utf-8", errors="replace")
            self._send_json(502, {"error": f"Ollama returned an error: {detail}"})
        except (URLError, TimeoutError, OSError) as error:
            self._send_json(
                503,
                {"error": f"Could not reach Ollama at {OLLAMA_URL}: {error}"},
            )
        except (json.JSONDecodeError, AttributeError) as error:
            self._send_json(502, {"error": f"Ollama returned an invalid response: {error}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), AppHandler)
    print(f"Northstar Athletics is running at http://127.0.0.1:{port}")
    print(f"Chat model: {MODEL} ({OLLAMA_URL})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Northstar Athletics.")
    finally:
        server.server_close()
