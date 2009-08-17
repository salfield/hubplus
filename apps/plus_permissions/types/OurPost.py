
# Permissions for OurPost, an example 
from django.db import models
from apps.plus_permissions.models import SetSliderOptions, SetAgentSecurityContext, SetAgentDefaults, SetPossibleTypes
from apps.plus_permissions.interfaces import InterfaceReadProperty, InterfaceWriteProperty, InterfaceCallProperty


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from apps.hubspace_compatibility.models import TgGroup

from apps.plus_permissions.OurPost import *

# This represents a typical model type from another django or pinax app



# This represents a typical model type from another django or pinax app
content_type = OurPost


# Here's the wrapping we have to put around it.

class OurPostViewer: 
    title = InterfaceReadProperty
    body = InterfaceReadProperty

class OurPostEditor: 
    title = InterfaceWriteProperty
    body = InterfaceWriteProperty
    delete = InterfaceCallProperty

class OurPostCommentor:
    pass


from apps.plus_permissions.interfaces import add_type_to_interface_map, get_interface_map

OurPostInterfaces = {'Viewer':OurPostViewer,
                     'Editor':OurPostEditor,
                     'Commentor':OurPostCommentor}

add_type_to_interface_map(OurPost, OurPostInterfaces)


SliderOptions = {'InterfaceOrder':['Viewer', 'Editor','Commentor']}
SetSliderOptions(TgGroup, SliderOptions)


# hmmm ... fake this for a minute
def force_add() :
    add_type_to_interface_map(OurPost,OurPostInterfaces)
    print "3zz33", get_interface_map(OurPost)

