from django.conf import settings
from django.http import Http404, JsonResponse

SUPPORTED_PATHS = [
    "/app/*",
    "/practice/*",
    "/simulate/*",
    "/progress/*",
    "/search/*",
    "/history/*",
    "/account/*",
    "/privacy/*",
]


def apple_app_site_association(_request):
    if not settings.MOBILE_LINKS_ENABLED:
        raise Http404
    return JsonResponse(
        {
            "applinks": {
                "details": [
                    {
                        "appIDs": [f"{settings.APPLE_TEAM_ID}.{settings.IOS_BUNDLE_IDENTIFIER}"],
                        "components": [{"/": path} for path in SUPPORTED_PATHS],
                    }
                ]
            }
        }
    )


def android_asset_links(_request):
    if not settings.MOBILE_LINKS_ENABLED:
        raise Http404
    return JsonResponse(
        [
            {
                "relation": ["delegate_permission/common.handle_all_urls"],
                "target": {
                    "namespace": "android_app",
                    "package_name": settings.ANDROID_PACKAGE_NAME,
                    "sha256_cert_fingerprints": settings.ANDROID_SHA256_CERT_FINGERPRINTS,
                },
            }
        ],
        safe=False,
    )
