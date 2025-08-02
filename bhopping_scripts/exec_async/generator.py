# Duration = 9 minutes * COUNT
COUNT = 10
for i in range (0, COUNT):
	with open(f"bhloop{i}.cfg", "w") as f:
		for _ in range (0,i):
			f.write("sleep 540000\n")
		for _ in range (0, 45000):
			f.write("sleep 12\n")
			f.write("bh\n")

with open("setup.cfg", "w") as f:
	f.write("echo Setting up timer, please wait...\n")
	f.write("log_flags InputService +donotecho\n")
	for i in range (0, COUNT):
		f.write(f"exec_async exec_async/bhloop{i};\n")
		f.write("sleep 1\n")
	f.write("log_flags InputService -donotecho\n")
	f.write("echo Setup done!\n")