"""Application entry point."""

import sys
from app.app import check_track


def main():
    """Main function."""
    try:
        check_track()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
