from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Auth token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Advocate REST URLS
    path("", views.endpoints, name="public-api"),
    path("advocates/", views.advocate_list, name="fetch-advocates"),
    path("advocates/<str:username>/", views.AdvocateDetail.as_view(), name="fetch-advocate-details"),
    #path("advocates/<str:username>/", views.advocate_details, name="fetch-advocate-details")

    # Company REST URLS
    path("companies/", views.company_list, name="fetch-company"),
    path("companies/<str:name>/", views.company_details, name="fetch-company-details"),
]
