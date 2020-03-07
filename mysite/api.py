from rest_framework import routers
from api import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'trials', myapp_views.TrialViewset)