from django.core.management.base import BaseCommand
import urllib.request
import json
from fleet.models import Route

class Command(BaseCommand):
    help = 'Seeds Route database with mock Leyte map coordinates'

    def get_osrm_route(self, name, origin, dest, coords):
        waypoints_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
        url = f"https://router.project-osrm.org/route/v1/driving/{waypoints_str}?geometries=geojson&overview=full"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Hainna-Route-Seeder/1.0'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if data['code'] != 'Ok':
                    self.stdout.write(self.style.ERROR(f"OSRM error for {name}: {data['code']}"))
                    return None
                
                route_data = data['routes'][0]
                distance_km = route_data['distance'] / 1000.0
                duration_sec = route_data['duration']
                
                hours = int(duration_sec // 3600)
                minutes = int((duration_sec % 3600) // 60)
                est_time = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                
                path_coords = [[lat, lon] for lon, lat in route_data['geometry']['coordinates']]
                wps = [{"lat": lat, "lng": lon} for lat, lon in coords]
                
                return {
                    'distance_km': distance_km,
                    'est_travel_time': est_time,
                    'path_coordinates': path_coords,
                    'waypoints': wps
                }
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch {name}: {e}"))
            return None

    def handle(self, *args, **kwargs):
        routes = [
            {
                "name": "Tacloban – Ormoc Express",
                "origin": "Tacloban City Hub",
                "destination": "Ormoc City Terminal",
                "color": "#3b82f6",
                "coords": [(11.2430, 125.0081), (11.0050, 124.6075)]
            },
            {
                "name": "Tacloban – Baybay Route",
                "origin": "Tacloban City Hub",
                "destination": "Baybay City Terminal",
                "color": "#10b981",
                "coords": [(11.2430, 125.0081), (10.6765, 124.7966)]
            },
            {
                "name": "Ormoc – Palompon Shuttle",
                "origin": "Ormoc City Terminal",
                "destination": "Palompon Port",
                "color": "#f59e0b",
                "coords": [(11.0050, 124.6075), (11.0489, 124.3831)]
            },
            {
                "name": "Tacloban – Carigara Loop",
                "origin": "Tacloban City Hub",
                "destination": "Carigara Terminal",
                "color": "#8b5cf6",
                "coords": [(11.2430, 125.0081), (11.3000, 124.6833)]
            },
            {
                "name": "Ormoc – Maasin Line",
                "origin": "Ormoc City Terminal",
                "destination": "Maasin City Hub",
                "color": "#ef4444",
                "coords": [(11.0050, 124.6075), (10.1333, 124.8333)]
            }
        ]

        self.stdout.write("Clearing old routes...")
        Route.objects.all().delete()

        self.stdout.write("Seeding Leyte routes via OSRM...")
        for r in routes:
            self.stdout.write(f"Fetching {r['name']}...")
            osrm_data = self.get_osrm_route(r['name'], r['origin'], r['destination'], r['coords'])
            if osrm_data:
                Route.objects.create(
                    name=r['name'],
                    origin=r['origin'],
                    destination=r['destination'],
                    distance_km=osrm_data['distance_km'],
                    est_travel_time=osrm_data['est_travel_time'],
                    status='Active',
                    color=r['color'],
                    geofence_radius_meters=500,
                    waypoints=osrm_data['waypoints'],
                    path_coordinates=osrm_data['path_coordinates']
                )
                self.stdout.write(self.style.SUCCESS(f"Created {r['name']} ({osrm_data['distance_km']:.2f} km)"))
        
        self.stdout.write(self.style.SUCCESS("Done seeding routes!"))
