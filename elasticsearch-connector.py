# Elasticsearch Connector

from __future__ import annotations


def print_banner() -> None:
    print("=" * 64)
    print("Elastic Connector")
    print("=" * 64)
    print("Purpose:")
    print("  - Detection-centric utilities for interacting with Elasticsearch.")
    print("  - Built for query validation, schema inspection, and scenario ingestion.")
    print("")
    print("Modes:")
    print("  1) CLI  - Interactive terminal interface (recommended).")
    print("  2) API  - Service interface (planned).")
    print("=" * 64)


def prompt_mode() -> str:
    while True:
        choice = input("Select mode [1=CLI, 2=API, q=quit]: ").strip().lower()
        if choice in {"1", "cli"}:
            return "cli"
        if choice in {"2", "api"}:
            return "api"
        if choice in {"q", "quit", "exit"}:
            return "quit"
        print("Invalid selection. Please enter 1, 2, or q.")


def main() -> None:
    print_banner()
    mode = prompt_mode()

    if mode == "quit":
        print("Exiting.")
        return

    if mode == "cli":
        from cli.cli import main as cli_main
        print("\nStarting CLI...\n")
        cli_main()
        return

    if mode == "api":
        print("\nAPI mode is not enabled in this release.")
        print("Planned: FastAPI gateway using the same core feature modules.")
        return


if __name__ == "__main__":
    main()
