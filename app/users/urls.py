from django.urls import path, include

from .apis import UserFacebookAccessTokenView, UserKakaoAccessTokenView
from .apis.user import UserListCreateView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('', UserListCreateView.as_view()),
    path('facebook-login/', UserFacebookAccessTokenView.as_view()),
    path('kakao-login/', UserKakaoAccessTokenView.as_view()),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('<int:pk>/bookmark/', include('bookmarkcollection.urls')),
]
