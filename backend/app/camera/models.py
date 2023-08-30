from django.db import models

# Create your models here.


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Camera(TrackableDateModel):
    location = models.TextField(max_length=2000, null=True, blank=False)
    latitude = models.FloatField(null=True, blank=False)
    longitude = models.FloatField(null=True, blank=False)
    type = models.TextField(max_length=100, null=True, blank=False)
    status = models.TextField(max_length=100, null=True, blank=False)


class Images(TrackableDateModel):
    camera = models.ForeignKey(Camera, related_name='images',
                               null=True, blank=True, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to='%Y/%m/%d/',  blank=True, null=True)


class Activity(TrackableDateModel):
    camera = models.ForeignKey(Camera, related_name='activities',
                               null=True, blank=True, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to='%Y/%m/%d/',  blank=True, null=True)
    note = models.TextField(max_length=2000, null=True, blank=False)
    time = models.DateTimeField(auto_now_add=True)
    cameraStatus = models.TextField(max_length=100, null=True, blank=False)
