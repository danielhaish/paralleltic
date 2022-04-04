
import inspect
from re import S
from threading import Thread
from queue import Queue
from .utils import queue_to_list
class ParallelizeThread:
    def __init__(self, threads_provider, log_provider=print, return_provider=all):
        self.thread_provider = threads_provider
        self.log_provider = log_provider
        self.return_provider = return_provider
        self.threads_resuatl_queue = Queue()

    def _get_ranges(self, number_of_threads, bigst_number):
        number_ranges = []
        jmps = bigst_number // number_of_threads
        remainder = bigst_number % number_of_threads
        last_number = 0
        current_number = 0
        while last_number + remainder < bigst_number:
            current_number += jmps
            number_ranges.append((last_number, current_number))
            last_number = current_number
        number_ranges[-1] = (number_ranges[-1][0], bigst_number)
        return number_ranges

    def  _separate_list_to_groups(self, lis, number_of_threads):
        if len(lis) < number_of_threads:
            number_of_threads = len(lis)
        list_ranges =self._get_ranges(number_of_threads, len(lis))
        lists = []
        for list_range in list_ranges:
            lists.append(lis[list_range[0]: list_range[1]])
        return lists
    def _wrap_function_in_thread(self, *args, **kwargs):
        return_value = args[0](*(args[1::]), **kwargs)
        self.threads_resuatl_queue.put(return_value)

    def _run_func_in_thread(self, func, thread_number, args, kwargs):
        self.thread_provider(target=self._wrap_function_in_thread, args=(func,) + (args, ), kwargs=kwargs).run()
        # self.log_provider("thread finished {}".format(thread_number))

    def _is_param_in_keywargs(self, func, unic_thread_param, kwargs):

        if  unic_thread_param in kwargs:
            return True
        if unic_thread_param in inspect.getargspec(func)[0]:
            return False
        raise ValueError("Function doest accept this param")
    
    def _get_param_index_in_function(self, func, param):
        return inspect.getargspec(func)[0].index(param)


    def _get_tuple_with_new_value(self, old_tuple, new_item, index):
        lis = list(old_tuple)[index] = new_item
        return tuple(lis)

    def paramtize_list(self, func, unic_thread_param, number_of_threads,  args, kwargs):
        
        if self._is_param_in_keywargs(func, unic_thread_param, kwargs):
                list_parts = self._separate_list_to_groups(kwargs[unic_thread_param] ,number_of_threads)  
        else:
                list_parts = self._separate_list_to_groups(args[self._get_param_index_in_function(func, unic_thread_param)],number_of_threads) 
        thread_count = 0
        for list_part in list_parts:
            thread_count += 1        
            if self._is_param_in_keywargs(func, unic_thread_param, kwargs):
                param_index = self._get_param_index_in_function(func, unic_thread_param)
                kwargs[unic_thread_param] = self._get_tuple_with_new_value(args, list_part, param_index)
            else:
                args = list_part
            self._run_func_in_thread(func, thread_count, args, kwargs)
        return self.return_provider(queue_to_list(self.threads_resuatl_queue, number_of_threads))


    def  paramtize(self, number_of_threads, unic_thread_param):
            def inner(func):
                def wrapper(*args, **kwargs):
                   return  self.paramtize_list(func, unic_thread_param, number_of_threads,  args, kwargs)
                return wrapper
            return inner


