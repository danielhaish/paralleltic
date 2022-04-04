from queue import Queue
def queue_to_list(res_queue: Queue, wait_for_number_of_itmes: int):
    """
     Getting number ofr itmes from queue and return then as list
    """
    lis = [res_queue.get() for q in range(wait_for_number_of_itmes)]
    for i in lis:
        res_queue.put(i)
    return lis

def wait_all_threads_to_end(thread_queue, number_of_threads):
    pass
    