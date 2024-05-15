from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('blogs2/', views.BlogDetailView.as_view(), name='blog_list2'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/<slug:slug>/',
         views.BlogPostDetailView.as_view(), name='blog_detail'),
    path('blog/create/', views.BlogPostCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>/',
         views.BlogPostUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>/',
         views.BlogPostDeleteView.as_view(), name='blog_delete'),
]
