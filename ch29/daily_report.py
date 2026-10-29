# daily_report.py - Chapter 29 mini project
"""Email a daily server report: HTML summary, plain-text fallback, chart and CSV attached.
Run with --dry-run first: it saves the message as report.eml so you can open it in your mail app."""
import argparse
import io
import os
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent
CSV = BASE / "health_history.csv"           # written by the Chapter 13 health monitor


def summarize(df: pd.DataFrame) -> dict:
    day = df[df["time"].dt.date == df["time"].dt.date.max()]
    return {"date": day["time"].dt.date.max(), "readings": len(day),
            "cpu_avg": day["cpu"].mean(), "cpu_max": day["cpu"].max(),
            "cpu_peak_at": day.loc[day["cpu"].idxmax(), "time"],
            "mem_max": day["mem"].max(), "disk": day["disk"].iloc[-1],
            "high": int((day["cpu"] > 85).sum()), "day": day}


def chart_png(day: pd.DataFrame) -> bytes:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(day["time"], day["cpu"], color="#2b6cb0", linewidth=1)
    ax.axhline(85, color="crimson", linestyle="--", linewidth=1, label="alert level 85%")
    ax.set(title="CPU % today", ylim=(0, 100))
    ax.legend(loc="upper left")
    fig.autofmt_xdate()
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    return buf.getvalue()


def build_message(s: dict, sender: str, to: list[str]) -> EmailMessage:
    status = "ATTENTION" if s["high"] or s["disk"] > 85 else "OK"
    msg = EmailMessage()
    msg["Subject"] = f"[{status}] web01 daily report {s['date']}"
    msg["From"], msg["To"] = sender, ", ".join(to)
    text = (f"Daily report for {s['date']}\n"
            f"CPU average {s['cpu_avg']:.1f}%, max {s['cpu_max']:.1f}% at {s['cpu_peak_at']:%H:%M}\n"
            f"Readings above 85%: {s['high']}\nMemory max {s['mem_max']:.1f}%\nDisk {s['disk']:.1f}%\n")
    msg.set_content(text)                                    # plain-text version for every mail client
    cid = make_msgid()
    color = "#c62828" if status == "ATTENTION" else "#2e7d32"
    msg.add_alternative(f"""\
<html><body style="font-family:Arial,sans-serif;color:#222">
<h2 style="margin:0 0 4px">web01 daily report</h2>
<p style="margin:0 0 12px;color:{color};font-weight:bold">{status} &middot; {s['date']}</p>
<table cellpadding="6" style="border-collapse:collapse">
<tr><td>CPU average</td><td><b>{s['cpu_avg']:.1f}%</b></td></tr>
<tr><td>CPU max</td><td><b>{s['cpu_max']:.1f}%</b> at {s['cpu_peak_at']:%H:%M}</td></tr>
<tr><td>Readings above 85%</td><td><b>{s['high']}</b></td></tr>
<tr><td>Memory max</td><td>{s['mem_max']:.1f}%</td></tr>
<tr><td>Disk used</td><td>{s['disk']:.1f}%</td></tr></table>
<p><img src="cid:{cid[1:-1]}" alt="CPU chart" width="640"></p>
</body></html>""", subtype="html")
    msg.get_payload()[1].add_related(chart_png(s["day"]), "image", "png", cid=cid)   # image shown inline
    msg.add_attachment(s["day"].to_csv(index=False).encode(), maintype="text", subtype="csv",
                       filename=f"readings_{s['date']}.csv")
    return msg


def send(msg: EmailMessage, host: str, port: int, user: str | None, password: str | None) -> None:
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        if port == 587:
            smtp.starttls(context=ssl.create_default_context())
        if user:
            smtp.login(user, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", nargs="+", default=[os.environ.get("REPORT_TO", "ops@example.com")])
    ap.add_argument("--dry-run", action="store_true", help="save report.eml instead of sending")
    a = ap.parse_args()
    data = pd.read_csv(CSV, parse_dates=["time"])
    summary = summarize(data)
    sender = os.environ.get("SMTP_USER", "reports@example.com")
    message = build_message(summary, sender, a.to)
    if a.dry_run:
        (BASE / "report.eml").write_bytes(bytes(message))
        print("Saved report.eml:", message["Subject"])
    else:
        send(message, os.environ.get("SMTP_HOST", "smtp.gmail.com"), int(os.environ.get("SMTP_PORT", 587)),
             os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASSWORD"))
        print("Sent:", message["Subject"])
