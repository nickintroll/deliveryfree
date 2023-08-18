from django import template

register = template.Library()

@register.simple_tag
def chat_dif_user(chat, request):
    return chat.get_oposite_user(request)