# -*- coding: utf-8 -*-
from django.db.models import Q

from data_storage.utils.dates import get_date_range, calculate_year
from data_storage.models import Athlete, Skill


def search_by_name(athletes, name_search):
    """
    Filters the given athletes queryset by name using the parameters in name_search
    """
    if name_search['match'] != 'exact':
        # If search criteria is not exact we build the query to use iexact/icontains operators
        kwargs = {'{}__{}'.format('full_name', name_search['match']): name_search['value']}
        athletes = athletes.filter(Q(**kwargs))
    else:
        # Otherwise we simply look for users with exactly the requested name in full_name
        athletes = athletes.filter(full_name=name_search['value'])

    return athletes


def search_by_age(athletes, age_search):
    """
    Filters the given athletes queryset by age using the parameters in age_search
    """
    if age_search['value'] == "<18":
        age_search['value'] = "00-17"
    if age_search['value'] == ">30":
        age_search['value'] = "31-99"
    # We need to calculate the actual dates corresponding to the requested age range
    min_date, max_date = get_date_range(age_search['value'])

    # Once we have the dates we just need filter all users with birth_date in that range
    return athletes.filter(birth_date__range=[min_date, max_date])


def search_by_experience(athletes, exp_search):
    """
    Filters the given athletes queryset by experience using the parameters in exp_search
    """
    # We need to calculate the target year first from the requested number of years
    year = calculate_year(exp_search['value'])
    if exp_search['match'] == 'exact':
        # If search is exact we look for athletes whose first championship was on the target year
        # This means championships exactly on the target year but also not other championships before
        athletes = athletes.filter(championships__year=year).exclude(championships__year__lt=year).distinct()
    elif exp_search['match'] == 'lower':
        # If search is lower we exclude all the athletes with championships before or on the target year
        athletes = athletes.exclude(championships__year__lte=year).distinct()
    elif exp_search['match'] == 'higher':
        # If search is higher we filter all the athletes with championships before the target year
        athletes = athletes.filter(championships__year__lt=year).distinct()

    return athletes


def search_by_skills(athletes, skills_search):
    """
    Filters the given athletes queryset by skills using the parameters in skills_search
    """
    skill_names_lower = [s.lower() for s in skills_search['value']]
    # From the dictionary with skill names we get the actual skills that match those names
    skills = Skill.objects.filter(name__in=skill_names_lower)
    # From the queryset with all the requested skills we also get their children skills
    skills = skills.get_descendants(include_self=True)

    # Finally, we get all the athletes that have at least one of the requested skills
    if skills:
        athletes = athletes.filter(skills__in=skills).distinct()
    else:
        # If no valid skills requested we return an empty list of athletes
        athletes = Athlete.objects.none()

    return athletes
