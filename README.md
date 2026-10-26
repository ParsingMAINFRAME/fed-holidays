# Federal Reserve holidays, 2000 to 2040

[![Refresh data](https://github.com/ParsingMAINFRAME/fed-holidays/actions/workflows/update.yml/badge.svg)](https://github.com/ParsingMAINFRAME/fed-holidays/actions/workflows/update.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Every day the Federal Reserve Banks are closed, as JSON, CSV and iCalendar. On these days FedACH and Fedwire don't settle, so this is the list that matters for ACH effective dates, wire value dates, payroll deadlines and most US bank business day logic.

## Not the same as US federal holidays

When a holiday falls on a Saturday, federal offices close on the Friday before, but the Federal Reserve Banks stay open ([Federal Reserve K.8](https://www.federalreserve.gov/aboutthefed/k8.htm)). Calendars built from a list of federal holidays mark those Fridays as bank holidays, and payments get scheduled a day early. The next ones:

| Friday | Why it looks like a holiday | Fed |
|---|---|---|
| June 18, 2027 | Juneteenth falls on Saturday | Open |
| December 24, 2027 | Christmas falls on Saturday | Open |
| December 31, 2027 | New Year's Day 2028 falls on Saturday | Open |
| November 10, 2028 | Veterans Day falls on Saturday | Open |

When a holiday falls on a Sunday, the Fed closes the following Monday, for example Monday, July 5, 2027.

## Files

| File | Format |
|---|---|
| [`fed-holidays.json`](fed-holidays.json) | `[{"date": "2026-11-11", "weekday": "Wednesday", "name": "Veterans Day"}, ...]` |
| [`fed-holidays.csv`](fed-holidays.csv) | `date,weekday,name`. Works as the holidays range for Excel or Google Sheets `NETWORKDAYS` and `WORKDAY` |
| [`fed-holidays.ics`](fed-holidays.ics) | Import into Google Calendar, Outlook or Apple Calendar. For a live subscription use `https://bankday.dev/ics/us-fed.ics` |

## Using it

Python:

```python
import datetime as dt, json

closed = {h["date"] for h in json.load(open("fed-holidays.json"))}

def is_fed_business_day(d: dt.date) -> bool:
    return d.weekday() < 5 and d.isoformat() not in closed
```

JavaScript:

```js
const closed = new Set(require("./fed-holidays.json").map((h) => h.date));

function isFedBusinessDay(iso) {
  const day = new Date(iso + "T00:00:00Z").getUTCDay();
  return day !== 0 && day !== 6 && !closed.has(iso);
}
```

## Need more than the list?

The data comes from [Bankday](https://bankday.dev), an API that also covers TARGET2, UK Bacs, Payments Canada, FedNow, 28 stock exchanges and 247 countries, and does the date math for you: add or count business days, roll conventions, Same Day ACH settlement times and FX spot value dates. The free tier is 1,000 requests a month.

## Updates

A GitHub Action refreshes the files on the 1st of each month from the Bankday API ([`update.py`](update.py)). If the Fed adds a holiday, as it did with Juneteenth in 2022, the files change here too.

## License

MIT, for both the data and the code. A link back to [Bankday](https://bankday.dev) is appreciated but not required.
