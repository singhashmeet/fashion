import requests
import numpy as np
import cv2
import os
import shutil
from urlparse import urlparse
from parsers import *
from sklearn.cluster import KMeans


class Methods():
    def __init__(self):
        self.PATH = "/tmp/extractor/"
        self.REGISTEREDSITES = {
            'www.amazon.in': 'amazon'
        }
        self.PARSERS = {
            'amazon': amazon
        }
        if not os.path.exists(self.PATH):
            os.makedirs(self.PATH)

    def __hilo(self, a, b, c):
        if c < b:
            b, c = c, b
        if b < a:
            a, b = b, a
        if c < b:
            b, c = c, b
        return a + c

    def __compliment(self, r, g, b):
        k = self.__hilo(r, g, b)
        return tuple(k - u for u in (r, g, b))

    def __rgb2hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def GetImageUrl(self, page_url):
        page_content = requests.get(page_url)
        site = self.DetectSite(page_url)
        parser = self.PARSERS.get(site)
        if parser:
            image_url = parser(page_content.text)
            return image_url
        return ''

    def SaveFile(self, url):
        file_name = os.path.basename(url)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(self.PATH + file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return self.PATH + file_name
        return ''

    def CleanUp(self, path):
        os.remove(path)

    def DetectSite(self, page_url):
        url = urlparse(page_url)
        return self.REGISTEREDSITES.get(url.netloc)

    def Analyse(self, image_path):
        if not os.path.isfile(image_path):
            return '', []
        img = cv2.imread(image_path)
        height, width, dim = img.shape
        img = img[(height / 4):(3 * height / 4),
                  (width / 4):(3 * width / 4), :]
        height, width, dim = img.shape
        img_vec = np.reshape(img, [height * width, dim])

        kmeans = KMeans(n_clusters=5)
        kmeans.fit(img_vec)

        unique_l, counts_l = np.unique(kmeans.labels_, return_counts=True)

        sort_ix = np.argsort(counts_l)
        sort_ix = sort_ix[::-1]

        dominant = []
        colors = []
        for cluster_center in kmeans.cluster_centers_[sort_ix]:
            c = self.__compliment(
                cluster_center[2], cluster_center[1], cluster_center[0])
            dominant.append(self.__rgb2hex(
                cluster_center[2], cluster_center[1], cluster_center[0]))
            colors.append(self.__rgb2hex(c[0], c[1], c[2]))
        if dominant:
            dominant = dominant[0]
        else:
            dominant = "000000"
        return dominant, colors
