import os
import sys
import subprocess
import signal
import time


def get_exceptions_args():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno


def cleanup():
    chrome_windows = subprocess.getoutput(['pgrep chrome'])
    if chrome_windows:
        chrome_windows_list = chrome_windows.split('\n')
        for pid in chrome_windows_list:
            os.kill(int(pid), signal.SIGKILL)
        time.sleep(1)

        sentenced = set(chrome_windows_list)
        alive = set(subprocess.getoutput(['pgrep chrome']).split('\n'))

        print(f'killed [{sorted(list(sentenced - alive))}]')
        print(f'survived [{sorted(list(alive))}]')