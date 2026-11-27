import argparse
import json
from dataclasses import asdict

from benchcalm.features import get_feature_providers
from benchcalm.features.base import FeatureReport


def _print_report(report: FeatureReport) -> None:
    print(f"{report.name}: {report.status} (risk: {report.risk})")
    if report.details:
        print(f"  {report.details}")
    for control in report.controls:
        current = control.current if control.current is not None else "unavailable"
        writable = "yes" if control.writable else "no"
        print(f"  {control.name}: {current} (writable: {writable})")
        if control.available_values:
            print(f"    available: {', '.join(control.available_values)}")


def _print_reports(reports: list[FeatureReport], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(report) for report in reports], indent=2))
        return
    for report in reports:
        _print_report(report)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the Benchcalm CLI."""

    parser = argparse.ArgumentParser(prog="benchcalm")
    commands = parser.add_subparsers(dest="command", required=True)
    discover_parser = commands.add_parser("discover", help="Discover supported device features")
    discover_parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args(argv)

    if args.command == "discover":
        reports = [provider.discover() for provider in get_feature_providers()]
        _print_reports(reports, args.json)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())