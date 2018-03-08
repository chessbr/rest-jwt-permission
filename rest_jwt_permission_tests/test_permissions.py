# -*- coding: utf-8 -*-
import jwt
from django.conf.urls import include, url
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.utils.encoding import force_text
from rest_framework import response, routers, serializers, status, views, viewsets
from rest_framework.decorators import api_view, detail_route, list_route, permission_classes
from rest_framework.test import APIClient

from rest_jwt_permission.permissions import JWTAPIPermission
from rest_jwt_permission.providers import get_permission_providers


class SimpleSerializer(serializers.Serializer):
    pk = serializers.ReadOnlyField()


class BasicView(views.APIView):
    permission_classes = [JWTAPIPermission]

    def get(self, request):
        return response.Response({"method": "GET"})

    def post(self, request):
        return response.Response({"method": "POST", "data": request.data})


@api_view(http_method_names=["post", "get"])
@permission_classes([JWTAPIPermission])
def function_endpoint(request):
    return response.Response({"method": request.method})


class SimpleViewSetPermission(viewsets.ViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [JWTAPIPermission]

    @list_route(methods=["patch", "put"], permission_classes=[JWTAPIPermission])
    def patch_put(self, request):
        return response.Response({"method": request.method})


class ModelViewSetPermission(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = SimpleSerializer
    permission_classes = [JWTAPIPermission]

    def create(self, request):
        return response.Response({"method": request.method})

    def destroy(self, request, pk=None):
        return response.Response({"method": request.method})

    @list_route(methods=["delete", "get"], permission_classes=[JWTAPIPermission])
    def some_method(self, request):
        return response.Response({"method": request.method})

    @detail_route(methods=["get", "post", "patch", "put"], permission_classes=[JWTAPIPermission])
    def some_detail_metod(self, request, pk=None):
        return response.Response({"method": request.method})


router = routers.DefaultRouter()
router.register(r"simple_viewset", SimpleViewSetPermission)
router.register(r"model_viewset", ModelViewSetPermission)

urlpatterns = [
    url(r"^basic/$", BasicView.as_view()),
    url(r"^function/$", function_endpoint),
    url(r"^other/", include(router.urls)),
]

def setup_function(fn):
    get_permission_providers.cache_clear()


def test_jwt_api_endpoint_permission(admin_user):
    with override_settings(
        ROOT_URLCONF="rest_jwt_permission_tests.test_permissions",
        REST_JWT_PERMISSION={
            "SCOPE_PROVIDERS": [
                "rest_jwt_permission.providers.APIEndpointScopeProvider",
                "rest_jwt_permission.providers.AdminScopeProvider"
            ]
        }
    ):
        payload = {
            "scopes": [
                "function_endpoint:get",
                "basicview:get",
                "simpleviewsetpermission:patch_put:put",
                "modelviewsetpermission:retrieve:get",
                "modelviewsetpermission:create:post",
                "modelviewsetpermission:some_method:delete",
                "modelviewsetpermission:destroy:delete",
                "modelviewsetpermission:some_detail_metod:patch",
            ]
        }
        client = APIClient()

        assert client.get("/function/").status_code == status.HTTP_403_FORBIDDEN

        key = "super-secret"  # defined at conftest.py
        authorization = "JWT " + force_text(jwt.encode(payload, key, algorithm="HS256"))
        client.credentials(HTTP_AUTHORIZATION=authorization)

        assert client.get("/function/").status_code == status.HTTP_200_OK
        assert client.post("/function/").status_code == status.HTTP_403_FORBIDDEN

        assert client.get("/basic/").status_code == status.HTTP_200_OK
        assert client.post("/basic/").status_code == status.HTTP_403_FORBIDDEN

        assert client.put("/other/simple_viewset/patch_put/").status_code == status.HTTP_200_OK
        assert client.patch("/other/simple_viewset/patch_put/").status_code == status.HTTP_403_FORBIDDEN

        assert client.get("/other/model_viewset/{}/".format(admin_user.id)).status_code == status.HTTP_200_OK
        assert client.post("/other/model_viewset/", data={"data": 1}).status_code == status.HTTP_200_OK
        assert client.delete("/other/model_viewset/some_method/", data={"data": 2}).status_code == status.HTTP_200_OK
        assert client.delete("/other/model_viewset/{}/".format(admin_user.id), data={"data": 3}).status_code == status.HTTP_200_OK
        assert client.patch("/other/model_viewset/{}/some_detail_metod/".format(admin_user.id), data={"data": 4}).status_code == status.HTTP_200_OK
