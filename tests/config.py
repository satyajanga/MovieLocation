
config = {}

fp = open("config.ini")
lines = fp.readlines()
fp.close()
for l in lines:
    line_split = l.strip().split(':')
    config[line_split[0].strip()] = line_split[1].strip()
