from tornado.httpclient import HTTPClient, AsyncHTTPClient
from tornado.concurrent import Future
from tornado import gen

def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

def asynchronous_fetch(url, callback):
    http_client = AsyncHTTPClient()
    def handle_response(response):
        callback(response.body)
    http_client.fetch(url, callback=handle_response)

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    raise gen.Return(response.body)

def output(ret):
    print ret

def main():
    import tornado.ioloop
    URL = "http://www.google.com/"
    #tornado.ioloop.IOLoop.current().run_sync(lambda: output(fetch_coroutine(URL)))
    #tornado.ioloop.IOLoop.current().run_sync(lambda: synchronous_fetch(URL))
    tornado.ioloop.IOLoop.current().run_sync(lambda: asynchronous_fetch(URL, output))
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
