from django.http import HttpResponse

from django.experimental.contrib.admin.views.decorators import superuser_required


@superuser_required
def superuser_secure_view(request):
    return HttpResponse("Superuser Secure View")


@superuser_required(redirect_field_name="myfield")
def superuser_secure_view_custom_field(request):
    return HttpResponse("Superuser Secure View With Custom Field")