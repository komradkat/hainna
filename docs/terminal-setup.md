# Terminal Setup Guide

HainNa is **terminal-aware** — the system knows which physical dispatch terminal it's running at, and filters all data (trips, queues, arrivals) accordingly.

---

## Concept

Each physical terminal (e.g., Tacloban Grand Terminal, Ormoc Terminal) is stored as a **Terminal node** in the database with:
- A display name
- Latitude/longitude coordinates (used for distance calculations on the TV board)

Users select their active terminal once per session via the **Active Station** picker in the top navigation bar.

---

## Setting Up Terminals

Terminals are seeded via the management command for the Leyte network:

```bash
uv run python manage.py seed_leyte
```

This creates all terminals and routes for Eastern Visayas.

To add terminals manually, go to Django Admin at `/admin/` → **Fleet → Terminals → Add Terminal**.

---

## Cashier / Dispatcher Session Scoping

When a user logs in and selects their terminal:

1. The terminal ID is stored in their Django **session**.
2. All views automatically filter by this terminal:
   - **POS (Booking)** — shows active trips departing from this terminal
   - **Dispatch Board** — shows the queue for this terminal's routes
   - **TV Board** — shows arrivals *destined for* this terminal

If no terminal is selected, the user is redirected to the **Select Station** page before accessing the POS or Dispatch Board.

---

## TV / Public Board

The public departure board is accessible without login at:

```
/booking/board/<terminal-name>/
```

For example: `/booking/board/Tacloban/`

Display it on a large TV screen at each terminal. It auto-refreshes every 15 seconds and shows:
- 🟠 **Loading** trips (currently departing)
- 🟡 **Standing By** trips (queued, not yet loading)
- 🟢 **Arriving** trips (inbound from other terminals, sorted by ETA/distance)

---

## Routes Between Terminals

Routes are directional — a route from **Tacloban → Ormoc** is distinct from **Ormoc → Tacloban**. Both must be created to support operations in both directions.

When a trip is marked **Completed** at the destination terminal, the system automatically creates a new **Standing By** trip for the reverse route, assigning the same vehicle. This means drivers don't need to be manually re-queued for the return journey.

---

## Multi-Terminal Operations

In a multi-terminal network:
- Each cashier workstation logs in and selects its own terminal
- Trips dispatched at Terminal A appear in the **Arriving** section of Terminal B's TV board
- The system uses terminal coordinates to estimate arrival order when multiple vans are inbound
