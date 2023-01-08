from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# To create a database structure.

class Task(models.Model):
    # This field is a foreign key that specifies a one-to-many relationship
    # with the 'User' model. This means that each task is associated with 
    # a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # This field is short string field that will store the title of the task
    title = models.CharField(max_length=255)
    
    # This field is a long text field that will store the description of the task
    description = models.TextField(null=True, blank=True)
    
    # This field is a boolean field that will store whether or not the task
    # has been completed
    complete = models.BooleanField(default=False)

    # This field is a data-time field that will store the date and time
    # when the task was created
    # The auto_now_add argument specifies that the field should be set to the
    # current date and time when the object is created.
    create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
