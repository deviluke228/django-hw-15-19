from django.urls import path
from bboard import views

urlpatterns = [
    path('', views.index, name='index'),

    path('rubric/<int:rubric_id>/', views.by_rubric, name='by_rubric'),

    path('bb/<int:id>/', views.bb_detail, name='bb_detail'),
    path('bb/<int:id>/delete/', views.bb_delete, name='bb_delete'),

    path('add/', views.BbCreateView.as_view(), name='add'),

    path('select/', views.select_columns, name='select_columns'),
    path('exclude/', views.exclude_values, name='exclude_values'),
    path('list/', views.bb_list, name='bb_list'),

    path('icecream/create/', views.icecream_create, name='icecream_create'),

    path('icecream/list/', views.available_icecream, name='icecream_list'),

    path('icecream/sets/', views.icecream_sets_short, name='icecream_sets_short'),
    path('icecream/tx/', views.icecream_transaction_demo, name='icecream_transaction_demo'),
    path('icecream/available/', views.available_icecream, name='available_icecream'),

    path('queryset/', views.queryset_demo, name='queryset_demo'),

    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    path('contact/', views.contact_view, name='contact'),
    path('tags/', views.tags_demo, name='tags_demo'),
    path('icecream/list/', views.icecream_list, name='icecream_list'),
]