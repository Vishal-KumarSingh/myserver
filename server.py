import socket
import subprocess
def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process.stdout.read()
def runningserver(config,log):
      global  logs
      logs=log
      msr = Server(config["port"])
      while True:
          msr.handle()
def stopserver():
    pass
def log_printer(message , tag):
    global logs
    logs.configure(state="normal")
    logs.insert("end", message , tag)
    logs.configure(state="disabled")

class Server:
    def __init__(self, port):
        self.myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myserver.bind(("127.0.0.1",int(port)))
        self.myserver.listen(100)
        self.response_header = bytes("HTTP/1.1 200 OK\r\n\n\n" , "utf-8")
        self.response_static_header = bytes("HTTP/1.1 200 OK\r\n Content-type: image/ico \n\n", "utf-8")
    def get_web_page(self , demand_page):

        file = open("htdocs/" + demand_page, "rb")
        data = file.read()
        file.close()
        return data
    def handle(self):
        self.client, addr = self.myserver.accept()
        try:
            request = self.client.recv(1028*100).decode().split("\r\n")
            demand_page=request[0].split(" ")[1]
            demand_page=self.remove_query_string(demand_page)
            if demand_page=="/":
                demand_page="/index.html"
                response = self.response_header+self.get_web_page("index.html")

            else:
                extension = demand_page.split(".")

                if extension[1] in ["html" , "js" , "css","htm"]:

                    response =self.response_header+ self.get_web_page(demand_page)
                elif extension[1] in ["php"]:

                    response = self.response_header + self.execute_php(demand_page)
                else:
                    response = self.response_static_header + self.get_web_page(demand_page)

            log_printer(demand_page+" file content delievered successfully\n", "desc")
            self.client.send(response)
        except Exception as e:
            #log_printer("File do not exist\n" , "stop")
            pass
        self.client.close()

    def remove_query_string(self, demand_page):
        pure_page = demand_page.split("?")
        return pure_page[0]

    def execute_php(self, param):

        data = popen("php htdocs/" +param)

        return bytes(data)


