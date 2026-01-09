from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def sort_url(context, field):
    """
    Gera URL de ordenação mantendo os parâmetros existentes
    """
    request = context['request']
    params = request.GET.copy()

    current_order = params.get('order_by', '')

    if current_order == field:
        new_order = f'-{field}'
    elif current_order == f'-{field}':
        new_order = field
    else:
        new_order = field

    params['order_by'] = new_order

    return f"?{params.urlencode()}"


@register.simple_tag(takes_context=True)
def sort_icon_class(context, field):
    """
    Retorna a classe do ícone Bootstrap Icons
    """
    request = context['request']
    current_order = request.GET.get('order_by', '')

    if current_order == field:
        return 'bi-arrow-up'
    elif current_order == f'-{field}':
        return 'bi-arrow-down'
    else:
        return 'bi-arrow-down-up'
