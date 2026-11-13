import os
import signal
import sys
import time
from flask import Flask, jsonify, request

app = Flask(__name__)
BACKEND_NAME = os.environ.get("BACKEND_NAME", "unknown")
DRAINING = False


@app.route("/health")
def health():
    return jsonify(status="ok", backend=BACKEND_NAME, draining=DRAINING)


@app.route("/work")
def work():
    delay = int(request.args.get("ms", 100))
    time.sleep(delay / 1000)
    return jsonify(
        backend=BACKEND_NAME,
        pid=os.getpid(),
        duration_ms=delay,
    )


@app.route("/slow")
def slow():
    delay = int(request.args.get("ms", 5000))
    time.sleep(delay / 1000)
    return jsonify(
        backend=BACKEND_NAME,
        completed=True,
        duration_ms=delay,
    )


def graceful_shutdown(signum, frame):
    global DRAINING
    DRAINING = True
    print(f"[{BACKEND_NAME}] received SIGTERM, draining requests", flush=True)
    time.sleep(2)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    print(f"[{BACKEND_NAME}] starting on port 8000", flush=True)
    app.run(host="0.0.0.0", port=8000, threaded=True)
