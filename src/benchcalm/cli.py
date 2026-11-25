import argparse


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the Benchcalm CLI."""

    ap = argparse.ArgumentParser(prog="benchcalm")
    ap.add_argument("command", choices=["setup", "revert", "status", "check", "doctor"])
    ap.add_argument("--profile", type=str, default=None)
    ap.add_argument("--journal", type=str, default=None)
    args = ap.parse_args(argv)


if __name__ == "__main__":
    main()