from rest_framework import views
from rest_framework.schemas import openapi
from rest_framework.response import Response
from django.conf import settings


class VersionSchema(openapi.AutoSchema):
    pass


class VersionView(views.APIView):
    schema = VersionSchema()

    def get(self, request, format=None):
        return Response(settings.VERSION)
