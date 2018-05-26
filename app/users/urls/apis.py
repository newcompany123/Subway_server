from django.urls import path

from ..apis import UserFacebookAccessTokenView
from ..apis.user import UserListCreateView, UserRetrieveUpdateDestroyView


urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('facebook-login/', UserFacebookAccessTokenView.as_view()),
]
