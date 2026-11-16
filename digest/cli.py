"""Command-line entry point: `digest setup` and `digest send`."""

import argparse

from digest.quiz import run_setup


def main() -> None:
    parser = argparse.ArgumentParser(prog="digest", description="Personal morning digest")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="Run the onboarding quiz and write config.yaml")
    sub.add_parser("send", help="Build and send today's digest")
    args = parser.parse_args()

    if args.command == "setup":
        run_setup()
    else:
        print("digest send: not implemented yet (Week 2)")
