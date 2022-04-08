class ThreadsLogs:
    resualts_list = []
    def __init__(self, print_overide) -> None:
        self.print_overide = print_overide
        
    def add_log(self, new_log, thread_number):
        self.resualts_list.append((str(new_log), thread_number))
    
    def get_logs_sorted(self):
        return [log[0] for log in sorted(self.resualts_list)]

    def print(self, string, thread_number):
        self.print_overide(string, self, thread_number)

def stdout_to_logs(string, logerobject, thread_number):
    logerobject.add_log(string, thread_number)
