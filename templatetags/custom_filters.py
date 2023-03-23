from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
	return int(value) - int(arg)


@register.filter(name='format_price')
def format_number(value):
    if not value:
        return ''
    return '{:,.2f}'.format(value)