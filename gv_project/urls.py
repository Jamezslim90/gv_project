from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include
from marketplace import views as MarketplaceViews


urlpatterns = [
    
    # path('jet/', include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    
    path('admin/', admin.site.urls),
    
    # User management
    
    path('accounts/', include('accounts.urls')),
   
    
    # Local apps
    path('', include('pages.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    
    #path('doctors/', include('doctors.urls'))
    path('blog/', include('blog.urls')),
    path('marketplace/', include('marketplace.urls')),
    
    path('laboratories/', include('laboratories.urls')),
    
     # CART
    path('cart/', MarketplaceViews.cart, name='cart'),
    # SEARCH
    path('search/', MarketplaceViews.search, name='search'),

    # CHECKOUT
    path('checkout/', MarketplaceViews.checkout, name='checkout'),

    # ORDERS
    path('orders/', include('orders.urls')),
    
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header =  "Getvet Admin"
admin.site.site_title =   "Getvet Admin Portal"
admin.site.index_title = "Welcome to Getvet Portal"

