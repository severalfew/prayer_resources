# Generated by Django 3.2.8 on 2021-10-15 17:14

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_rename_intro_curatorpage_about_me'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resourcepage',
            old_name='source_link',
            new_name='source',
        ),
        migrations.AlterField(
            model_name='prayerresource',
            name='prayer',
            field=wagtail.core.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='quotationresource',
            name='quotation',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
