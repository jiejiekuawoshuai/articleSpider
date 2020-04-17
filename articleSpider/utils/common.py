import hashlib


def get_md5(url):
    if isinstance(url, str):        # 我们可以对传入的类型检测，避免报错
        url = url.encode("utf-8")   # 不能直接对字符串加密，要先把字符串转换成bytes类型
    m = hashlib.md5()               # 实例化MD5对象
    m.update(url)                   # 加密
    return m.hexdigest()            # 获取结果返回


if __name__ == '__main__':
    print(get_md5("https://cnblogs.com"))