from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        # Add the new M2M field
        migrations.AddField(
            model_name='categoryoffer',
            name='categories',
            field=models.ManyToManyField(
                blank=True,
                related_name='category_offers_m2m',
                to='products.category',
            ),
        ),
        # Remove the old FK field
        migrations.RemoveField(
            model_name='categoryoffer',
            name='category',
        ),
        # Rename M2M to 'categories' with correct related_name
        migrations.AlterField(
            model_name='categoryoffer',
            name='categories',
            field=models.ManyToManyField(
                blank=False,
                related_name='category_offers',
                to='products.category',
            ),
        ),
    ]
