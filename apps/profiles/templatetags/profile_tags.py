from django import template
from apps.plus_permissions.api import secure_wrap, TemplateSecureWrapper
from apps.plus_permissions.models import GenericReference

register = template.Library()

def show_profile(context, profile):
    if isinstance(profile, GenericReference):
        profile = profile.obj
    homehub = profile.homeplace.tggroup_set.filter(level='member')[0]
    #profile = TemplateSecureWrapper(secure_wrap(profile, context['request'].user, interface_names=['Viewer'], required_interfaces=['Viewer']))
    return {"homehub":homehub, "profile":profile}
register.inclusion_tag("profile_item.html", takes_context=True)(show_profile)

def clear_search_url(request):
    getvars = request.GET.copy()
    if 'search' in getvars:
        del getvars['search']
    if len(getvars.keys()) > 0:
        return "%s?%s" % (request.path, getvars.urlencode())
    else:
        return request.path
register.simple_tag(clear_search_url)


