# -*- coding:utf-8 -*-
import os
import sys
import queue

import time
import re
import threading
import records
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from myconfig import readConfig







if __name__ == "__main__":
    x = np.linspace(-1, 1, 50)
    y = 2 * x + 1
    plt.figure()
    plt.plot(x, y)
    plt.show()