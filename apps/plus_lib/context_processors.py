
from django.conf import settings
from utils import hub_name,  hub_name_plural, main_hub_name

def get_area(context):
    path = context.path.split('/')
    return path[1]

def get_group_or_hub_name(context) :
    area = get_area(context)
    if area == 'groups' :
        return 'Group'
    else :
        return hub_name()
    
def configs(context):
    # This function is a context processor to load the base.html template with some other standard 
    # values pulled from local_settings.py
    if get_area(context) in ['groups','regions','hubs'] :
        is_group_type = True
    else :
        is_group_type = False

    try:
        SETTINGS = {
            'COPYRIGHT_HOLDER' : settings.COPYRIGHT_HOLDER,
            'PROJECT_THEME': settings.PROJECT_THEME,
            'WELCOME_PAGE' : 'clients/%s/welcome.html' % settings.PROJECT_THEME,
            'INTRO_BAR' : 'clients/%s/intro_bar.html' % settings.PROJECT_THEME,
            "HOME_TABS" : 'home/clients/%s/tabbed_subs.html' % settings.PROJECT_THEME,
            'SITE_NAME' : settings.SITE_NAME,
            'SITE_NAME_SHORT': settings.SITE_NAME_SHORT,
            'HUB_NAME' : hub_name(),
            'HUB_NAME_PLURAL' : hub_name_plural(),
            "MAIN_HUB_NAME" : main_hub_name(),
            'PROJECT_NAME' : settings.PROJECT_NAME,
            'CURRENT_AREA': get_area(context),
            'GROUP_OR_HUB' : get_group_or_hub_name(context),
            'IS_GROUP_TYPE' : is_group_type,
            'SUPPORT_EMAIL' : settings.SUPPORT_EMAIL,
            'EXPLORE_NAME' : settings.EXPLORE_NAME, 

            'EXPLORE_SEARCH_TITLE' : settings.EXPLORE_SEARCH_TITLE,
            'MEMBER_SEARCH_TITLE' : settings.MEMBER_SEARCH_TITLE,
            'GROUP_SEARCH_TITLE' : settings.GROUP_SEARCH_TITLE,
            'HUB_SEARCH_TITLE' : settings.HUB_SEARCH_TITLE,
            'TAG_SEARCH_TITLE' : settings.TAG_SEARCH_TITLE,
            'SIDE_SEARCH_TITLE' : settings.SIDE_SEARCH_TITLE,

            'GROUPS_INTRO_BOX' : 'groups_intro_bar',
            'MEMBERS_INTRO_BOX' : 'clients/%s/intro_box.html' % settings.PROJECT_THEME,
            'EXPLORE_INTRO_BOX' : 'explore_intro_bar', 
            'HUBS_INTRO_BOX' : 'hubs_intro_bar',
            
            'STATUS_COPY' : settings.STATUS_COPY,

            }

        return SETTINGS
        
    except Exception, e:
        import ipdb
        #ipdb.set_trace()
        print e
        raise e
