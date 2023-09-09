from locust import task, run_single_user
from locust import FastHttpUser


class urbannestlogin(FastHttpUser):
    host = "http://127.0.0.1:8000"
    default_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "mk-RS,mk;q=0.9,en-RS;q=0.8,en-US;q=0.7,en;q=0.6,fil;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "127.0.0.1:8000",
        "Referer": "http://127.0.0.1:8000/accounts/login/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    @task
    def t(self):
        with self.client.request(
                "POST",
                "/accounts/login/",
                headers={
                    "Content-Length": "114",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cookie": "csrftoken=f5mHFza87u4bpOGIzJnNHEe3JyMRtDaR",
                    "Origin": "http://127.0.0.1:8000",
                },
                data="csrfmiddlewaretoken=rgHqWTWNJrxqyr9UsxXEBiZ0hi9fUv9awbTXriWLGLrrN5FsR6ah8M3TQGLWdY9R&username=admin&password=admin",
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/",
                headers={
                    "Cookie": "csrftoken=a1jclTxVpc04DH5XknlSMRBLtNSYpDf5; sessionid=qxo7e6th3btrdu2b1x3wx0pr4ik9m0uj"
                },
                catch_response=True,
        ) as resp:
            pass


if __name__ == "__main__":
    run_single_user(urbannestlogin)
