from django.urls import path

from myPay import views

app_name = 'myPay'

urlpatterns = [
    path('get_test', views.GetTestView.as_view()),
    path('get_post_test', views.GetPostTestView.as_view()),
    path('get_post_test_order', views.GetPostTestOrderView.as_view()),
    path('get_post_order', views.GetPostOrderView.as_view()),
    path('get_user_post_order', views.GetUserPostOrderView.as_view()),
    path('callback',views.CallBackView.as_view()),
]