import re
def link_filter(url):
    pattern0 = re.compile(r'javascript')
    pattern1 = re.compile(r'chinadaily')
    if re.search(pattern0, url):
        print("this link is a javascript")
        return None
    elif url == 'None':
        print("this link is blank")
        return None
    elif url.startswith('http'):
        if re.search(pattern1, url):
            print("this is the link which matches our goal and needs no modification")
            print(url)
            return url
        else:
            print("this link doesn't match our goal,because it is linked to outside website")
            return None
    else:
        url = 'http://www.chinadaily.com.cn/' + url
        print("this link matach our goal, but we need to add some string to complete it")
        print(url)
        return url
link_filter('china/2017-05/13/content_29328561.htm')
link_filter('http://www.chinadaily.com.cn/china/')
link_filter('business/tech/')
link_filter('http://corp.sohu.com/')
link_filter('None')