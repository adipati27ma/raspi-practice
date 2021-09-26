import threading
import concurrent.futures
import time

start = time.perf_counter()

def do_something(seconds):
  print(f'Sleeping {seconds} second(s)..')
  time.sleep(seconds)
  print(f'Done sleeping...{seconds}')
  # return f'Done sleeping...{seconds}'

# Start using concurrent futures---
#* with 10 or 5 process
# with concurrent.futures.ThreadPoolExecutor() as executor :
#   secs = [5, 4, 3, 2, 1]
#   results = [executor.submit(do_something, sec) for sec in secs]

#   for f in concurrent.futures.as_completed(results):
#     print(f.result())
  
  #* with single/few process
  # f1 = executor.submit(do_something, 1)
  # f2 = executor.submit(do_something, 1)
  # print(f1.result())
  # print(f2.result())

# End of using concurrent futures---

# Start using old threading---
# threads = []
# secs = [5, 4, 3, 2, 1]
# for sec in secs:
#   t = threading.Thread(target=do_something, args=[sec])
#   t.start()
#   threads.append(t)

# for thread in threads :
#   thread.join()

t1 = threading.Thread(target=do_something, args=[1])
t2 = threading.Thread(target=do_something, args=[1])

t1.start()
t2.start()

# t1.join()
# t2.join()

# End of using old threading---

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')