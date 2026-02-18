"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),  # 將 api.urls 的路由配置包含進來，前綴為 'api/'
    
    path('api/auth/', include('dj_rest_auth.urls')),    # 登入、登出、密碼重設
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')), # 註冊
    
    # --- 以下為 API 文件路由 ---
    # 1. 生成 OpenAPI Schema (YAML 格式的定義檔)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. Swagger UI (互動式 API 文件，開發者最常用)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # 3. Redoc UI (另一種排版風格的文件，適合閱讀)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]