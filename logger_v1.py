from datetime import datetime
import codecs
import time

class logger:
    def __init__(self, log_file='./log/main_log.txt'):
        self.log_file = log_file
        self.k = '\n'#改行

    def write(self, text):
        print(str(datetime.now()) + ' | ' + text + self.k, file=codecs.open(self.log_file, 'a', 'utf-8'))
        return

    def clear_log(self):
        with open(self.log_file, 'w') as f:
            f.write('')
        return
