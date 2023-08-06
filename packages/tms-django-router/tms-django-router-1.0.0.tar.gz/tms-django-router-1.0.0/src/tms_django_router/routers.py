from rest_framework import routers, response
from rest_framework.reverse import reverse
from collections import OrderedDict
from django.urls import NoReverseMatch


class HybridAPIRootView(routers.APIRootView):

    api_view_urls = None

    def get(self, request, *args, **kwargs):
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format"),
                )
            except NoReverseMatch:
                continue

        for api_view_key in self.api_view_urls.keys():
            ret[api_view_key] = reverse(
                self.api_view_urls[api_view_key].name,
                args=args,
                kwargs=kwargs,
                request=request,
                format=kwargs.get("format"),
            )
        return response.Response(ret)


class HybridRouter(routers.DefaultRouter):
    APIRootView = HybridAPIRootView

    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}

    def add_api_view(self, name, url):
        self._api_view_urls[name] = url

    def remove_api_view(self, name):
        del self._api_view_urls[name]

    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key in self._api_view_urls.keys():
            urls.append(self._api_view_urls[api_view_key])
        return urls

    def get_api_root_view(self, api_urls=None):
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        api_view_urls = self._api_view_urls

        return HybridAPIRootView.as_view(
            api_root_dict=api_root_dict, api_view_urls=api_view_urls
        )
