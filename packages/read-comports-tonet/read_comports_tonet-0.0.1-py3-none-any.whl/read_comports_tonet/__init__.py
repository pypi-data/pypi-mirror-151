# from read_comports_tonet.app import ReadFromComPorts
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from read_comports_tonet.app import ReadFromComPorts