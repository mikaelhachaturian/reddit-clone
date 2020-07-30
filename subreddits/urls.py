from django.urls import path
from . import views

app_name = 'subreddits'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_subr_form', views.subr_creation_form, name='subr_creation_form'),
    path('submit', views.post_creation_form,
         name='post_creation_form'),
    path('<str:subr_url_name>', views.subr_view, name='subr_view'),
    path('comments/<int:post_id>/', views.post_view, name='post_view'),
    path('comments/<int:post_id>/<int:comment_id>',
         views.post_view, name='post_view'),
    path('comments/<int:post_id>/<int:comment_id>/<str:vote_type>',
         views.post_view, name='post_view'),
    path('comments/<int:post_id>/<str:vote_type>',
         views.post_view, name='post_view'),

]
