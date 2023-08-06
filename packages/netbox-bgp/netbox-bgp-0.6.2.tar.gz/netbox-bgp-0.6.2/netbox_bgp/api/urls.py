from rest_framework import routers

from .views import (
    ASNViewSet, BGPSessionViewSet, RoutingPolicyViewSet, BGPPeerGroupViewSet,
    CommunityViewSet
)

router = routers.DefaultRouter()
router.register('asn', ASNViewSet)
router.register('session', BGPSessionViewSet, 'session')
router.register('bgpsession', BGPSessionViewSet, 'bgpsession')
router.register('routing-policy', RoutingPolicyViewSet)
router.register('peer-group', BGPPeerGroupViewSet, 'peergroup')
router.register('bgppeergroup', BGPPeerGroupViewSet, 'bgppeergroup')
router.register('community', CommunityViewSet)


urlpatterns = router.urls
