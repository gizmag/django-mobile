from django_mobile import flavour_storage
from django_mobile import set_flavour, _init_flavour
from django_mobile.ua_detector import UADetector
from django_mobile.conf import settings


class SetFlavourMiddleware(object):
    def process_request(self, request):
        _init_flavour(request)

        if settings.FLAVOURS_GET_PARAMETER in request.GET:
            flavour = request.GET[settings.FLAVOURS_GET_PARAMETER]
            if flavour in settings.FLAVOURS:
                set_flavour(flavour, request, permanent=True)

    def process_response(self, request, response):
        flavour_storage.save(request, response)
        return response


class MobileDetectionMiddleware(object):
    """
    This middleware detects and sets a flavour in case there is no previous
    flavour saved. In that case the saved flavour is set.
    """

    def process_request(self, request):
        saved_flavour = flavour_storage.get(request)

        if saved_flavour is None:
            if UADetector(request).is_user_agent_mobile():
                    set_flavour(settings.DEFAULT_MOBILE_FLAVOUR, request)
            else:
                set_flavour(settings.FLAVOURS[0], request)
        else:
            set_flavour(saved_flavour, request)
