import requests,time
for name,U in [("anteprima","https://3000-i4nq7yqdswtyddr7hb8sj.sandbox.easy-peasy.ai/api/trpc/latino.translate"),("produzione","https://latino-facile-app-2.easy-peasy.site/api/trpc/latino.translate")]:
    t0=time.time()
    d=requests.post(U,json={"json":{"text":"Nauta aquam bibit. Servus dominum non timet."}},timeout=100).json()["result"]["data"]["json"]
    print(name,d["source"],d["colorSource"],d["lines"],f"{time.time()-t0:.1f}s")
