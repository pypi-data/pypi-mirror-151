import math
import numpy as np
import pandas as pd
pd.options.display.max_colwidth = 1800
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"
import plotly.io as pio
pio.templates.default = "plotly_dark"
import sqlite3
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
plt.style.use('dark_background')
from mpl_toolkits import mplot3d
from Trinnuty import *

__version__ = "0.0.1"