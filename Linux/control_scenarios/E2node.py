from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 打印收到的请求路径
        print(f"Received POST request on {self.path}")
        
        # 获取请求的长度并读取内容
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 打印请求体内容
        print(f"Post data: {post_data.decode('utf-8')}")
        
        # 发送HTTP响应
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # 响应内容
        response = '{"status": "success"}'
        self.wfile.write(response.encode('utf-8'))

# 服务器运行的端口
PORT = 8000

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
