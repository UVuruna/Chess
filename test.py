import threading
import time





a=0
def counter():
    for _ in range(10**6):
        global a
        a +=1

start0 = time.time()
for _ in range(100):
    counter()
print(a)
a=0


start = time.time()
print(f'{(start-start0)*1000:,.0f} ms')

threads = []
for i in range(100):
    t = threading.Thread(target=counter)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
else:
    print('-------------')
    print(a)
    end = time.time()
    print(f'{(end-start)*1000:,.0f} ms')
