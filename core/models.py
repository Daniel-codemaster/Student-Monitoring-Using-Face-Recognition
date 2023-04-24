from django.db import models
import uuid


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    is_out_of_bound = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Location'

class Camera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Camera'

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forename = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    picture_url = models.ImageField(upload_to='students/')
    number = models.CharField(max_length=16)
    Last_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.forename} {self.surname}"

    class Meta:
        db_table = 'Student'


class Notification(models.Model):
    STATUS_CHOICES = (
        ('Failed', 'Failed'),
        ('Sent', 'Sent'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    attachment_url = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} ({self.status}) - {self.location}"

    class Meta:
        db_table = 'Notification'

class Whatsapp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=32)
    token = models.CharField(max_length=1024)
    template = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.phone
