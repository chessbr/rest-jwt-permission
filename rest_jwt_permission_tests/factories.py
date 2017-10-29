# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import response, serializers, views, viewsets
from rest_framework.decorators import api_view, detail_route, list_route


class SimpleSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()


class BasicView(views.APIView):
    queryset = get_user_model().objects.none()
    def get(self, request, *args, **kwargs):
        return response.Response({'method': 'GET'})

    def post(self, request, *args, **kwargs):
        return response.Response({'method': 'POST', 'data': request.data})


@api_view(http_method_names=["post", "get"])
def function_endpoint(request):
    return response.Response({'method': request.method})


class SimpleViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects.none()
    serializer_class = SimpleSerializer

    @list_route(methods=["patch", "put"])
    def patch_put(self, request):
        return response.Response({'method': request.method})


class SimpleModelViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.none()
    serializer_class = SimpleSerializer

    @list_route(methods=["delete", "get"])
    def some_method(self, request):
        return response.Response({'method': request.method})

    @detail_route(methods=["get", "post", "patch", "put"])
    def some_detail_metod(self, request):
        return response.Response({'method': request.method})
