from django.conf.urls import url, include
from BetProsApp.views import *

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django BetProsApp.
    url(r'^.*\.html', gentella_html, name='gentella'),

    # The home page
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^logout', LogoutView.as_view(), name='logout'),
    url(r'^register', RegistrationView.as_view(), name='registration'),
    url(r'^api/', include("BetProsApp.api.urls", namespace='urls-api')),
]