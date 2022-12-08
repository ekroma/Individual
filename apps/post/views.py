from urllib.request import Request
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filter
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser, 
    AllowAny,
    )
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
    )

from .models import (
    Post,
    Tag,
    Answer,
    Rating,
    Like
)
from .serializers import (
    LikeSerializer,
    PostListSerializer,
    PostSerializer,
    PostCreateSerializer,
    AnswerSerializer,
    RatingSerializer,
    TagSerializer,
    LikedPostSerializer,
)
from .permissions import IsOwner


class PostViewSet(ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post/post.html'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter,
        rest_filter.DjangoFilterBackend,
        filters.OrderingFilter
        ]
    search_fields = ['title', 'user__username']
    ordering_fields = ['created_at']
    
    def list(self, request):
        self.object = self.get_queryset()
        return Response({'posts': self.object.order_by('-created_at') })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'post': serializer.data}, template_name='post/retrieve.html')
            
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action == 'answer' and self.request.method == 'DELETE':
            self.permission_classes = [IsOwner]
        if self.action in ['create', 'answer', 'set_rating','like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [ IsOwner]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def answer(self, request:Request, pk=None):
        post = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data,
                status=status.HTTP_201_CREATED
            )

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set-rating')
    def set_rating(self, request:Request, pk=None):
        data = request.data.copy()
        data['post'] = pk #TODO: 
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user = request.user,
            post = pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Rating object does not exist. Use POST method'})

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request:Request, pk=None):
        post = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'post': post
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked')

class AnswerCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
    ):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='post/create_answer.html'
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwner]

    



class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

        
class LikedPostsView(ListAPIView):
    serializer_class = LikedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

    

"""
actions

create() - POST
retrieve() - GET /post/1/
list() - GET /post/
destroy() - DELETE /post/1/
partial_update() - PATCH /post/1/
update() - PUT /post/1/

"""
#TODO: кастомизация админ-панели