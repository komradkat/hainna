# Architecture Overview

A high-level map of how HainNa is structured — apps, key models, data flow, and external integrations.

---

## App Structure

```
apps/
├── core/         # Project hub — settings, base URLs, dashboard, live tracking
├── fleet/        # Physical fleet — vehicles, drivers, routes, terminals, GPS
├── booking/      # Operations — trips, tickets, POS, dispatch, public board
└── users/        # Auth — custom user model, roles, password management
```

---

## Key Models

### `fleet`

| Model | Description |
|---|---|
| `Terminal` | Physical node (bus terminal). `is_master_hub` grants global dispatch/viewing rights. |
| `Route` | Directional link between two Terminals with distance/time |
| `Vehicle` | Van/bus with Traccar Device ID for GPS tracking |
| `Driver` | Driver record linked to a User |
| `MaintenanceLog` | Service history per vehicle |
| `Zone` | Geographic zone/geofence polygon |

### `booking`

| Model | Description |
|---|---|
| `Trip` | A single journey on a Route, with a Vehicle, Driver, and status |
| `Ticket` | A passenger ticket issued for a Trip |

### `users`

| Model | Description |
|---|---|
| `CustomUser` | Extended Django user with `role`, `department`, `position`, `status`, `requires_password_change` |

---

## Trip Lifecycle

```
[Cashier creates trip]
        │
        ▼
   Standing By ──── Cashier loads passengers ──▶ Loading
        │                                            │
        │                                            ▼
        │                                       Dispatched
        │                                            │
        └────────────────────────────────────────────▼
                                               Completed
                                                    │
                                    [Auto: create reverse trip]
                                                    │
                                                    ▼
                                            Standing By (return)
```

When a trip is **Completed**, the system automatically creates a **Standing By** trip for the reverse route, assigning the same vehicle. This prevents manual re-queuing.

---

## Request Flow

```
Browser ──▶ Nginx ──▶ Gunicorn ──▶ Django
                                     │
                          ┌──────────┼──────────┐
                          ▼          ▼           ▼
                       SQLite/    WhiteNoise   Templates
                      Postgres    (static)    HTMX partials
```

### HTMX Navigation & Dynamic UI

The interface uses **HTMX** for partial page updates to maintain a smooth, "app-like" feel without full reloads:
- **Sidebar Integration**: The sidebar remains static while the contents of the `<main>` area are swapped on navigation.
- **Partial Swaps**: Views detect `HX-Request` and return either `base.html` (full page) or `partial_base.html` (main content only).
- **Event Triggers**: The system uses `HX-Trigger` headers to refresh UI components across different areas of the dashboard (e.g., `fleetChanged` triggers a refresh of the metrics overview).

---

## Performance & Caching

To ensure low latency on high-traffic terminals:
- **Dashboard Stats**: Key metrics (revenue, active trips, fleet efficiency) are cached using Django's cache framework with a 60-second TTL.
- **Select Related**: Views heavily use `.select_related()` and `.prefetch_related()` to avoid N+1 query bottlenecks in the dispatch boards.

---

## GPS Data Flow

```
Driver Phone
  Traccar Client App
        │ broadcasts GPS every 10-30s
        ▼
  Traccar Server (:5055)
        │ stores positions
        ▼
  Traccar REST API (:8082)
        │ polled by HainNa every 5s
        ▼
  /live-tracking/positions/ (JSON)
        │
        ▼
  Leaflet map (browser)
  marker.setLatLng() — smooth update
```

See [Traccar Integration](traccar-integration.md) for full setup instructions.

---

## Authentication & Access Control

- All views require login (`LoginRequiredMixin` or `@login_required`)
- Session is scoped to a terminal — POS and Dispatch Board redirect to terminal selection if no session context is set
- Public exception: `/booking/board/<terminal>/` (TV display, no login required)
- Sessions expire after **8 hours** or on browser close

---

## Static Files

In **development**: Django serves static files automatically via `runserver`.

In **production**: WhiteNoise middleware serves compressed, cached static files from `staticfiles/` without needing a separate Nginx `location /static/` block (though Nginx can still front it for performance).
