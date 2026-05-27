from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importamos las vistas de la API que acabamos de crear
from beatemplate import api_views 

# Registramos las rutas automáticamente
router = DefaultRouter()
router.register('artists', api_views.ArtistViewSet)
router.register('releases', api_views.ReleaseViewSet)
router.register('songs', api_views.SongViewSet)
router.register('playlists', api_views.PlaylistViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas originales de tu web HTML
    path('', include('beatemplate.urls')),

    # --- RUTAS DE LA API REST ---
    path('api/', include(router.urls)),

    # --- RUTAS DE AUTENTICACIÓN JWT ---
    path('api/token/', TokenObtainPairView.as_view(), name='obtener_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refrescar_token'),

    # --- RUTAS DE DOCUMENTACIÓN (SWAGGER) ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]