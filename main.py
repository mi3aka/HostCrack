import time
import requests
import urllib3
import pandas as pd
from threading import Thread
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
results = []


def check(ip, host):  # check("1.1.1.1", "mi3aka.eu.org") cdn host测试
    for http in ["http://", "https://"]:
        headers = {'Host': host, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'}
        max_retry = 3
        while True:
            try:
                r = requests.get(url=http + ip, headers=headers, timeout=3, verify=False)
            except Exception:
                max_retry -= 1
                if max_retry == 0:
                    break
                time.sleep(3)
                continue
            else:
                results.append({"ip": ip, "host": http + host, "status": r.status_code, "text": r.text[:63]})
                break


if __name__ == '__main__':
    domain = "mi3aka.eu.org"  # 主域名
    with open('ip.txt') as f:
        ips = f.read().split()
    with open('dictionary.txt') as f:  # dictionary.example.com
        words = f.read().split()
    with open('host.txt') as f:  # 已知域名
        hosts = f.read().split()

    thread_list = []

    for ip in tqdm(ips):
        for host in hosts:
            t = Thread(target=check, args=(ip, host))
            t.start()
            thread_list.append(t)
        for word in words:
            t = Thread(target=check, args=(ip, word + '.' + domain))
            t.start()
            thread_list.append(t)

    for t in thread_list:
        t.join()

    df = pd.DataFrame(results)
    df.to_csv(time.strftime("%m_%d_%H_%M_%S.csv", time.localtime()))
