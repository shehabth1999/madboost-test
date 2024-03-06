from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='romanize_division')
def romanize_division(value):
  if value == 1:
    return 'IV'
  elif value == 2:
    return 'III'
  elif value == 3:
    return 'II'
  elif value == 4:
    return 'I'
  else:
    return value
  
@register.filter(name='server_name')
def server_name(value):
  if value == 1:
    return 'Europa'
  elif value == 2:
    return 'America'
  elif value == 3:
    return 'Asia'
  elif value == 4:
    return 'Africa'
  elif value == 5:
    return 'Oceania'
  else:
    return value
  
@register.filter(name='format_time_difference')
def format_time_difference(updated_at):
  now = timezone.now()
  time_difference = now - updated_at

  days = time_difference.days
  months = days // 30
  years = days // 365

  if years >= 1:
    return f'{years} {"year" if years == 1 else "years"}'
  elif months >= 1:
    return f'{months} {"month" if months == 1 else "months"}'
  elif days >= 1:
    return f'{days} {"day" if days == 1 else "days"}'
  else:
    return 'today'
  
@register.filter(name='romanize_division_original')
def romanize_division_original(value):
  if value == 1:
    return 'I'
  elif value == 2:
    return 'II'
  elif value == 3:
    return 'III'
  elif value == 4:
    return 'IV'
  else:
    return value
  
@register.filter(name='ten_romanize_division')
def ten_romanize_division(value):
  if value == 1:
    return 'X'
  elif value == 2:
    return 'IX'
  elif value == 3:
    return 'VIII'
  elif value == 4:
    return 'VII'
  elif value == 5:
    return 'VI'
  elif value == 6:
    return 'V'
  elif value == 7:
    return 'IV'
  elif value == 8:
    return 'III'
  elif value == 9:
    return 'II'
  elif value == 10:
    return 'I'
  else:
    return value
  
@register.filter(name='five_romanize_division')
def five_romanize_division(value):
  if value == 1:
    return 'V'
  elif value == 2:
    return 'IV'
  elif value == 3:
    return 'III'
  elif value == 4:
    return 'II'
  elif value == 2:
    return 'I'
  else:
    return value