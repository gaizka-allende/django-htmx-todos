from django.db import migrations

def add_suggestions(apps, schema_editor):
    Suggestions = apps.get_model('todos', 'Suggestions')
    suggestions = [
        {'id': 1, 'title': 'buy milk'},
        {'id': 2, 'title': 'buy cheese'},
        {'id': 3, 'title': 'go to the gym'},
        {'id': 4, 'title': 'clean the house'},
        {'id': 5, 'title': 'buy cake'},
        {'id': 6, 'title': 'buy chocolate'},
    ]
    Suggestions.objects.bulk_create([
        Suggestions(**suggestion) for suggestion in suggestions
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_suggestions),
    ] 