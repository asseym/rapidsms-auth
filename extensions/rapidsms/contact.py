from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from rapidsms.models import ContactBase

class AuthenticatedContact(models.Model):
    """
    This extension for Contacts allows developers to tie a Contact (and potentially
    a phone number) to an authenticated django User object.  In order for this to
    work correctly, it's important to add the following line to settings.py:
    
    AUTH_PROFILE_MODULE = 'rapidsms.Contact'
    
    When this is set up properly, django will automatically load the appropriate
    Contact object as the User's "profile" (accessible via get_profile()) 
    upon login.
    
    See http://docs.djangoproject.com/en/dev/topics/auth/ under the section 
    'Storing additional information about users' for more information.
    """
    user = models.ForeignKey(User, unique=True)
    perms = models.ManyToManyField(Permission, blank=True)
    
    @property
    def user_permissions(self):
        """
        There are basically two options for 
        """
        if self.user:
            return self.user.permissions
        else:
            return self.perms
    
    def save(self, force_insert=False, force_update=False, using=None):
        super(ContactBase, self).save(force_insert, force_update, using)
        if self.user and not self.user.user_permissions:
            self.user.user_permissions = self.perms
            self.perms = None
            self.save()

    class Meta:
        abstract = True
