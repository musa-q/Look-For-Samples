import time
import sys

class COLOR:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loadingBar(duration):
    interval = 1
    increments = duration // interval
    for i in range(increments):
        sys.stdout.write('\r')
        sys.stdout.write(f"[{'=' * (i + 1)}{' ' * (increments - i - 1)}] {COLOR.HEADER}{i * interval}/{duration}{COLOR.ENDC} seconds")
        sys.stdout.flush()
        time.sleep(interval)
    sys.stdout.write('\n')