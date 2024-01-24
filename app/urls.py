from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .form import LoginForm, MyPasswordChangeForm
urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    path('cart/', views.showCart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    
    
    path('buy/', views.buy_now, name='buy-now'),
    
    
    path('profile/', views.Profile.as_view(), name='profile'),
    
    
    
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/ <slug:data>', views.mobile, name='mobiledata'),
    path('topwear/', views.topwear , name='topwear'),
    path('topwear/ <slug:data>', views.topwear, name='topweardata'),
    
    
    
    # path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form= LoginForm) , name='login'),
    
    
    # logout view (built in)
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('logout/', views.logout_view, name='logout'),
    
    
    
    # path('changepassword/', views.change_password, name='changepassword'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm), name='passwordchange'),
    
    
    
    
    path('registration/', views.CustomeRegistrationView, name='customerregistration'),
    # path('registration/', views.customerregistration, name='customerregistration'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
