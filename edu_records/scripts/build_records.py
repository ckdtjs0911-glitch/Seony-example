"""Google Calendar 일정(JSON) → 올해 누적 교육 기록(data/<연도>.json).

사용법:
  python3 build_records.py <events.json> <연도> <파악일 YYYY-MM-DD>

<events.json>: Google Calendar list_events 결과의 "events" 배열(또는 그 배열을 가진 객체).
파악일 이전(전날까지)에 시작한 일정만 넣는다. 매번 그해 1월 1일부터 다시 계산하므로
같은 달에 두 번 돌려도 중복이 생기지 않는다.
"""
import html
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def strip_html(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "", flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_hours(desc):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:시간|hours?|hrs?|h)\b", desc, flags=re.I)
    if not m:
        m = re.search(r"(\d+(?:\.\d+)?)\s*시간", desc)
    if not m:
        return ""
    v = m.group(1)
    return (v[:-2] if v.endswith(".0") else v) + "시간"


def split_title(title):
    m = re.match(r"\s*\[([^\]]+)\]\s*(.*)", title or "")
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", (title or "").strip()


def event_dates(ev):
    s, e = ev["start"], ev["end"]
    if "date" in s:  # 종일 일정: end는 다음 날(배타적)
        start = date.fromisoformat(s["date"])
        last = date.fromisoformat(e["date"]) - timedelta(days=1)
    else:
        start = date.fromisoformat(s["dateTime"][:10])
        last = date.fromisoformat(e["dateTime"][:10])
    return start, max(start, last)


def fmt_dates(start, last):
    if start == last:
        return start.strftime("%Y.%m.%d")
    if start.year == last.year:
        return f"{start:%Y.%m.%d}~{last:%m.%d}"
    return f"{start:%Y.%m.%d}~{last:%Y.%m.%d}"


def main():
    events_path, year, scan = sys.argv[1], int(sys.argv[2]), date.fromisoformat(sys.argv[3])
    cfg = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
    raw = json.loads(Path(events_path).read_text(encoding="utf-8"))
    events = raw.get("events", []) if isinstance(raw, dict) else raw
    email_to_emp = {m.lower(): e["name"] for e in cfg["employees"] for m in e["emails"]}

    records, unmatched = [], []
    for ev in events:
        if ev.get("status") == "cancelled":
            continue
        desc = strip_html(ev.get("description", ""))
        if cfg["keyword"] not in desc:
            continue
        start, last = event_dates(ev)
        if start.year != year or start >= scan:
            continue
        inst, course = split_title(ev.get("summary", ""))
        creator = (ev.get("creator") or {}).get("email", "").lower()
        rec = {
            "event_id": ev.get("id"),
            "start": start.isoformat(),
            "date_text": fmt_dates(start, last),
            "course": course,
            "hours": parse_hours(desc),
            "institution": inst,
            "note": "",
            "creator": creator,
            "employee": email_to_emp.get(creator),
            "title": ev.get("summary", ""),
        }
        (records if rec["employee"] else unmatched).append(rec)

    records.sort(key=lambda r: (r["employee"], r["start"]))
    out = {"year": year, "scanned_on": scan.isoformat(), "records": records, "unmatched": unmatched}
    path = BASE / "data" / f"{year}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
