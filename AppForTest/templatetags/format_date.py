import datetime

from django import template

register = template.Library()

def format_date(value: datetime.datetime):
    return value.strftime("%d.%m.%Y в %H:%M")

register.filter("format_date", format_date)