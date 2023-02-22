from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # User management
    path('accounts/', include('accounts.urls')),
    # Local apps
    path('', include('pages.urls')),
    #path('doctors/', include('doctors.urls'))
    #path('blog/', include('blog.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

