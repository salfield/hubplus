
# Permissions for OurPost, an example                                                                                                                        
from django.db import models

from models import Interface, Slider, SliderOption, SecurityTag, PermissionManager
from models import get_permission_system, default_admin_for, InterfaceReadProperty, InterfaceWriteProperty

from apps.profiles.models import Profile

from apps.hubspace_compatibility.models import TgGroup

from django.db.models.signals import post_save

import ipdb

# Here's the wrapping we have to put around it.                                                                                                              

def read_interface(name,id) :
    class ReadInterface(Interface) : 
        @classmethod
        def get_id(self):
            return id
    setattr(ReadInterface,name,InterfaceReadProperty(name))
    return ReadInterface
        
class ProfileViewer(Interface) : 

    about = InterfaceReadProperty('about')
    location = InterfaceReadProperty('location')
    website = InterfaceReadProperty('website')
    homeplace = InterfaceReadProperty('homeplace')
    organisation = InterfaceReadProperty('organisation')
    role = InterfaceReadProperty('role')

    display_name = InterfaceReadProperty('display_name')
    title = InterfaceReadProperty('title')

    @classmethod
    def get_id(self) : 
        return 'Profile.Viewer'

ProfileEmailAddressViewer = read_interface('email_address','Profile.EmailAddressViewer')
ProfileHomeViewer = read_interface('home','Profile.HomeViewer')
ProfileWorkViewer = read_interface('work','Profile.WorkViewer')
ProfileMobileViewer = read_interface('mobile','Profile.MobileViewer')
ProfileFaxViewer = read_interface('fax','Profile.FaxViewer')
ProfileAddressViewer = read_interface('address','Profile.AddressViewer')
ProfileSkypeViewer = read_interface('skype_id','Profile.SkypeViewer')
ProfileSipViewer = read_interface('sip_id','Profile.SipViewer')


class ProfileEditor(Interface) : 
    pk = InterfaceReadProperty('pk')
    about = InterfaceWriteProperty('about')
    location = InterfaceWriteProperty('location')
    website = InterfaceWriteProperty('website')

    organisation = InterfaceWriteProperty('organisation')
    role = InterfaceWriteProperty('role')

    display_name = InterfaceWriteProperty('display_name')
    title = InterfaceWriteProperty('title')

    mobile = InterfaceWriteProperty('mobile')
    email_address = InterfaceWriteProperty('email_address')
    address = InterfaceWriteProperty('address')
    skype_id = InterfaceWriteProperty('skype_id')
    sip_id = InterfaceWriteProperty('sip_id')
    website = InterfaceWriteProperty('website')
    homeplace = InterfaceWriteProperty('homeplace')
    
    @classmethod
    def get_id(self) :
        return 'Profile.Editor'


def display_name(x) :
    if x.display_name : return x.display_name 
    if x.username : return x.username
    if x.name : return x.name
    return '%s'%x

class ProfilePermissionManager(PermissionManager) :
    def register_with_interface_factory(self,interface_factory) :
        self.interface_factory = interface_factory
        interface_factory.add_type(Profile)
        interface_factory.add_interface(Profile,'Viewer',ProfileViewer)
        interface_factory.add_interface(Profile,'Editor',ProfileEditor)
        interface_factory.add_interface(Profile,'EmailAddressViewer',ProfileEmailAddressViewer)
        interface_factory.add_interface(Profile,'HomeViewer',ProfileHomeViewer)
        interface_factory.add_interface(Profile,'WorkViewer',ProfileWorkViewer)
        interface_factory.add_interface(Profile,'MobileViewer',ProfileMobileViewer)
        interface_factory.add_interface(Profile,'FaxViewer',ProfileFaxViewer)

        interface_factory.add_interface(Profile,'AddressViewer',ProfileAddressViewer)
        interface_factory.add_interface(Profile,'SkypeViewer',ProfileSkypeViewer)
        interface_factory.add_interface(Profile,'SipViewer',ProfileSipViewer)


    def setup_defaults(self,resource, owner, creator) :
        options = self.make_slider_options(resource,owner,creator)
        self.save_defaults(resource,owner,creator)

        interfaces = self.get_interfaces()

        slide = interfaces['Viewer'].make_slider_for(resource,options,owner,0,creator)
        slide = interfaces['Editor'].make_slider_for(resource,options,owner,2,creator)
        slide = interfaces['EmailAddressViewer'].make_slider_for(resource,options,owner,1,creator)
        slide = interfaces['HomeViewer'].make_slider_for(resource,options,owner,2,creator)
        slide = interfaces['WorkViewer'].make_slider_for(resource,options,owner,2,creator)
        slide = interfaces['MobileViewer'].make_slider_for(resource,options,owner,2,creator)
        slide = interfaces['FaxViewer'].make_slider_for(resource,options,owner,2,creator)

        slide = interfaces['AddressViewer'].make_slider_for(resource,options,owner,2,creator)
        slide = interfaces['SkypeViewer'].make_slider_for(resource,options,owner,1,creator)


    def main_json_slider_group(self,resource) :
        json = self.json_slider_group('Profile Permissions', 'Use these sliders to set overall permissions on your profile', resource, ['Viewer','Editor'], [0,0], [[0,1]])
        return json

    def make_slider_options(self,resource,owner,creator) :
        options = [
            SliderOption('World',get_permission_system().get_anon_group()),
            SliderOption('All Members',get_permission_system().get_all_members_group()),
            SliderOption('Me',owner),
            SliderOption('Hosts',creator)

        ]

        default_admin = default_admin_for(owner)

        if not default_admin is None :
            options.append( SliderOption(default_admin.display_name,default_admin) )

        return options
        
        #ipdb.set_trace()


        
get_permission_system().add_permission_manager(Profile,ProfilePermissionManager(Profile))




