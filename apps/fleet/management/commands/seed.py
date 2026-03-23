from django.core.management.base import BaseCommand
import datetime
import random
import urllib.request
import json
from django.utils import timezone
from fleet.models import Driver, Vehicle, MaintenanceLog, Zone, Route, Terminal
from booking.models import Trip, Ticket

class Command(BaseCommand):
    help = 'Centralized Database Seeder for Hainna CRM (Fleet, Logistics, Leyte Routes, Booking)'

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
        self.stdout.write("Initializing Centralized Holistic Seeder...")

        # 1. Clear old data securely
        self.stdout.write("Wiping legacy modules...")
        Ticket.objects.all().delete()
        Trip.objects.all().delete()
        MaintenanceLog.objects.all().delete()
        Vehicle.objects.all().delete()
        Driver.objects.all().delete()
        Zone.objects.all().delete()
        Route.objects.all().delete()
        Terminal.objects.all().delete()

        # 2. Seed Drivers
        drivers_data = [
            {"first_name": "Juan", "last_name": "Dela Cruz", "license": "L01-20-123456", "contact": "0917-111-2222", "status": "Active", "rating": 4.8},
            {"first_name": "Pedro", "last_name": "Penduko", "license": "L01-21-234567", "contact": "0918-222-3333", "status": "Active", "rating": 4.5},
            {"first_name": "Jose", "last_name": "Rizal", "license": "L04-19-345678", "contact": "0919-333-4444", "status": "Off Duty", "rating": 5.0},
            {"first_name": "Andres", "last_name": "Bonifacio", "license": "L02-18-456789", "contact": "0920-444-5555", "status": "Active", "rating": 4.9},
            {"first_name": "Antonio", "last_name": "Luna", "license": "L03-22-567890", "contact": "0921-555-6666", "status": "On Leave", "rating": 4.7},
        ]
        
        driver_objs = []
        for d in drivers_data:
            drv = Driver.objects.create(
                first_name=d["first_name"],
                last_name=d["last_name"],
                license_number=d["license"],
                license_expiry=datetime.date.today() + datetime.timedelta(days=random.randint(100, 1000)),
                contact_number=d["contact"],
                status=d["status"],
                rating=d["rating"]
            )
            driver_objs.append(drv)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(driver_objs)} Drivers."))

        # 3. Seed Vehicles
        vehicles_data = [
            {"plate": "NVA-1234", "make": "Isuzu", "model": "Elf NHR", "year": 2020, "capacity": "3000 kg", "status": "Moving"},
            {"plate": "HAB-5678", "make": "Toyota", "model": "Hiace Commuter", "year": 2021, "capacity": "15 Pax", "status": "Moving"},
            {"plate": "ABC-9012", "make": "Mitsubishi", "model": "L300 FB", "year": 2019, "capacity": "1000 kg", "status": "Maintenance"},
            {"plate": "DEF-3456", "make": "Hino", "model": "300 Series", "year": 2022, "capacity": "4500 kg", "status": "Moving"},
            {"plate": "XYZ-8888", "make": "Foton", "model": "Tornado", "year": 2018, "capacity": "2500 kg", "status": "Out of Service"},
        ]

        vehicle_objs = []
        for i, v in enumerate(vehicles_data):
            veh = Vehicle.objects.create(
                driver=driver_objs[i],
                plate_number=v["plate"],
                make=v["make"],
                model=v["model"],
                year=v["year"],
                vin=f"VIN{v['year']}{v['plate'].replace('-', '')}XXXX",
                status=v["status"],
                mileage=random.randint(20000, 150000),
                capacity=v["capacity"]
            )
            vehicle_objs.append(veh)
        self.stdout.write(self.style.SUCCESS(f"Generated {len(vehicle_objs)} Vehicles & assigned to Drivers."))

        # 4. Seed Maintenance Logs
        service_types = ['Preventive', 'Repair', 'Inspection', 'Cleaning']
        for v in vehicle_objs:
            for _ in range(random.randint(1, 4)):
                st = random.choice(service_types)
                MaintenanceLog.objects.create(
                    vehicle=v,
                    driver=v.driver,
                    service_type=st,
                    description=f"Routine {st.lower()} and general checkup.",
                    date=datetime.date.today() - datetime.timedelta(days=random.randint(1, 365)),
                    odometer_reading=v.mileage - random.randint(100, 5000),
                    cost=round(random.uniform(500.0, 15000.0), 2),
                    status=random.choice(['Completed', 'Completed', 'Scheduled']),
                    performed_by=random.choice(['AutoMechanic Leyte', 'Tacloban Casings Ltd', 'Internal Shop'])
                )
        self.stdout.write(self.style.SUCCESS("Generated Maintenance Logs history."))

        # 5. Seed Leyte Zones
        zones_data = [
            {"name": "Tacloban Mega Hub", "type": "Delivery Hub", "coords": "[[11.235, 125.000], [11.235, 125.015], [11.250, 125.015], [11.250, 125.000]]"},
            {"name": "Ormoc Central Dispatch", "type": "Delivery Hub", "coords": "[[10.995, 124.595], [10.995, 124.615], [11.015, 124.615], [11.015, 124.595]]"},
            {"name": "Maharlika Highway Restricted", "type": "Restricted", "coords": "[[11.160, 124.900], [11.160, 124.910], [11.170, 124.910], [11.170, 124.900]]"}
        ]
        for z in zones_data:
            Zone.objects.create(name=z["name"], zone_type=z["type"], coordinates=z["coords"])
        self.stdout.write(self.style.SUCCESS("Generated Leyte Maps Operational Zones."))

        # 6. Seed Terminals
        terminals_data = [
            ("Tacloban City Hub", 11.2430, 125.0081),
            ("Ormoc City Terminal", 11.0050, 124.6075),
            ("Baybay City Terminal", 10.6765, 124.7966),
            ("Palompon Port", 11.0489, 124.3831),
            ("Carigara Terminal", 11.3000, 124.6833),
            ("Maasin City Hub", 10.1333, 124.8333),
        ]
        term_map = {}
        for name, lat, lng in terminals_data:
            term_map[name] = Terminal.objects.create(name=name, location_lat=lat, location_lng=lng)
        self.stdout.write(self.style.SUCCESS("Bootstrapped Terminal Nodes."))

        # 7. Seed Routes
        routes = [
            {"name": "Tacloban - Ormoc Express", "origin": "Tacloban City Hub", "destination": "Ormoc City Terminal", "color": "#3b82f6", "coords": [(11.2430, 125.0081), (11.0050, 124.6075)]},
            {"name": "Tacloban - Baybay Route", "origin": "Tacloban City Hub", "destination": "Baybay City Terminal", "color": "#10b981", "coords": [(11.2430, 125.0081), (10.6765, 124.7966)]},
            {"name": "Ormoc - Palompon Shuttle", "origin": "Ormoc City Terminal", "destination": "Palompon Port", "color": "#f59e0b", "coords": [(11.0050, 124.6075), (11.0489, 124.3831)]},
            {"name": "Tacloban - Carigara Loop", "origin": "Tacloban City Hub", "destination": "Carigara Terminal", "color": "#8b5cf6", "coords": [(11.2430, 125.0081), (11.3000, 124.6833)]},
            {"name": "Ormoc - Maasin Line", "origin": "Ormoc City Terminal", "destination": "Maasin City Hub", "color": "#ef4444", "coords": [(11.0050, 124.6075), (10.1333, 124.8333)]}
        ]
        route_objs = []
        self.stdout.write("Seeding Leyte routes via OSRM...")
        for r in routes:
            osrm_data = self.get_osrm_route(r['name'], r['origin'], r['destination'], r['coords'])
            if osrm_data:
                ro = Route.objects.create(
                    name=r['name'],
                    origin=term_map[r['origin']],
                    destination=term_map[r['destination']],
                    distance_km=osrm_data['distance_km'],
                    est_travel_time=osrm_data['est_travel_time'],
                    status='Active',
                    color=r['color'],
                    geofence_radius_meters=500,
                    waypoints=osrm_data['waypoints'],
                    path_coordinates=osrm_data['path_coordinates']
                )
                route_objs.append(ro)
        self.stdout.write(self.style.SUCCESS("Done seeding routes!"))

        # 8. Seed Trips & Tickets
        active_vehicles = [v for v in vehicle_objs if v.status == 'Moving']
        for i in range(75):
            trip = Trip.objects.create(
                route=random.choice(route_objs),
                vehicle=random.choice(active_vehicles) if active_vehicles else None,
                dispatch_type=random.choice(['Fill-up', 'Scheduled']),
                ticket_color=random.choice(['Blue', 'Red', 'Yellow', 'Green']),
                status=random.choice(['Pending Vehicle', 'Standing By', 'Loading', 'Dispatched', 'Completed'])
            )
            
            # Create tickets
            for j in range(random.randint(5, 15)):
                Ticket.objects.create(
                    trip=trip,
                    passenger_name=f"Guest {random.randint(1000, 9999)}",
                    seat_number=f"{random.choice(['A','B','C'])}{random.randint(1,4)}",
                    fare=random.randint(250, 800),
                    status=random.choice(['Waiting', 'Boarded'])
                )
        self.stdout.write(self.style.SUCCESS("Generated Booking Trips and Tickets."))
        
        self.stdout.write(self.style.SUCCESS("\nComplete! Unified Data structures securely prepopulated."))
