# Generated by Django 2.0.8 on 2018-11-26 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('events', '0002_auto_20180513_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='EventPage',
        ),
    ]