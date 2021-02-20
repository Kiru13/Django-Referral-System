from rest_framework.routers import DefaultRouter
from .views import SignupViewSet, UsersViewSet, ShareReferralCodeViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('signup', SignupViewSet, basename='signup')
router.register('share', ShareReferralCodeViewSet, basename='share_referral')

urlpatterns = router.urls
