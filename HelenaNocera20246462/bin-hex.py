import sys

filename = sys.argv[1]
fp = open(filename, "r")

print("v3.0 hex words plain")
for line in fp:
        print(hex(int(line.strip(),2)))

fp.close()

