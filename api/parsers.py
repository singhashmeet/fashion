from bs4 import BeautifulSoup


def amazon(payload):
    soup = BeautifulSoup(payload, 'html.parser')
    check = soup.find('div', attrs={'id': 'altImages'})
    if check:
        img_div = soup.find('div', attrs={'id': 'imgTagWrapperId'})
        img_tag = img_div.find('img')
        return img_tag.get('src')
    return ''
