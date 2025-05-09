from django.db import migrations

import csv

def create_store_data(apps, schema_editor):
    Store = apps.get_model('main', 'Store')
    with open('main/csv_data/timezones.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            Store.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str'],
            )

def populate_store_start_end_time(apps, schema_editor):
    Store = apps.get_model('main', 'Store')
    StoreTiming = apps.get_model('main', 'StoreTiming')
    with open('main/csv_data/menu_hours.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            store = Store.objects.filter(store_id=row['store_id']).first()
            if store:
                store_timing = StoreTiming.objects.create(
                    store=store,
                    day=row['dayOfWeek'],
                    start_time=row['start_time_local'],
                    end_time=row['end_time_local'],
                )
                print(store_timing)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_store_data,reverse_code=migrations.RunPython.noop),
        migrations.RunPython(populate_store_start_end_time,reverse_code=migrations.RunPython.noop),
    ]
