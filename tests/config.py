
config = {}

fp = open("config.ini")
lines = fp.readlines()
fp.close()
config.update(dict([map(lambda x: x.strip(), l.strip().split(':', 1)) for l in lines]))
