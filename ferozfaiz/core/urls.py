from django.urls import path
from django.conf.urls import handler403, handler404
from . import views

handler403 = views.Handler403View.as_view()
handler404 = views.Handler404View.as_view()
handler401 = views.Handler401View.as_view()

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('403/', views.Handler403View.as_view(), name='403'),
    path('404/', views.Handler404View.as_view(), name='404'),
    path('401/', views.handler401, name='401'),
]
