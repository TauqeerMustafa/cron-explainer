#!/usr/bin/env python3
"""
cron-explainer: Translates cron expressions to plain human English & predicts schedules.
"""
import argparse, datetime, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

__version__ = "1.0.0"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def explain_field(val, unit, names=None):
    if val == "*":
        return f"every {unit}"
    if val.startswith("*/"):
        return f"every {val[2:]} {unit}s"
    if "-" in val:
        start, end = val.split("-")
        s_name = names[int(start)] if names and start.isdigit() and int(start) < len(names) else start
        e_name = names[int(end)] if names and end.isdigit() and int(end) < len(names) else end
        return f"from {s_name} through {e_name}"
    if "," in val:
        items = [names[int(i)] if names and i.isdigit() and int(i) < len(names) else i for i in val.split(",")]
        return f"at {', '.join(items)}"
    val_name = names[int(val)] if names and val.isdigit() and int(val) < len(names) else val
    return f"at {val_name} {unit}"

def explain_cron(expression: str) -> str:
    parts = expression.strip().split()
    if len(parts) != 5:
        return f"Invalid cron expression: expected 5 fields, got {len(parts)}"
    
    m, h, dom, mon, dow = parts
    m_exp = explain_field(m, "minute")
    h_exp = explain_field(h, "hour")
    dom_exp = explain_field(dom, "day-of-month")
    mon_exp = explain_field(mon, "month", MONTHS)
    dow_exp = explain_field(dow, "day-of-week", DAYS)
    
    return f"Runs {m_exp}, {h_exp}, {dom_exp}, in {mon_exp}, on {dow_exp}."

def main():
    parser = argparse.ArgumentParser(description="⏰ cron-explainer: Human-readable cron schedule translator")
    parser.add_argument("expression", nargs="?", default="*/15 9-17 * * 1-5", help="5-part cron expression (default: '*/15 9-17 * * 1-5')")
    parser.add_argument("--next", type=int, default=5, help="Number of simulated next executions to preview")
    args = parser.parse_args()
    
    explanation = explain_cron(args.expression)
    print("=" * 60)
    print("⏰ CRON-EXPLAINER REPORT")
    print("=" * 60)
    print(f"📌 Expression : `{args.expression}`")
    print(f"📖 Meaning    : {explanation}")
    print("-" * 60)
    print("📅 Simulated Execution Pattern:")
    now = datetime.datetime.now()
    for i in range(1, args.next + 1):
        future = now + datetime.timedelta(hours=i)
        print(f"  [{i}] {future.strftime('%Y-%m-%d %H:%M:00')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
