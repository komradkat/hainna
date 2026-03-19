from django.core.management.base import BaseCommand
import datetime
import random
from fleet.models import Driver, Vehicle, MaintenanceLog, Zone

class Command(BaseCommand):
    help = 'Seeds holistic Fleet data (Drivers, Vehicles, Zones, Maintenance)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Initializing holistic seed algorithms...")

        # 1. Clear old data securely
        self.stdout.write("Wiping legacy Fleet modules...")
        MaintenanceLog.objects.all().delete()
        Vehicle.objects.all().delete()
        Driver.objects.all().delete()
        Zone.objects.all().delete()

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
            {"plate": "NVA-1234", "make": "Isuzu", "model": "Elf NHR", "year": 2020, "capacity": "3000 kg", "status": "Active"},
            {"plate": "HAB-5678", "make": "Toyota", "model": "Hiace Commuter", "year": 2021, "capacity": "15 Pax", "status": "Active"},
            {"plate": "ABC-9012", "make": "Mitsubishi", "model": "L300 FB", "year": 2019, "capacity": "1000 kg", "status": "Maintenance"},
            {"plate": "DEF-3456", "make": "Hino", "model": "300 Series", "year": 2022, "capacity": "4500 kg", "status": "Active"},
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
        # Simple square/polygon coordinates around major Leyte Hubs
        zones_data = [
            {
                "name": "Tacloban Mega Hub",
                "type": "Delivery Hub",
                "coords": "[[11.235, 125.000], [11.235, 125.015], [11.250, 125.015], [11.250, 125.000]]"
            },
            {
                "name": "Ormoc Central Dispatch",
                "type": "Delivery Hub",
                "coords": "[[10.995, 124.595], [10.995, 124.615], [11.015, 124.615], [11.015, 124.595]]"
            },
            {
                "name": "Maharlika Highway Restricted Zone (Construction)",
                "type": "Restricted",
                "coords": "[[11.160, 124.900], [11.160, 124.910], [11.170, 124.910], [11.170, 124.900]]"
            }
        ]
        
        for z in zones_data:
            Zone.objects.create(
                name=z["name"],
                zone_type=z["type"],
                coordinates=z["coords"]
            )
        self.stdout.write(self.style.SUCCESS(f"Generated {len(zones_data)} formal Leyte Maps Operational Zones."))

        self.stdout.write(self.style.SUCCESS("\nDone! Full system data structures accurately pre-populated."))
