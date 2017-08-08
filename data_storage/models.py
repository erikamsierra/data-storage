# -*- coding: utf-8 -*-
import datetime

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

YEAR_CHOICES = []
for r in range(1900, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))


class Athlete(models.Model):
    """
    Represents an athlete
    """
    full_name = models.CharField(max_length=255, db_index=True)
    birth_date = models.DateField(db_index=True)
    skills = models.ManyToManyField('Skill', related_name="athletes")
    championships = models.ManyToManyField('Championship', related_name="athletes")

    def __str__(self):
        return u'{}'.format(self.full_name)


class Skill(MPTTModel):
    """
    Represents a skill
    """
    name = models.CharField(max_length=50, unique=True, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return u'{}'.format(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Skill, self).save(*args, **kwargs)


class Championship(models.Model):
    """
    Represents a championship
    """
    name = models.CharField(max_length=255, db_index=True)
    year = models.IntegerField(choices=YEAR_CHOICES)

    class Meta:
        unique_together = ('name', 'year')

    def __str__(self):
        return u'{} {}'.format(self.name, self.year)
