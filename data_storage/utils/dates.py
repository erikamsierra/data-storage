# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta


def get_date_range(age_range_str):
    """
    Given a range str with format YY-YY returns the corresponding dates
    """
    today = datetime.date.today()
    max_date = (today - relativedelta(years=int(age_range_str[0:2])))
    min_date = (today - relativedelta(years=int(age_range_str[3:5])+1))
    return min_date, max_date


def calculate_year(num_years_ago):
    """
    Returns which year it was X years ago
    """
    today = datetime.date.today()
    new_date = (today - relativedelta(years=int(num_years_ago)))
    return new_date.year
