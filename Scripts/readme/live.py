"""Data-driven cards, rebuilt by the `README cards` workflow.

- contributions.wav: the last 12 months of GitHub contributions drawn as an
  audio waveform with a playhead sweeping across it
- stats: streaks, stars, repos and a language breakdown
- sensors: the latest SensorHub readings from sadra.nl's public API

Each source is fetched independently; if one fails, its previous cards are
left untouched so the README never shows a broken image.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from svg import (
    DISPLAY,
    MONO,
    SANS,
    THEMES,
    Theme,
    card_frame,
    clip_card,
    document,
    esc,
    font_css,
    measure,
)

UA = "SadraShameli-readme-cards (+https://github.com/SadraShameli/SadraShameli)"
SADRA_API = "https://sadra.nl/api/trpc/reading.getReadingsInput"
SENSOR_LOCATION_PK = 1  # Rijswijk
LIVE_WINDOW = timedelta(hours=3)


def _get_json(url: str, *, data: bytes | None = None, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=25) as res:
        return json.load(res)


# ── GitHub ──────────────────────────────────────────────────────────────────

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


@dataclass
class GitHubStats:
    days: list[tuple[date, int]]
    total: int
    repos: int
    stars: int
    followers: int
    since: int
    languages: list[tuple[str, str, float]]  # name, colour, share

    @property
    def current_streak(self) -> int:
        counts = [c for _, c in self.days]
        # today may simply not have happened yet
        if counts and counts[-1] == 0:
            counts = counts[:-1]
        n = 0
        for c in reversed(counts):
            if not c:
                break
            n += 1
        return n

    @property
    def longest_streak(self) -> int:
        best = run = 0
        for _, c in self.days:
            run = run + 1 if c else 0
            best = max(best, run)
        return best

    @property
    def peak(self) -> tuple[date, int]:
        return max(self.days, key=lambda d: d[1])


def fetch_github(login: str, token: str) -> GitHubStats:
    payload = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    res = _get_json(
        "https://api.github.com/graphql",
        data=payload,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    if res.get("errors"):
        raise RuntimeError(res["errors"])
    user = res["data"]["user"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [
        (date.fromisoformat(d["date"]), d["contributionCount"])
        for w in cal["weeks"]
        for d in w["contributionDays"]
    ]
    sizes: dict[str, list] = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            entry = sizes.setdefault(name, [edge["node"]["color"] or "#8b8b8b", 0])
            entry[1] += edge["size"]
    total_size = sum(v[1] for v in sizes.values()) or 1
    ranked = sorted(sizes.items(), key=lambda kv: kv[1][1], reverse=True)
    languages = [(name, color, size / total_size) for name, (color, size) in ranked[:6]]
    rest = 1 - sum(share for *_, share in languages)
    if rest > 0.005:
        languages.append(("Other", "#8b8b8b", rest))
    return GitHubStats(
        days=days,
        total=cal["totalContributions"],
        repos=user["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        followers=user["followers"]["totalCount"],
        since=int(user["createdAt"][:4]),
        languages=languages,
    )


def _css(t: Theme) -> str:
    return font_css(("sgm", 400), ("sgm", 600), ("sgs", 400), ("sor", 800)) + (
        f".eb{{font-family:{MONO};font-size:11px;letter-spacing:2px;fill:{t.muted}}}"
        f".mo{{font-family:{MONO};font-size:12px;fill:{t.faint}}}"
        f".big{{font-family:{DISPLAY};font-weight:800;fill:{t.text}}}"
        f".sm{{font-family:{SANS};font-size:13px;fill:{t.muted}}}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
    )


def waveform_card(t: Theme, gh: GitHubStats) -> str:
    W, H = 1000, 260
    x0, x1 = 32, W - 32
    mid, amp = 142, 64
    days = gh.days
    n = len(days)
    pitch = (x1 - x0) / n
    bw = max(pitch * 0.62, 1)
    top = max(c for _, c in days) or 1
    bars = []
    for i, (_, c) in enumerate(days):
        h = max((c / top) ** 0.55 * amp, 0.8)
        x = x0 + i * pitch
        bars.append(f'<rect x="{x:.2f}" y="{mid - h:.2f}" width="{bw:.2f}" height="{h * 2:.2f}" rx="{bw / 2:.2f}"/>')
    bars_svg = "".join(bars)

    months = []
    seen = set()
    for i, (d, _) in enumerate(days):
        if d.day <= 7 and d.month not in seen and i > 3:
            seen.add(d.month)
            months.append(
                f'<text x="{x0 + i * pitch:.1f}" y="{mid + amp + 30}" class="mo">{d.strftime("%b").lower()}</text>'
            )
    peak_day, peak_n = gh.peak
    peak_i = days.index((peak_day, peak_n))
    px = x0 + peak_i * pitch

    dur = 16
    title = "contributions.wav"
    sub = f"{gh.total:,} contributions · last 12 months"
    body = (
        "<defs>"
        + clip_card("clip", W, H)
        + f'<clipPath id="played"><rect x="{x0}" y="0" width="0" height="{H}">'
        f'<animate attributeName="width" values="0;{x1 - x0};{x1 - x0}" keyTimes="0;.92;1" dur="{dur}s" '
        f'repeatCount="indefinite"/></rect></clipPath>'
        f'<linearGradient id="wv" x1="0" x2="1"><stop offset="0" stop-color="{t.green}"/>'
        f'<stop offset="1" stop-color="{t.text}"/></linearGradient>'
        "</defs>"
        + card_frame(t, W, H)
        + '<g clip-path="url(#clip)">'
        # player header
        + f'<circle cx="{x0 + 18}" cy="48" r="18" fill="{t.text}"/>'
        f'<path d="M{x0 + 13} 39 L{x0 + 26} 48 L{x0 + 13} 57Z" fill="{t.bg}"/>'
        f'<text x="{x0 + 50}" y="44" font-family="{MONO}" font-size="15" font-weight="600" fill="{t.text}">{title}</text>'
        f'<text x="{x0 + 50}" y="64" class="sm">{esc(sub)}</text>'
        f'<text x="{x1}" y="44" text-anchor="end" class="eb">STREAK {gh.current_streak}D · BEST {gh.longest_streak}D</text>'
        f'<text x="{x1}" y="64" text-anchor="end" class="sm">peak {peak_n} on {_day(peak_day)}</text>'
        # waveform: dim base + bright played part
        + f'<g fill="{t.faint}" fill-opacity=".55">{bars_svg}</g>'
        + f'<g fill="url(#wv)" clip-path="url(#played)">{bars_svg}</g>'
        + f'<line x1="{x0}" y1="{mid}" x2="{x1}" y2="{mid}" stroke="{t.faint}" stroke-opacity=".35"/>'
        # playhead
        + f'<g><line x1="{x0}" y1="{mid - amp - 10}" x2="{x0}" y2="{mid + amp + 10}" stroke="{t.text}" stroke-width="1.5"/>'
        f'<circle cx="{x0}" cy="{mid - amp - 10}" r="4" fill="{t.text}"/>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;{x1 - x0} 0;{x1 - x0} 0" '
        f'keyTimes="0;.92;1" dur="{dur}s" repeatCount="indefinite"/></g>'
        # peak marker
        + f'<path d="M{px:.1f} {mid - amp - 22}l-4 -6h8z" fill="{t.yellow}"/>'
        + "".join(months)
        + "</g>"
    )
    return document(W, H, body, _css(t), title="contributions.wav", desc=sub)


def stats_card(t: Theme, gh: GitHubStats) -> str:
    W, H = 1000, 236
    pad, gap = 24, 12
    tiles = [
        ("CONTRIBUTIONS · 12 MO", f"{gh.total:,}", "commits, PRs, issues & reviews"),
        ("CURRENT STREAK", f"{gh.current_streak}", "days in a row"),
        ("LONGEST STREAK", f"{gh.longest_streak}", "days, last 12 months"),
        ("ON GITHUB SINCE", f"{gh.since}", f"{gh.repos} repos · {gh.stars} stars"),
    ]
    tw = (W - pad * 2 - gap * (len(tiles) - 1)) / len(tiles)
    th = 108
    parts = []
    for i, (label, value, note) in enumerate(tiles):
        x = pad + i * (tw + gap)
        parts.append(
            f'<rect x="{x:.1f}" y="{pad}" width="{tw:.1f}" height="{th}" rx="12" fill="{t.panel}" stroke="{t.border}"/>'
            f'<text x="{x + 18:.1f}" y="{pad + 28}" class="eb">{esc(label)}</text>'
            f'<text x="{x + 16:.1f}" y="{pad + 72}" class="big" font-size="34">{esc(value)}</text>'
            f'<text x="{x + 18:.1f}" y="{pad + 94}" class="sm">{esc(note)}</text>'
        )
    # language bar
    by = pad + th + 34
    bx, bw_total = pad, W - pad * 2
    parts.append(f'<text x="{bx}" y="{by - 10}" class="eb">LANGUAGES · PUBLIC REPOS</text>')
    x = bx
    segs = []
    for name, color, share in gh.languages:
        w = bw_total * share
        segs.append(f'<rect x="{x:.1f}" y="{by}" width="{max(w - 2, 1):.1f}" height="10" fill="{color}"/>')
        x += w
    parts.append(
        f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw_total}" height="10" rx="5"/></clipPath>'
        f'<g clip-path="url(#bar)">{"".join(segs)}</g>'
    )
    lx, ly = bx, by + 34
    for name, color, share in gh.languages:
        label = f"{name} {share * 100:.1f}%"
        parts.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
            f'<text x="{lx + 16}" y="{ly}" class="sm">{esc(label)}</text>'
        )
        lx += 16 + measure(label, "sans", 400, 13) + 26
    body = (
        "<defs>" + clip_card("clip", W, H) + "</defs>" + card_frame(t, W, H)
        + '<g clip-path="url(#clip)">' + "".join(parts) + "</g>"
    )
    desc = "; ".join(f"{a}: {b}" for a, b, _ in tiles)
    return document(W, H, body, _css(t), title="GitHub stats", desc=desc)


# ── SensorHub ───────────────────────────────────────────────────────────────


@dataclass
class Series:
    name: str
    unit: str
    latest: float
    high: float
    low: float
    values: list[float]


@dataclass
class SensorSnapshot:
    series: dict[int, Series]  # by sensor id
    at: datetime  # time of the newest reading


SENSORS_SHOWN = [(1, "TEMPERATURE"), (2, "HUMIDITY"), (3, "AIR PRESSURE"), (6, "LOUDNESS")]


def _parse_reading_date(raw: str, now: datetime) -> datetime:
    # the API formats dates as "15 May, 7:54" without a year (server time, UTC)
    parsed = datetime.strptime(f"{raw.strip()} {now.year}", "%d %b, %H:%M %Y").replace(tzinfo=timezone.utc)
    if parsed > now + timedelta(days=1):
        parsed = parsed.replace(year=now.year - 1)
    return parsed


def fetch_sensors(now: datetime) -> SensorSnapshot:
    query = urllib.parse.urlencode(
        {"input": json.dumps({"json": {"location_id": SENSOR_LOCATION_PK, "granularity": "raw"}})}
    )
    res = _get_json(f"{SADRA_API}?{query}")
    data = res["result"]["data"]["json"]
    if "data" not in data:
        raise RuntimeError(data.get("error", "no readings"))
    series: dict[int, Series] = {}
    newest = None
    for rec in data["data"]:
        sid = rec["sensor"]["id"]
        series[sid] = Series(
            name=rec["sensor"]["name"],
            unit=rec["sensor"]["unit"],
            latest=rec["latestReading"]["value"],
            high=rec["highest"],
            low=rec["lowest"],
            values=[r["value"] for r in rec["readings"]],
        )
        at = _parse_reading_date(rec["latestReading"]["date"], now)
        newest = at if newest is None or at > newest else newest
    if newest is None:
        raise RuntimeError("empty response")
    return SensorSnapshot(series=series, at=newest)


def _day(d: date) -> str:
    return f"{d.day} {d:%b %Y}"


def _ago(delta: timedelta) -> str:
    s = int(delta.total_seconds())
    for unit, size in (("month", 30 * 86400), ("day", 86400), ("hour", 3600), ("minute", 60)):
        if s >= size:
            n = s // size
            return f"{n} {unit}{'s' if n != 1 else ''} ago"
    return "just now"


def sensor_card(t: Theme, snap: SensorSnapshot, now: datetime) -> str:
    W, H = 1000, 300
    pad, gap = 24, 12
    live = now - snap.at <= LIVE_WINDOW
    status_color = t.green if live else t.yellow
    status = "LIVE" if live else "OFFLINE"
    parts = [
        f'<text x="{pad + 4}" y="46" font-family="{MONO}" font-size="15" font-weight="600" fill="{t.text}">'
        "sensorhub</text>"
        f'<text x="{pad + 4 + measure("sensorhub", "mono", 600, 15) + 10:.1f}" y="46" class="sm">'
        "Sadra's Reader · Rijswijk, NL · BME680 + INMP441</text>"
    ]
    pill = f"{status} · last reading {_ago(now - snap.at)}"
    pw = measure(pill, "mono", 400, 11, 2) + 40
    px = W - pad - pw
    anim = ' style="animation:pulse 1.6s ease-in-out infinite"' if live else ""
    parts.append(
        f'<rect x="{px:.1f}" y="27" width="{pw:.1f}" height="26" rx="13" fill="{t.panel}" stroke="{t.border}"/>'
        f'<circle cx="{px + 16:.1f}" cy="40" r="4.5" fill="{status_color}"{anim}/>'
        f'<text x="{px + 28:.1f}" y="44" class="eb" style="fill:{t.text}">{esc(pill.upper())}</text>'
    )
    shown = [(sid, label) for sid, label in SENSORS_SHOWN if sid in snap.series]
    tw = (W - pad * 2 - gap * (len(shown) - 1)) / max(len(shown), 1)
    ty, th = 72, 172
    for i, (sid, label) in enumerate(shown):
        s = snap.series[sid]
        x = pad + i * (tw + gap)
        value = f"{s.latest:g}"
        parts.append(
            f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="12" fill="{t.panel}" stroke="{t.border}"/>'
            f'<text x="{x + 18:.1f}" y="{ty + 28}" class="eb">{label}</text>'
            f'<text x="{x + 16:.1f}" y="{ty + 72}" class="big" font-size="32">{esc(value)}'
            f'<tspan font-family="{MONO}" font-weight="400" font-size="15" fill="{t.muted}" dx="6">{esc(s.unit)}</tspan></text>'
        )
        # sparkline over the last hour of readings
        vals = s.values or [s.latest]
        lo, hi = min(vals), max(vals)
        span = (hi - lo) or 1
        sx0, sx1, sy0, sy1 = x + 18, x + tw - 18, ty + 96, ty + 138
        pts = [
            (sx0 + (sx1 - sx0) * (j / max(len(vals) - 1, 1)), sy1 - (v - lo) / span * (sy1 - sy0))
            for j, v in enumerate(vals)
        ]
        line = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        area = f"{line} L{sx1:.1f} {sy1} L{sx0:.1f} {sy1}Z"
        parts.append(
            f'<path d="{area}" fill="{t.text}" fill-opacity=".06"/>'
            f'<path d="{line}" fill="none" stroke="{t.text}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="3" fill="{status_color}"/>'
            f'<text x="{x + 18:.1f}" y="{ty + th - 14}" class="mo">lo {s.low:g} · hi {s.high:g} · 1h</text>'
        )
    parts.append(
        f'<text x="{pad + 4}" y="{H - 20}" class="mo">'
        f"newest reading {_day(snap.at)}, {snap.at:%H:%M} UTC · via sadra.nl/api · "
        f"card rebuilt {_day(now)}, {now:%H:%M} UTC</text>"
    )
    body = (
        "<defs>" + clip_card("clip", W, H) + "</defs>" + card_frame(t, W, H)
        + '<g clip-path="url(#clip)">' + "".join(parts) + "</g>"
    )
    desc = ", ".join(f"{snap.series[s].name} {snap.series[s].latest:g} {snap.series[s].unit}" for s, _ in shown)
    return document(W, H, body, _css(t), title=f"SensorHub readings ({status.lower()})", desc=desc)


# ── entry point ─────────────────────────────────────────────────────────────


def _warn(msg: str) -> None:
    # shows up as an annotation on the workflow run
    prefix = "::warning::" if os.environ.get("GITHUB_ACTIONS") else "warning: "
    print(prefix + msg, file=sys.stderr)


def build_live(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    failures = 0

    def write(name: str, render) -> None:
        for t in THEMES:
            (out / f"{name}-{t.name}.svg").write_text(render(t), encoding="utf-8")

    token = os.environ.get("STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("STATS_LOGIN", "SadraShameli")
    if token:
        try:
            gh = fetch_github(login, token)
            write("live-contributions", lambda t: waveform_card(t, gh))
            write("live-stats", lambda t: stats_card(t, gh))
            print(f"github: {gh.total} contributions, {gh.repos} repos")
        except Exception as exc:  # keep the previous cards
            failures += 1
            _warn(f"github cards not rebuilt: {exc}")
    else:
        _warn("github cards not rebuilt: set STATS_TOKEN or GITHUB_TOKEN")

    try:
        snap = fetch_sensors(now)
        write("live-sensors", lambda t: sensor_card(t, snap, now))
        print(f"sensors: newest reading {snap.at.isoformat()}")
    except Exception as exc:
        failures += 1
        _warn(f"sensor card not rebuilt: {exc}")
    return failures
