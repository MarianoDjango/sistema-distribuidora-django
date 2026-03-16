from django import template

register = template.Library()

@register.filter
def precio_ars(value):
    try:
        return '{:,.2f}'.format(float(value)).replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return value