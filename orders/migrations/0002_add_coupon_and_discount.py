# Generated manually for adding coupon/discount fields
from django.db import migrations, models
import django.db.models.deletion


def create_migration(apps, schema_editor):
    # this function isn't necessary; operations handle it
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
    ]
