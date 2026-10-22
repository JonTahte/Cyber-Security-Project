from django.urls import path
from .views import homePageView, registerView, create_account, add, delete, loginView, profileView

urlpatterns = [
    path('', homePageView, name='index'),
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('create_account/', create_account),
    path('add/', add),
    path('delete/', delete),
    path('profile/<str:user_id>/', profileView, name='profile')
]
