"""Command-line entry point: `digest setup`, `digest fetch`, `digest send`."""

import argparse

from digest.db import Store
from digest.ingest import ingest
from digest.profile import Profile


def _fetch(profile: Profile) -> dict[str, int]:
    store = Store()
    try:
        return ingest(profile, store)
    finally:
        store.close()


def main() -> None:
    parser = argparse.ArgumentParser(prog="digest", description="Personal morning digest")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="Run the onboarding quiz and write config.yaml")
    sub.add_parser("fetch", help="Fetch feeds and store new articles (no email sent)")
    sub.add_parser("send", help="Build and send today's digest")
    args = parser.parse_args()

    if args.command == "setup":
        from digest.quiz import run_setup

        run_setup()
        return

    profile = Profile.load()
    if args.command == "fetch":
        counts = _fetch(profile)
        print(f"Stored {sum(counts.values())} new articles: {counts}")
    else:
        counts = _fetch(profile)
        print(f"digest send: {sum(counts.values())} new articles fetched; "
              "email delivery lands once SMTP is configured (see .env.example)")
