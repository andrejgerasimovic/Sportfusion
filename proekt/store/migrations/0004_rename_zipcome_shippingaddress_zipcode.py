# Generated by Django 4.1.7 on 2023-05-21 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_orderitem_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcome',
            new_name='zipcode',
        ),
    ]