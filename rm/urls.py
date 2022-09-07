from django.urls import path
# from . import views
from .views import HomeList, HomeDetail, HomeCreate, HomeUpdate, HomeDelete, HomeLogin, HomeRegister  # used to import class function from views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', HomeLogin.as_view(), name='homelogin'), #to get class from the views
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'), #to get class from the views
    path('', HomeList.as_view(), name='homelist'), #to get class from the views
    path('detail/<int:pk>/', HomeDetail.as_view(), name='homedetail'), #detail function take primary key as slug as default
    path('create/', HomeCreate.as_view(), name='homecreate'),
    path('update/<int:pk>/', HomeUpdate.as_view(), name='homeupdate'), #detail function take primary key as slug as default
    path('delete/<int:pk>/', HomeDelete.as_view(), name='homedelete'),
    path('register/', HomeRegister.as_view(), name='homeregister'),
]
 