from django.db import migrations


def clear_default_avatar(apps, schema_editor):
    Profile = apps.get_model('authentication', 'Profile')
    Profile.objects.filter(avatar='avatars/default.png').update(avatar=None)


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.RunPython(clear_default_avatar, migrations.RunPython.noop),
    ]
