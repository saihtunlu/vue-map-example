from .models import Camera
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CameraSerializers, ImageSerializers, ActivitySerializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from django.shortcuts import get_object_or_404


class Cameras(generics.ListAPIView):
    """
    Cameras
    @methods - get
    """

    def get(self, request):
        if 'location' in request.GET:
            location = request.GET['location']
            status_ = request.GET['status']
            type = request.GET['type']
            if not location == '':
                cameras = Camera.objects.filter(
                    location__icontains=location, status__icontains=status_, type__icontains=type)
                cameras_serializer = CameraSerializers(
                    cameras, many=True)
                return Response(
                    cameras_serializer.data,
                    status=status.HTTP_200_OK)
        else:
            status_ = request.GET['status']
            type = request.GET['type']
            cameras = Camera.objects.filter(
                status__icontains=status_, type__icontains=type)
            cameras_serializer = CameraSerializers(
                cameras, many=True)
            return Response(
                cameras_serializer.data,
                status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class SingleCamera(generics.ListAPIView):
    """
    Single Camera Class
    @methods - post
    """

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):

        cameras = get_object_or_404(
            Camera, id=request.GET['id'])
        cameras_serializer = CameraSerializers(
            cameras, many=False)
        return Response(
            cameras_serializer.data,
            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        length = request.data['length']
        images = request.data
        camera = json.loads(request.data['camera'])
        new_camera = Camera()
        camera_serializer = CameraSerializers(new_camera, data=camera)
        if camera_serializer.is_valid():
            camera_serializer.save()
            for number in range(int(length)):
                array = {"image": None, "camera": None}
                array['image'] = images['image'+str(number)]
                array['camera'] = new_camera.id
                image_serializer = ImageSerializers(data=array)
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(camera_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(camera_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activities(generics.ListAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):

        activity = json.loads(request.data['activity'])
        if 'image' in request.data:
            image = request.data['image']
            activity['image'] = image
        camera = get_object_or_404(
            Camera, id=activity['camera'])
        camera.status = activity['cameraStatus']
        camera.save()
        activity_serializer = ActivitySerializers(data=activity)
        if activity_serializer.is_valid():
            activity_serializer.save()
            return Response(activity_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
