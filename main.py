# Написать две программы.Первая – вычисляет контрольную сумму файла. Вторая –
# вычисляет контрольную сумму всех файлов в директории, при этом обработка каждого
# отдельного файла осуществляется с помощью первой программы в отдельном процессе.

import json
import subprocess
import os
import hashlib
import time
from threading import Thread, Lock
from collections import defaultdict


result_for_hashing = defaultdict()
lock = Lock()


def hash_file(path, idx):
	h = hashlib.new('md5') 
	with open(path, 'rb') as f:
		while True: 
			block = f.read(1024) 
			if not block: 
				break 
			h.update(block) 
	
	lock.acquire()
	global result_for_hashing
	d = result_for_hashing.copy()
	d[idx] = h.hexdigest()
	time.sleep(0.1)
	result_for_hashing = d.copy()
	lock.release() 

def hash_string(string):
	h = hashlib.new('md5') 
	h.update(string.encode()) 
	return h.hexdigest() 


path = '.'

threads = []

files = os.listdir(path)
for idx, file in enumerate(files):
	fullpath = os.path.join(path, file)
	if os.path.isdir(fullpath):
		continue

	print(f'{fullpath} found')

	thread = Thread(
		target=hash_file,
		args=(fullpath, idx)
	)
	thread.start()
	threads.append(thread)


for thread in threads:
	thread.join()


result = []
for key in sorted(result_for_hashing.keys()):
	result.append(result_for_hashing[key])

print(hash_string(''.join(result)))
