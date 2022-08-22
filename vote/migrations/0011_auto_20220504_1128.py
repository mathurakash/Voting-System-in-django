# Generated by Django 3.2.13 on 2022-05-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0010_votingdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='votes',
            field=models.ManyToManyField(blank=True, related_name='votes', to='vote.UserDetails'),
        ),
        migrations.DeleteModel(
            name='VotingDetail',
        ),
    ]
