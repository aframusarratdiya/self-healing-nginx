# Self-Healing Nginx

A small high-availability web system. An nginx reverse proxy load-balances traffic between two identical Flask backends (**blue** and **green**). If one backend stops, nginx automatically sends all traffic to the other, and the failed backend rejoins when it comes back. Everything runs in Docker Compose.

## Architecture

| Container | Role |
|---|---|
| `edge` | nginx reverse proxy and load balancer, exposed on port 8080 |
| `blue-web` | Flask backend named "blue" (port 8000) |
| `green-web` | Flask backend named "green" (port 8000) |
| `collector` | Reads the nginx access log and prints each request |

## How it works

- **Health checks:** each backend is checked every 5 seconds on `/health`. nginx only starts after both backends are healthy.
- **Load balancing:** nginx alternates requests between blue and green.
- **Failover:** `max_fails=1 fail_timeout=5s` marks a failed backend as down, and `proxy_next_upstream` retries the request on the other backend, so users still get a successful response.
- **Recovery:** after `fail_timeout`, nginx tries the failed backend again and it rejoins automatically.
- **Graceful shutdown:** the Flask app drains for 2 seconds on SIGTERM.

## Run it

```
docker compose up -d --build
docker compose ps
```

Open http://localhost:8080/work. View collected logs with:

```
docker compose logs collector --tail 10
```

Stop everything with `docker compose down`.

## Test failover

```
docker stop blue-web
1..6 | ForEach-Object { (Invoke-WebRequest -UseBasicParsing http://localhost:8080/work).Content }
docker start blue-web
```

With blue stopped, every request is answered by green. After blue restarts, replies alternate again.

## Endpoints

- `/health` returns backend status
- `/work` returns the backend name after a short simulated job
- `/slow` simulates a long request