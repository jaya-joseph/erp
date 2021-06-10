from django import template

register = template.Library()


@register.filter
def check_designation(designations, designation):
    """
    :param designations: status value or list of status values
    :type Django.db.models.QuerySet:
    :return: return queryset
    """
    return bool(designations.filter(designation=designation).count())
