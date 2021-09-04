from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
from django.utils.translation import ugettext_lazy as _

class Todo(TrackingModel):

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    is_complete = models.BooleanField(_("is complete"), default = False)
    owner  = models.ForeignKey(to = User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
    
    
    
