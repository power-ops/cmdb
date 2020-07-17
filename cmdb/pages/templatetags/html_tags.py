from django import template

register = template.Library()


@register.filter(name='addClass')
def addClass(value, args):
    css_classes = value.field.widget.attrs.get('class', '').split(' ')
    if css_classes and args not in css_classes:
        css_classes = '%s %s' % (css_classes, args)
    return value.as_widget(attrs={'class': css_classes})



