from paralizethread.paralize import ParallelizeThread
from threading import Thread
from paralizethread.thread_loger import stdout_to_logs, ThreadsLogs
logger = ThreadsLogs(stdout_to_logs)
load_balancer = ParallelizeThread(threads_provider=Thread, return_provider=list, log_provider=logger)

@load_balancer.paramtize(number_of_threads=2, unic_thread_param="list_of_numbers")
def print_seqare_root_of_list(list_of_numbers):
    for i in list_of_numbers:
        print(i ** 2)

def test_simple_log():
    print_seqare_root_of_list([2,3])
    assert logger.get_logs_sorted() == ['4', '9']