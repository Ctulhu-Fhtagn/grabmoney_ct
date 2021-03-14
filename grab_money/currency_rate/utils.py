# Thirdparty:
import requests


# get ONE currency in date or today, if date=none
def get_currency_rate(cur, date):
    url = "https://www.nbrb.by/api/exrates/rates/{}?ondate={}&parammode=2"
    res = requests.get(url.format(cur, date)).json()
    cur_rate = {"rate": res["Cur_OfficialRate"], "scale": res["Cur_Scale"]}
    return cur_rate


# get ALL currencies in date or today, if date=none
def get_all_currency_rate_date(date):
    url = "https://www.nbrb.by/api/exrates/rates?ondate={}&periodicity=0"
    res = requests.get(url.format(date)).json()
    cur_rate = []
    for i in res:
        cur_rate.append(
            {
                "abbreviation": i["Cur_Abbreviation"],
                "rate": i["Cur_OfficialRate"],
                "scale": i["Cur_Scale"],
            }
        )
    return cur_rate
