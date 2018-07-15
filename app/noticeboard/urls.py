from django.urls import path

from noticeboard.apis import NoticeboardListCreateView

urlpatterns = [
    path('', NoticeboardListCreateView.as_view()),
]
