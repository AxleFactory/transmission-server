from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

mustache_docs_url = "https://mustache.github.io/mustache.5.html"
template_field_help_text = "%s will be evaluated as a <a href='%s' target='_blank'>mustache template</a>."


class ModelWithDates(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Action(ModelWithDates):
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CallAction(Action):
    call_script = models.TextField(
        max_length=500,
        help_text=template_field_help_text % ("Call script", mustache_docs_url)
    )


class TextAction(Action):
    message_content = models.TextField(
        max_length=200,
        help_text=template_field_help_text % ("Message content", mustache_docs_url)
    )


class Assignment(ModelWithDates):
    name = models.CharField(max_length=30)
    active = models.BooleanField(
        default=False,
        help_text="Only assignments marked 'Active' will be shown to users. See <a href='/all-assignments.json' target='_blank'>all-assignments.json</a> for an unfiltered view containing expired and inactive assignments.",
        db_index=True
    )
    description = models.CharField(max_length=200)
    instructions = models.CharField(max_length=200)
    expiration = models.DateTimeField('expiration date', db_index=True)
    priority = models.PositiveSmallIntegerField(
        default=0,
        help_text="Assignments will be sorted from highest to lowest priority before being shown to users.  Assignments with the same priority will be sorted by expiration date.",
        validators=[MaxValueValidator(100)],
        db_index=True
    )
    require_call_first = models.BooleanField(
        default=False,
        help_text="If selected, the user will have to complete a call action for the current assignment before text actions become available."
    )
    call_actions = models.ManyToManyField(CallAction, blank=True)
    text_actions = models.ManyToManyField(TextAction, blank=True)

    class Meta:
        ordering = ['-priority', 'expiration']

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
