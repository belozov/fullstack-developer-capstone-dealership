import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from djangoapp.restapis import analyze_review_sentiments

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Static HTML pages
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('about', TemplateView.as_view(template_name="About.html"), name='about_noslash'),
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact', TemplateView.as_view(template_name="Contact.html"), name='contact_noslash'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),

    # React Frontend SPA routes
    path('login', TemplateView.as_view(template_name="index.html"), name='login_page_noslash'),
    path('login/', TemplateView.as_view(template_name="index.html"), name='login_page'),
    path('register', TemplateView.as_view(template_name="index.html"), name='register_page_noslash'),
    path('register/', TemplateView.as_view(template_name="index.html"), name='register_page'),
    path('dealers', TemplateView.as_view(template_name="index.html"), name='dealers_page_noslash'),
    path('dealers/', TemplateView.as_view(template_name="index.html"), name='dealers_page'),
    path('dealer/<int:dealer_id>', TemplateView.as_view(template_name="index.html"), name='dealer_view_noslash'),
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html"), name='dealer_view'),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html"), name='postreview_noslash'),
    path('postreview/<int:dealer_id>/', TemplateView.as_view(template_name="index.html"), name='postreview'),

    # Direct sentiment analysis endpoint
    path('analyze/<path:input_txt>', lambda req, input_txt: JsonResponse(analyze_review_sentiments(input_txt))),

    # Manifest file
    re_path(
        r'^manifest\.json$',
        serve,
        {
            'document_root': os.path.join(settings.BASE_DIR, 'frontend/build'),
            'path': 'manifest.json'
        }
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
