#!/usr/bin/env python3
"""Static server for the dashboard.

`python3 -m http.server` cannot be used here: its CLI evaluates os.getcwd() at
import time, which the preview sandbox denies. This takes the directory and port
as explicit arguments so no working-directory lookup ever happens.

    python3 dashboard/serve.py <absolute-dir> <port>
"""
import functools, http.server, socketserver, sys

directory = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 4173

TEXTUAL = {"text/html", "text/css", "text/plain", "text/javascript",
           "application/javascript", "application/json", "image/svg+xml"}

class Handler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        # SimpleHTTPRequestHandler omits the charset, and this page carries no
        # <meta charset> of its own (the Artifact platform supplies one at publish
        # time). Without this, em-dashes and ellipses render as mojibake locally.
        t = super().guess_type(path)
        base = t.split(";")[0].strip()
        return t + "; charset=utf-8" if base in TEXTUAL and "charset" not in t else t

    def end_headers(self):
        # always serve the freshest build — this file is regenerated often
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()
    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", port),
                            functools.partial(Handler, directory=directory)) as httpd:
    print(f"serving {directory} on http://127.0.0.1:{port}", flush=True)
    httpd.serve_forever()
