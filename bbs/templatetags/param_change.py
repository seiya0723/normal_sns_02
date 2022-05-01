from django import template

register = template.Library()

# @から始まるのは、デコレーター。次に書いた関数にデコレーターの機能を追加する。
@register.simple_tag()
def url_replace(request, key, value):
    copied      = request.GET.copy()
    copied[key] = value
    return copied.urlencode()  # category=1&search=&page=2
