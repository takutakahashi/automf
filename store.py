def persist(dct, cls):
    with open("/mnt/{}.txt".format(cls), 'a') as f:
        f.write(dct)
