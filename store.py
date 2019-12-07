import datetime
def persist(dct, cls):
    if dct is None:
        return
    print({"created_at": datetime.datetime.now().strftime("%Y-%m-%d"), "data": dct})
