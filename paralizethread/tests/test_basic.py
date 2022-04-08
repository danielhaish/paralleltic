from paralizethread.paralize import ParallelizeThread
from threading import Thread
load_balancer = ParallelizeThread(threads_provider=Thread, return_provider=sum)
@load_balancer.paramtize(number_of_threads=10, unic_thread_param="list_of_numbers")
def sum_billons_of_numbers(list_of_numbers):
    return sum(list_of_numbers)

load_balancer = ParallelizeThread(threads_provider=Thread, return_provider=all)
@load_balancer.paramtize(number_of_threads=2, unic_thread_param="list_of_numbers")
def is_all_even(list_of_numbers):
    lis = map(lambda number: number % 2 == 0, list_of_numbers)
    return all(lis)


def test_sum():
    assert sum_billons_of_numbers(range(1000)) == sum(range(1000))

def test_bool_with_false():
    assert is_all_even([2,4,6,8,1 ] ) == False
    