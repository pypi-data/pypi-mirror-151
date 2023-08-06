
""" wfGenes: Automatic workflow generator."""


__author__ = 'Mehdi Roozmeh'
__email__ = 'mehdi.roozmeh@kit.edu'
__copyright__ = 'Copyright 2020, Karlsruhe Institute of Technology'




import os
import os.path
from copy import deepcopy
from collections import OrderedDict
import shutil
import argparse
import json
import xmlschema
import yaml
import jsonschema
from jsonschema import validate
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

class FireworksPlugin():
    """ Perform array initialization for fireworks """
    def __init__(self, blueargs):
        self.args_workflowconfig = blueargs['workflowconfig']
        self.args_inputpath = blueargs['inputpath']
        self.args_wms = blueargs['wms']
        self.previous_stamp = os.stat(self.args_workflowconfig).st_mtime
        self.firework_generation(blueargs)
        # List declaration

    def firework_generation(self, blueargs):
        print('pass')


        
        
    
        