from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnswerCreateDeleteView, LikedPostsView, PostViewSet, TagViewSet


router = DefaultRouter()
router.register('post', PostViewSet, 'get')
router.register('answer', AnswerCreateDeleteView, 'answer')
router.register('tags', TagViewSet, 'tags' )
urlpatterns = [
    path('liked/', LikedPostsView.as_view(), name='liked'),
]
urlpatterns += router.urls