"""Punto de entrada de la aplicación."""

import sys
from app.app import check_track


def main():
    """Función principal."""
    try:
        check_track()
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
