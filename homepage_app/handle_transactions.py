# transaction
import json
import random

import requests
from django.conf import settings

def make_transaction(debitID, creditID, amount, remarks="SRE Transaction"):
    url = settings.ZETA_BASE_URL + "/transfers"
    data = json.dumps({
        "requestID": f"{random.randint(1, 1e5)}-{random.randint(1,1e4)}-{random.randint(1,1e6)}",
        "amount": {
            "currency": "INR",
            "amount": amount
        },
        "transferCode": "ATLAS_P2M_AUTH",
        "debitAccountID": debitID,
        "creditAccountID": creditID,
        "transferTime": 1574741608000,
        "remarks": remarks,
    })

    res = requests.post(url, data=data, headers=settings.HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print(res.json())
        return -1