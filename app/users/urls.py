from django.urls import path, include, re_path

from .apis import UserFacebookAccessTokenView, UserKakaoAccessTokenView
from .apis.user import UserListCreateView, UserRetrieveUpdateDestroyView

app_name = 'user'
urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list'),
    path('facebook-login/', UserFacebookAccessTokenView.as_view(), name='facebook-login'),
    path('kakao-login/', UserKakaoAccessTokenView.as_view(), name='kakao-login'),
    # path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    # path('<int:pk>/bookmark/', include('bookmarkcollection.urls'),

    # {{HOST}}/user/1/ 형식과 {{HOST}}/user/1/bookmark or collection
    # 이 두 가지를 urlpatterns에서 각각 사용하고 싶음.
    re_path(r'^(?P<pk>\d+)/$', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    re_path(r'^(?P<pk>\d+)/', include('bookmarkcollection.urls')),

    # 아래 regex는 안되는데 이유는 \w에 해당하는 문자까지 같이 인식되어 넘어가는 것 같음.
    # re_path(r'^(?P<pk>\d+)/\w+', include('bookmarkcollection.urls')),
]
