# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from methods import Methods

# Create your views here.


class GetLiveColor(APIView):

    def __init__(self):
        self.m = Methods()

    def post(self, request):
        resp = {'s': False}
        url = request.data.get('url')
        if url:
            site = self.m.DetectSite(url)
            if site:
                image_url = self.m.GetImageUrl(url)
                image_path = self.m.SaveFile(image_url)
                dominant_color, colors = self.m.Analyse(image_path)
                self.m.CleanUp(image_path)
                resp['s'] = True
                resp['d'] = dominant_color
                resp['c'] = colors
                resp['i'] = image_url
        return Response(resp, 200)
