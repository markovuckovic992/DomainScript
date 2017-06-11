import pyximport; pyximport.install()
import scriptmodule
import time
import sys

if __name__ == '__main__':
    start_time = time.time()
    scriptmodule.init(sys.argv[4])
    scriptmodule.main_filter(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
    )
    duration = int(time.time() - start_time)
    scriptmodule.close(sys.argv[4], duration)