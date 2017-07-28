from datetime import timedelta
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Post(models.Model):

    profile = models.ForeignKey('core.Profile', on_delete=CASCADE, related_name='posts')
    content = models.CharField(max_length=256, blank=True, null=False)
    image = models.ImageField(upload_to='posts/', null=True)
    created_at = models.DateTimeField(null=False)
    edited_at = models.DateTimeField(null=True)
    is_visible = models.BooleanField(default=True, null=False)

    def __str__(self):
        to_str = "%s posted by %s" % (self.content, self.profile)
        to_str += " at %s" % self.created_at
        if self.edited_at != self.created_at:
            to_str += " and edit at %s" % self.edited_at
        return to_str

    def edit(self, new_content):
        if self.is_editable():
            self.content = new_content
            self.edited_at = timezone.now()
            self.save(force_update=True)
            return True
        else:
            return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.created_at is None:
            self.created_at = timezone.now()
        if self.edited_at is None:
            self.edited_at = self.created_at
        super(Post, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.is_visible = False
        self.save()

    def is_editable(self):
        return (self.created_at + timedelta(seconds=59)) > timezone.now() and not self.image
