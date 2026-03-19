# Traccar GPS Integration

HainNa uses [Traccar](https://www.traccar.org/) — a free, open-source GPS tracking server — to display real-time vehicle positions on the Live Tracking map.

---

## Architecture

```
[Driver's Phone]          [Traccar Server]          [HainNa]
  Traccar Client App  →   (self-hosted)         ←   REST API poll
  (broadcasts GPS)        receives positions        every 5 seconds
```

1. The **Traccar Client** app on each driver's phone sends GPS positions to your Traccar server.
2. **Traccar Server** aggregates positions from all devices.
3. **HainNa** polls Traccar's REST API every 5 seconds via `GET /api/positions` and updates the Leaflet map without a page reload.

---

## Step 1: Install Traccar Server

### Option A — Docker (recommended)

```bash
docker run -d \
  --name traccar \
  --restart unless-stopped \
  -p 8082:8082 \
  -p 5055:5055 \
  -v /opt/traccar/logs:/opt/traccar/logs:rw \
  -v /opt/traccar/data:/opt/traccar/data:rw \
  traccar/traccar:latest
```

Traccar web UI will be available at `http://your-server:8082`.  
Default credentials: `admin` / `admin` (change immediately).

### Option B — Native installer

Download from [traccar.org/download](https://www.traccar.org/download/) and follow the installer for Windows/Linux.

---

## Step 2: Configure HainNa

Add these to your `.env` file:

```env
TRACCAR_URL=http://your-server:8082
TRACCAR_USER=admin
TRACCAR_PASSWORD=your_password
```

Restart the Django server after changing `.env`.

---

## Step 3: Set Up Driver Phones

1. Each driver installs **Traccar Client** from:
   - Android: [Play Store — "Traccar Client"](https://play.google.com/store/apps/details?id=org.traccar.client)
   - iOS: [App Store — "Traccar Client"](https://apps.apple.com/app/traccar-client/id843156974)

2. Open the app and configure:
   - **Server URL**: `http://your-server:5055` (note: port 5055, not 8082)
   - **Device Identifier**: any unique string, e.g. `van-01` or the plate number
   - **Frequency**: 10–30 seconds recommended
   - Enable **Start on boot**

3. The device appears in your Traccar web UI under **Devices**. Note its **numeric Device ID** — you'll need this in Step 4.

---

## Step 4: Link Vehicles to Traccar Devices

In HainNa:

1. Go to **Fleet → Vehicles**
2. Click **Edit** on a vehicle
3. In the **Traccar Device ID** field, enter the numeric ID from Traccar (not the name — the integer ID shown in the Traccar device list)
4. Save

The vehicle will now appear on the Live Tracking map.

---

## How Live Tracking Works

### Service Layer — `apps/fleet/traccar.py`

| Function | Description |
|---|---|
| `get_all_positions()` | `GET /api/positions` — returns dict keyed by device ID |
| `get_devices_map()` | `GET /api/devices` — maps device IDs to names |
| `is_connected()` | `GET /api/server` — returns `True` if Traccar is reachable |

Speed values from Traccar are in **knots** and are automatically converted to **km/h**.

### Polling Endpoint — `GET /live-tracking/positions/`

An authenticated JSON endpoint that merges Vehicle DB records with live Traccar positions:

```json
{
  "traccar_ok": true,
  "units": [
    {
      "id": "ABC-123",
      "name": "Juan Dela Cruz",
      "status": "Moving",
      "speed": 48.2,
      "speed_display": "48.2 km/h",
      "lat": 11.2437,
      "lng": 124.9937
    }
  ]
}
```

**Status logic:**
- `speed > 5 km/h` → **Moving** (green)
- `speed > 0` → **Idle** (amber)  
- `speed == 0` → **Stopped** (red)
- No GPS fix → **Offline** (grey)

### Frontend Polling

The Live Tracking page starts a `setInterval` loop 3 seconds after load, polling `/live-tracking/positions/` every 5 seconds. On each response, markers are updated with `marker.setLatLng()` — smooth movement, no page flicker.

The sidebar footer badge updates in real time:
- 🟢 **Traccar Live** — connected
- 🔴 **Traccar Offline** — server unreachable (map still loads, vehicles show as Offline)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Map shows no vehicles | Check that vehicles have a Traccar Device ID set in Fleet → Vehicles |
| Status badge shows "Traccar Offline" | Verify `TRACCAR_URL`, credentials, and that the Traccar server is running |
| Device appears in Traccar but not on map | Confirm you're using the integer Device ID (not the device name) |
| Driver's phone not reporting | Check the Traccar Client app server URL uses port `5055`, not `8082` |
| Positions are stale / not updating | Increase reporting frequency in the Traccar Client app settings |
