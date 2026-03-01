from django.db import migrations


def create_socialapp_placeholder(apps, schema_editor):
    try:
        SocialApp = apps.get_model('socialaccount', 'SocialApp')
    except LookupError:
        # allauth not installed/configured yet; skip
        return

    Site = apps.get_model('sites', 'Site')
    from django.conf import settings

    site_id = getattr(settings, 'SITE_ID', 1)

    # Avoid duplicate creation
    if SocialApp.objects.filter(provider='google', client_id='PLACEHOLDER').exists():
        return

    # Create or get site
    try:
        site = Site.objects.get(id=site_id)
    except Site.DoesNotExist:
        site = None

    socialapp = SocialApp.objects.create(
        provider='google',
        name='Google (placeholder)',
        client_id='PLACEHOLDER',
        secret='PLACEHOLDER',
        key=''
    )

    if site:
        socialapp.sites.add(site)


def remove_socialapp_placeholder(apps, schema_editor):
    try:
        SocialApp = apps.get_model('socialaccount', 'SocialApp')
    except LookupError:
        return

    SocialApp.objects.filter(provider='google', client_id='PLACEHOLDER').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_socialapp_placeholder, remove_socialapp_placeholder),
    ]
