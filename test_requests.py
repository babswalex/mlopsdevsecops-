import requests, time
url='http://127.0.0.1:8787/classify'
tests=[('malicious','This is a secure message'),('safe','Hello team, please review the attached report')]
for name,text in tests:
    for i in range(10):
        try:
            r=requests.post(url,json={'text':text},timeout=3)
            print(name.upper(), r.status_code, r.text)
            break
        except Exception as e:
            time.sleep(0.5)
            if i==9:
                print(name.upper(),'ERROR',e)
