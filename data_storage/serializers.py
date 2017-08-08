# -*- coding: utf-8 -*-
from rest_framework import serializers

from data_storage import models


''' Serializers to display data'''

class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a skill
    """
    class Meta:
        model = models.Skill
        fields = ('id', 'name')


class ChampionshipSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a championship
    """
    class Meta:
        model = models.Championship
        fields = ('id', 'name', 'year')


class AthleteSerializer(serializers.ModelSerializer):
    """
    Serializer to represent an athlete
    """
    skills = SkillSerializer(many=True)
    championships = ChampionshipSerializer(many=True)

    class Meta:
        model = models.Athlete
        fields = ('id', 'full_name', 'birth_date', 'skills', 'championships')


''' Serializers to validate the search dictionary '''

NAME_MATCH_CHOICES = [('exact', 'exact'),
                      ('iexact', 'iexact'),
                      ('icontains', 'icontains')]

EXP_MATCH_CHOICES = [('exact', 'exact'),
                     ('lower', 'lower'),
                     ('higher', 'higher')]

AGE_CHOICES = [('<18', '<18'),
               ('18-21', '18-21'),
               ('22-25', '22-25'),
               ('26-30', '26-30'),
               ('>30', '>30')]

class NameSerializer(serializers.Serializer):
    """
    Serializer to validate the name search criteria
    """
    value = serializers.CharField(max_length=255)
    match = serializers.ChoiceField(choices=NAME_MATCH_CHOICES)


class AgeSerializer(serializers.Serializer):
    """
    Serializer to validate the age search criteria
    """
    value = serializers.ChoiceField(choices=AGE_CHOICES)


class ExperienceSerializer(serializers.Serializer):
    """
    Serializer to validate the years_experience search criteria
    """
    value = serializers.IntegerField(min_value=0)
    match = serializers.ChoiceField(choices=EXP_MATCH_CHOICES)


class SkillsSerializer(serializers.Serializer):
    """
    Serializer to validate the skills search criteria
    """
    value = serializers.ListField(child=serializers.CharField(max_length=255))


class SearchSerializer(serializers.Serializer):
    """
    Main serializer to validate the search dictionary
    """
    ids_only = serializers.BooleanField(required=False)
    name = NameSerializer(required=False)
    age = AgeSerializer(required=False)
    years_experience = ExperienceSerializer(required=False)
    skills = SkillsSerializer(required=False)
