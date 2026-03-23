from django.utils import timezone
from users.models import CustomUser
from fleet.models import Terminal, Route, Driver, Vehicle, MaintenanceLog
from booking.models import Trip, Ticket
import random
from datetime import timedelta

print('Seeding data...')

# 1. Terminals
terminals_data = [
    {'name': 'Manila Central', 'lat': 14.5995, 'lng': 120.9842},
    {'name': 'Cubao Terminal', 'lat': 14.6186, 'lng': 121.0543},
    {'name': 'Pasay Terminal', 'lat': 14.5378, 'lng': 121.0014},
    {'name': 'Baguio Terminal', 'lat': 16.4023, 'lng': 120.5960},
    {'name': 'Cebu Hub', 'lat': 10.3157, 'lng': 123.8854},
]
terminals = []
for td in terminals_data:
    t, _ = Terminal.objects.get_or_create(name=td['name'], defaults={'location_lat': td['lat'], 'location_lng': td['lng']})
    terminals.append(t)
    
# 2. Routes
routes = []
for i in range(len(terminals)):
    for j in range(i+1, len(terminals)):
        r, _ = Route.objects.get_or_create(
            name=f"{terminals[i].name} to {terminals[j].name}",
            origin=terminals[i],
            destination=terminals[j],
            defaults={'distance_km': random.randint(50, 400), 'est_travel_time': f"{random.randint(1, 6)}h 30m"}
        )
        routes.append(r)

# 3. Drivers
drivers = []
for i in range(25):
    d, _ = Driver.objects.get_or_create(
        first_name=f"Driver{i}",
        last_name=f"Smith{i}",
        license_number=f"LIC-{random.randint(1000,9999)}-{i}",
        defaults={
            'license_expiry': timezone.now().date() + timedelta(days=365),
            'contact_number': f"0917{random.randint(1000000,9999999)}",
            'status': random.choice(['Active', 'Active', 'Off Duty']),
            'rating': round(random.uniform(4.0, 5.0), 1)
        }
    )
    drivers.append(d)

# 4. Vehicles
vehicles = []
for i in range(20):
    v, _ = Vehicle.objects.get_or_create(
        plate_number=f"ABC-{random.randint(1000,9999)}",
        defaults={
            'driver': drivers[i] if i < len(drivers) else None,
            'make': random.choice(['Toyota', 'Nissan', 'Ford']),
            'model': random.choice(['Hiace', 'Urvan', 'Transit']),
            'year': random.randint(2018, 2024),
            'status': random.choice(['Active', 'Active', 'Active', 'Maintenance', 'Active', 'Moving']),
            'mileage': random.randint(10000, 150000),
            'capacity': '15 Seater'
        }
    )
    vehicles.append(v)

# 5. Maintenance
for v in vehicles:
    if v.status == 'Maintenance':
        MaintenanceLog.objects.get_or_create(
            vehicle=v,
            date=timezone.now().date(),
            defaults={
                'service_type': random.choice(['Preventive', 'Repair']),
                'description': 'Check engine light diagnostic routine.',
                'status': 'Scheduled',
                'cost': random.randint(1500, 8000)
            }
        )

# 6. Trips and Tickets
for i in range(30):
    trip = Trip.objects.create(
        route=random.choice(routes),
        vehicle=random.choice(vehicles) if random.random() > 0.3 else None,
        dispatch_type=random.choice(['Fill-up', 'Scheduled']),
        status=random.choice(['Pending Vehicle', 'Standing By', 'Loading', 'Dispatched', 'Completed'])
    )
    
    num_tickets = random.randint(5, 15)
    for j in range(num_tickets):
        Ticket.objects.create(
            trip=trip,
            passenger_name=f"Passenger {random.randint(100, 999)}",
            seat_number=str(j+1),
            fare=random.randint(300, 1500),
            status=random.choice(['Waiting', 'Boarded'])
        )
        
print(f'Successfully seeded {len(terminals)} terminals, {len(routes)} routes, {len(drivers)} drivers, {len(vehicles)} vehicles, and trips/tickets.')
