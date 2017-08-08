# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import list_route

from data_storage.models import Athlete
from data_storage import serializers
from data_storage.utils import search as search_utils


class AthletesViewSet(viewsets.ViewSet):
    model = Athlete
    serializer = serializers.AthleteSerializer

    @list_route(methods=['post'])
    def search(self, request):
        """
        This endpoint receives a dictionary with some search criteria and return the athletes that match it.
        """
        search_serializer = serializers.SearchSerializer(data=request.data)
        # First we validate if the search dictionary is correct
        if search_serializer.is_valid():
            search = search_serializer.data
            # Then we get the queryset with all the athletes so we can filter on them
            athletes = self.model.objects

            # If name criteria, filter all the athletes with the given name in full_name
            if 'name' in search:
                athletes = search_utils.search_by_name(athletes, search['name'])

            # If age criteria, filter all the athletes with birth_date included in the requested range
            if 'age' in search:
                athletes = search_utils.search_by_age(athletes, search['age'])

            # If years_experience criteria, filter all the athletes with the desired experience
            if 'years_experience' in search:
                athletes = search_utils.search_by_experience(athletes, search['years_experience'])

            # If skills criteria, filter all the athletes with the requested skills or any of their children
            if 'skills' in search:
                athletes = search_utils.search_by_skills(athletes, search['skills'])

            if search.get('ids_only'):
                # If ids_only is true then we only return a list with all the athlete ids
                return Response({"athlete_ids": athletes.values_list('id', flat=True)})
            else:
                # Otherwise we return the full data, defined in the AthleteSerializer
                serializer = self.serializer(athletes, many=True)
                return Response(serializer.data)
        else:
            raise exceptions.ValidationError(search_serializer.errors)
