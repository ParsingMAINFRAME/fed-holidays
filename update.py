"""Regenerate the Federal Reserve holiday files from the Bankday API (keyless playground).

    python update.py
"""
import csv
import json
import urllib.request

API = "https://bankday.dev/demo/v1/holidays?calendar=us-fed&start={}-01-01&end={}-12-31"
RANGES = [(2000, 2009), (2010, 2019), (2020, 2029), (2030, 2039), (2040, 2040)]  # the API caps a range at 10 years


def fetch():
    out = []
    for a, b in RANGES:
        req = urllib.request.Request(API.format(a, b), headers={"user-agent": "fed-holidays-updater (+https://github.com/ParsingMAINFRAME/fed-holidays)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            out += [{"date": h["date"], "weekday": h["weekday"], "name": h["name"]} for h in json.load(r)["holidays"]]
    return out


def ics_text(s):
    return s.replace("\\", "\\\\").replace(",", r"\,").replace(";", r"\;")


def ics(rows):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Bankday//fed-holidays//EN", "CALSCALE:GREGORIAN",
             "X-WR-CALNAME:" + ics_text("Federal Reserve holidays (FedACH, Fedwire)")]
    for h in rows:
        d = h["date"].replace("-", "")
        lines += ["BEGIN:VEVENT", f"UID:us-fed-{h['date']}@bankday.dev", f"DTSTAMP:{d}T000000Z", f"DTSTART;VALUE=DATE:{d}",
                  "SUMMARY:" + ics_text("Fed closed: " + h["name"]), "TRANSP:TRANSPARENT", "END:VEVENT"]
    return "\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n"


def main():
    rows = fetch()
    assert len(rows) > 300 and rows[0]["date"].startswith("2000"), "unexpected API response"
    with open("fed-holidays.json", "w", encoding="utf-8", newline="\n") as f:
        f.write("[\n" + ",\n".join("  " + json.dumps(r) for r in rows) + "\n]\n")
    with open("fed-holidays.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "weekday", "name"])
        w.writerows([r["date"], r["weekday"], r["name"]] for r in rows)
    with open("fed-holidays.ics", "w", encoding="utf-8", newline="") as f:
        f.write(ics(rows))
    print(f"{len(rows)} closures, {rows[0]['date']} to {rows[-1]['date']}")


if __name__ == "__main__":
    main()
