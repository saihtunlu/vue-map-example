from rest_framework import serializers
from .models import Camera, Images, Activity


class ImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = "__all__"


class ActivitySerializers(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = "__all__"


class CameraSerializers(serializers.ModelSerializer):
    images = ImageSerializers(many=True, read_only=True)
    activities = ActivitySerializers(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = ['id',
                  'location',
                  'latitude',
                  'longitude',
                  'type',
                  'status',
                  'images',
                  'activities',
                  'created_at']
