from django.urls import path
from . import views
from store import views as user_views
from django.contrib.auth import views as auth_views
from .views import PostDetailView,PostCreateView,PostUpdateView,PostDeleteView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',views.store, name='store'),
    path('allproducts',views.products,name='products'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/',views.processOrder, name='process_order'),
    path('login/',auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
    path('profile/',user_views.profile,name='profile'),
    path('logout/',auth_views.LogoutView.as_view(template_name='store/logout.html'),name='logout'),
    path('register/',user_views.register,name='register'),
    path('product/<int:pk>',PostDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/',PostUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/',PostDeleteView.as_view(), name='product-delete'),
    path('product/new/',PostCreateView.as_view(), name='product-create'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)