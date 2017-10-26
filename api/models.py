from django.db import models


class TaskList(models.Model):
    """This class represents the TaskList model."""

    owners = models.ManyToManyField('auth.User', related_name='task_lists')
    name = models.CharField(max_length=255, blank=False, unique=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class ListItem(models.Model):
    """This class represents the ListItem model."""

    STATES = (
        ('DONE', 'Done'),
        ('UNDONE', 'Undone')
    )

    owners = models.ManyToManyField('auth.User', related_name='list_items')
    task_list = models.ForeignKey(
        TaskList, related_name='list_items', default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, unique=False)
    state = models.CharField(
        max_length=255, choices=STATES, default='UNDONE', blank=False, unique=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)
