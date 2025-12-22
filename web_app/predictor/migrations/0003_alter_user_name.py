from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_remove_user_created_at_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
