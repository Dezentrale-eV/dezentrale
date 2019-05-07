from django import template

register = template.Library()

@register.simple_tag
def get_title():
    return 'get_Title Tag successful'

@register.filter(name='get_num_color')
def get_num_color(value):
    if value < 1:
        return "#FF0000"
    elif value <= 3 :
        return "#FF7400"
    else:
        return "#00CC00"