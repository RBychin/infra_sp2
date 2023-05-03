from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from reviews.models import Review, Category, Title, Genre
from .filters import CustomFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrReadOnly,
                          IsModeratorOrReadOnly)
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitlePostSerializer,
                          TitleSerializer,
                          )

User = get_user_model()


class ListCreateDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet
                              ):
    pass


class ReviewViewSet(ModelViewSet):
    """Представление на основе модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly
                          | IsAdminOrReadOnly
                          | IsModeratorOrReadOnly]

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        context['title'] = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return context

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(ModelViewSet):
    """Представление на основе модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly
                          | IsAdminOrReadOnly
                          | IsModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        )


class TitleViewSet(ModelViewSet):
    """Представление на основе модели Title."""

    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('-year')
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = CustomFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitlePostSerializer


class CategoryViewSet(ListCreateDeleteViewSet):
    """Представление на основе модели Category."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDeleteViewSet):
    """Представление на основе модели Genre."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
