import requests


headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"21\", \" Not;A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://pbservice.moc.oocl.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://pbservice.moc.oocl.com/party/cargotracking/ct_search_from_other_domain.jsf?ANONYMOUS_BEHAVIOR=BUILD_UP&domainName=PARTY_DOMAIN&ENTRY_TYPE=OOCL&ENTRY=MCC&ctSearchType=BC&ctShipmentNumber=OOLU2716050370",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "$Cookie": "cscaptachaCookie=e0d6c4b5-ea66-4128-9fdf-051a4d0b6f46; JSESSIONID=zjAbHfn0D16ykriUameQrgd1Zsv4GoXbhMBardURIQYolIQropTu\\u00211066063339; AcceptCookie=yes; AcceptCookie_Functional=yes; AcceptCookie_Statistical=yes; HMF_CI=3f9e6f110437c739958285349ae21303f14140264c1ae73887c6351c17a72730f008ed77a5a58a3c65ed3e1d7c6a474cff5f839dc862e3f18954d2f04f1c90e25d; CSH_DF=3Aj/f80GgJffaV5iXNdmgzb9rUedi5/+T2BnT8GuEtw1Sa+S2qryRhf/SEpjc6p4G9; CSH_UF=f8256d37159e3faf28ae61a6406601c3; _ga=GA1.4.1818281913.1688347802; _gid=GA1.4.312525864.1688347802; WT_FPC=id=2f2a5cbcacf52b046811688347801098:lv=1688348285507:ss=1688347801098; HMY_JC=f010023fc57c6a2132a6c309c133c332e66a495c75f28bfb7cb2e91a64717c280b,; HBB_HC=76f23b365e4a9b6124e8903d9f8931fae39e1255feb958329ca7c53b44f59c852dff8cbf31dc1e6cf4306ea64245fd3f4e; HOY_TR=FTUMQSRWXYADBHVZ,9387ABCDEF012456,xkvWwjublmcetina,0"
}
url = "https://pbservice.moc.oocl.com/party/cargotracking/ct_search_from_other_domain.jsf"
params = {
    "ANONYMOUS_TOKEN": "RRgdJZEyDnuiXuHcjMcvMCCOOCL",
    "ENTRY": "MCC",
    "ENTRY_TYPE": "OOCL",
    "PREFER_LANGUAGE": "en-US"
}
data = {
    "hiddenForm%3AsearchType": "BC",
    "hiddenForm%3ApCTTNa": "pCTTVag",
    "hiddenForm%3AbillOfLadingNumber": "",
    "hiddenForm%3AsupportUtfChars": "true",
    "hiddenForm%3AbookingNumber": "OOLU2716050370",
    "hiddenForm%3AcontainerNumber": "",
    "hiddenForm%3AreferenceNumber": "",
    "hiddenForm%3AreferenceType": "",
    "hiddenForm%3AisFromMobile": "false",
    "hiddenForm%3AembededContent": "false",
    "hiddenForm%3AselectedDomain": "PARTY_DOMAIN",
    "hiddenForm%3Atoken": "OCRzv6t9MIZ2ah/ZlOsCagYb4DiRx14nsl0yxtmJfyCVzeMzXhdb+Qh6Xj+YBntuFQY1JWme2kPbYHqidZY5PcRuixEnw8VhTFz8cha7qW0=",
    "hiddenForm%3Anc_token": "",
    "hiddenForm%3Acsessionid": "",
    "hiddenForm%3Asig": "",
    "USER_TOKEN": "USER_TOKEN=RRgdJZEyDnuiXuHcjMcvMCCOOCL&ENTRY=MCC&ENTRY_TYPE=OOCL&PREFER_LANGUAGE=en-US&OPERATOR_USER_ID=",
    "ENTRY": "MCC",
    "ENTRY_TYPE": "OOCL",
    "PREFER_LANGUAGE": "en-US",
    "OPERATOR_USER_ID": "",
    "hiddenForm_SUBMIT": "1",
    "hiddenForm%3A_link_hidden_": "hiddenForm:goToCargoTrackingBC",
    "jsf_tree_64": "1HdYiTH+P6YdNGZEgeEY1r3kF5UueVMTJS14BwpPDa6mSOp0b3jTtSxAnFTsI9yuDSKohURgmhS6RVkNT3OV7fw0ZtcTDjj4VQmpx4cLxwjdDR3KA1SnRTfdAR3VZGGc8AwPCMc/Ip2hu6CuudYafwGoJbd5cW0OM+uiXKJrwDg9RQcf7BMWLz6VPSdw6tZ1EPsUVNGpr33JpdvWx2Ernu5Fk583G8PQk6l0ZOO44ydnVSy+ocZjP74A8j4GoATNAwgaETwoxzAiX35gmLC6TnAkDA9Man7kpxlYC6GdtGDN7k/GrYC+BlLLqSFeIm34Im0dW20XiDlEVgMzWGklODx8sArrpd+a4w3H6mSSnyKDAYsBjAgvM6TZZZmT0CZ3/PCPFOxUQ7lLkuzwGLt2hvqVJs42YSFiJ3Z8C6Np1taS7f3oS2WFfIZb0eHq1VAP++TCUvG3LELzmYKrSjnHwX1HMyqHmJ1pKCX8qd89bZej2rAlcHPLYMDn6SH/qd6CLDJaLIdsq4+IN9pQ/QEL9IDdONbjYnrdOTgmuy7GuKK9dF9sduOuilQuEW8akWZ9yJH+WtOKDPCm5kUmv5k59NVbtMsbG1kcp8KKEj7Mq4XKe63+5Ky7+8dGXyks397L9n9d8yQUK/knTW3CZIlHBBs8svoy7prb",
    "jsf_state_64": "1HdYiTH+P6bOq1lF9hAgQSAUWImDP22oXTv8fgdLRr8fGl2a9OenkvlWa+4K8KKBUfiSyCb/P7tkWiifWJHs4Qmqt4YFw5Z7+ZkOGOi//2/mERJSh+Ls7ocdrZS4hq20KNAGTCOvOHW0Weq5YES7goLeVlfL6fE52GGlDIhPgB0wld+O1hnflPXqi1KqoFnu1Np0Z8SllmKhdTq+bZVNZbBbVKpGs/mRlhLBVfGcJG9DsM3Yk8Pw+vVpW8wII0PCtu+/bWi7EQflw6vdySyVsIPlBQrvTG7QIjFKOlocJgt8rBoT/ZsA6Pm/NRcB/XEt/dmyEecXO5c5DeahXsuo2jWWprUkIGilpU66yMUuEX7ZC9RgybmJgmLBr5q/9FbkVua33k+jojmjAxg1asqgYkKj3EDNMY6skn07mN04R5ux0LL9rmUOiT5+XHMbn3qeCy7Jat243CR/H52t0Ev7qV/3VqlrJgaZu4T4u9q6bGDqK/Q6WBv/Gr5mJtd9OGNF/SS8hfGbKiceEBYmbzQqmV7yDvFSIls0BAghTc0UYwF09Ur/RO9vpJv1QL8Xuew+PQLjzhZjmhklFPgh+U7zyF2MlGeuUIp0uo6D2FyUziL1cocMhOmPoL4ysfpSfmpH+wVoIL2ETHNevx46IiedEyk+ZPdibNAS95BhEAe9rE2MnbFQupHN+8rc753W07dxndXoNOpbbmy3BUgNYLs7nlotTdU4k9qRecvq+wGSrZSw7qZVoVED1SyLThOJkndT7Cxusd13L5pDsFii6/p2ZUDeFsIc0yoOauAnvAY21aWf/wuxZBh62U2JiYjfOv8luSKZtqVQcriWz/Bf+NkaPFm+kJf8tY+1JeZjzISd0hzvNVzbN4t3h2l8dW8t2eE9M2R950M1AtaDhQbPdsHCbm4D8xcLT+zxjlUjhNXzBWGZiwaHh/hG0ER1IHZSKu3mzdmCyMjCqHQLNI9hr2BbmOuz5mgebCX6H8w0keFoxZcwVm9Tjc67AVk2wTXKs49fjihvG4zVfEK2oonbUCO8jpHX1obcZHMe0S1UFIuMFBgG5iIk4xtJzG/IULZrjg/CTCeBXqu8KkVisJYEJL1W6vrnHW4eZ48c9EEDzh4U5hGMp0JTaCr/Mq9PeyPS0f7vd7RK2Bjcj4y1nCB8GIG8DAJbD78ZWo9v/ix+Y7uPMiVxqlacIBcL8mS/zcvFQ44LdOm5HaIoQ3qKeVdooMH+uYhRss5gGne4dkQYt1ZDYPuYm3H0gJMdPKWNB6olJmDqOYTR/wSZOFr0qeCLdYacEFXM8q/WGokgFCbkMuNvptWYUD8HRWaE+pGVkA8U6yT7u7ryvxlXZ5mmVWo+ilsShQXC7euVbtv2FNf/s+/mtaiH9KuuU7rQO0fY9jFZ5nXnG0u6wQvxuL6swb1lXjajnzMcQGU7Njq44NTp8xkwiEiHIc9K3KY2qDUAwiyIvzrfsjHj413zPc9134bFVXPqSppjXNGbxt3EZZZUHpH+Qu7LYmO9EGAYNLJFKSVwJnm3tkal+seQXzaPuVX5ILONLT+LtPL54XQpx2BTYpENlQSMmopuA7X7rPhkeOV1D75wFbXrf3i3UXqU9ZvWmPN5OXrmxrWkK6dCINcgDabzPE+63Qwyq13BUe4zUce+Rc4TCgi9cndMPL1DnwNNRRy65kop5epmOQ0pnjNaqwdEHtM1Yj4ytBFQem7yhll9WDz8FeXhjzkeFjUsLwFXcYjbJGm9g3gDUwVjqsyjYyc6Ay+eDlwV9Z+3wDmhhMpJHkFdR8GBM3L3G0l4Cl5CyNPV4FMIHTacuymjuBY9YxGQN2dYNGQ/R+0zn0xnRAPQhokQk8zf12HTxTgTrs9HeLAV+s9hyMOBtTdO2HSAcRhAq8vGaWLDMMZeJyRJ60DVoocW1/VNw/YJPy+ZDjMwNnf1mG/iejZlpVqO3JeB+Sv+0cKMzneF5IZKvx8r1Cd4sv/OB2GuSAtgplmfvPwrhi9kN5iEI+nQwpMRU8I+TJSYXmwCyKRmpFh7SNTRjz2bxAf6Yo3utjVQeifdB+Pybq9c6SrUVdMjKBlC43FGGxd0cJxQlcngOUsWRRkBX0hW924iQTGPrfJQz1epk6qyXnCMXBDCxD0TWknX5s4OotDZhqTw9FqudlCRej+pX0m9RniBeaSH56HETE/iOvp0DSkPC19FLxmBw0KjCjVR+Qk0feeTMcfKwbdTgVDK9xsI4RASkYtfFkkk2O1JrCGIlsjCHwf3hmlSG4+sAqexYcpWhUEZzU5jV38H+vTxcxINoUuJw2YakGzp+lOhF93DvLdDbFIttNNsBoeTUL6xabIQY2qWKSUa/4LopP1ox42Vu4wR6Y03nlMUXVcuzOwUzorK+5sQ0r8strJyGwukTvmjYfqOTRBWc5wK8fjmdKA3yoD3P2d7rXNbzRTiEB01Acp1ulvgHAG5E1YikXdd2ouE4E+VSd+dHV7FH3M0AJjMgFwe5D529q/wHkApploJivWKSny9/JPcJhVBt/y0BdU3VWbozR9rcp+ygA==",
    "jsf_viewid": "/cargotracking/ct_search_from_other_domain.jsp"
}
response = requests.post(url, headers=headers, params=params, data=data)

print(response.text)
print(response)