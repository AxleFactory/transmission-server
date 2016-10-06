from django.db import models
from django.utils import timezone


class ModelWithDates(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Action(ModelWithDates):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CallAction(Action):
    call_script = models.TextField(max_length=500)


class TextAction(Action):
    message_content = models.TextField(max_length=200)


class Assignment(ModelWithDates):
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    instructions = models.CharField(max_length=200)
    expiration = models.DateTimeField('expiration date')
    require_call_first = models.BooleanField(default=False)
    call_actions = models.ManyToManyField(CallAction, blank=True)
    text_actions = models.ManyToManyField(TextAction, blank=True)

    @property
    def expired(self):
        return timezone.now() > self.expiration

    def __str__(self):
        return self.name

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'expiration': self.expiration.isoformat(),
            'require_call_first': self.require_call_first,
            'call_actions': [{
                                 'id': a.id,
                                 'name': a.name,
                                 'call_script': a.call_script,
                             } for a in self.call_actions.all()],
            'text_actions': [{
                                 'id': a.id,
                                 'name': a.name,
                                 'message_content': a.message_content,
                             } for a in self.text_actions.all()],
        }
