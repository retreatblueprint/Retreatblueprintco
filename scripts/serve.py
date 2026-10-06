import io, os, re, sys, functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class H(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()
    def send_head(self):
        rng = self.headers.get('Range')
        path = self.translate_path(self.path)
        m = re.match(r'bytes=(\d*)-(\d*)$', rng or '')
        if not m or os.path.isdir(path) or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        if a == '':
            s, e = max(size - int(b), 0), size - 1
        else:
            s, e = int(a), (int(b) if b else size - 1)
        e = min(e, size - 1)
        with open(path, 'rb') as f:
            f.seek(s); data = f.read(e - s + 1)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {s}-{e}/{size}')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        return io.BytesIO(data)

port, directory = int(sys.argv[1]), sys.argv[2]
ThreadingHTTPServer(('127.0.0.1', port), functools.partial(H, directory=directory)).serve_forever()
