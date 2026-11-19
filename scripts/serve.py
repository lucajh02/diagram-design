#!/usr/bin/env python3
"""Serve the diagram gallery on localhost.

Usage:
    python3 scripts/serve.py            # http://localhost:8000/
    python3 scripts/serve.py --port 9000
    python3 scripts/serve.py --open     # also open the browser

Only the standard library is used. The server binds to 127.0.0.1 by default,
so it is reachable from this machine only.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills" / "diagram-design" / "assets"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="127.0.0.1", help="bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="port (default: 8000)")
    parser.add_argument("--open", action="store_true", help="open the gallery in the default browser")
    args = parser.parse_args()

    if not (ROOT / "index.html").is_file():
        print(f"error: gallery not found at {ROOT}", file=sys.stderr)
        return 1

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    try:
        server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        print(f"error: cannot bind {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

    url = f"http://localhost:{args.port}/" if args.host in ("127.0.0.1", "0.0.0.0", "localhost") else f"http://{args.host}:{args.port}/"
    print(f"Serving {ROOT} at {url}  (Ctrl+C to stop)")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
