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
| `Terminal` | Physical node (bus terminal) with lat/lng coordinates |
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

### HTMX Navigation

Pages use **HTMX** for partial updates — navigation swaps only the `<main>` content area, avoiding full page reloads. Views detect `HX-Request` headers and return either:
- `base.html` (full page for direct access)
- `partial_base.html` (content only for HTMX swap)

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
