

import os, sys
import sys

import inspect
import pprint
import traceback

import logging
import configparser

import datetime
import shutil
import json
import csv



def debug_info():
    line_no = inspect.currentframe().f_back.f_lineno
    fcn_name = inspect.currentframe().f_back.f_code.co_name
    print("Line: " + str(line_no))
    print("Fcn: " + str(fcn_name))




def debug_info_string():
    debug_info = ''
    line_no = inspect.currentframe().f_back.f_lineno
    fcn_name = inspect.currentframe().f_back.f_code.co_name
    debug_info += "Line: " + str(line_no)
    debug_info += "  Fcn: " + str(fcn_name)

    return debug_info




def get_current_fcn_name():
    return inspect.currentframe().f_back.f_code.co_name




def debug_var(var):
    pp = pprint.PrettyPrinter(indent=4)
    pp.depth = 6
    if(isinstance(var, object)):
        pp.pprint(vars(var))
    else:
        pp.pprint(var)


def debug_pprint(var):
    pp = pprint.PrettyPrinter(indent=4)
    pp.depth = 6
    pp.pprint(var)



def get_arg_parser():
    """Get parser object for script xy.py."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("--mode", dest="mode", default="clean", type=str, help="Mode", choices=["index", "retrieve", "clean"])

    parser.add_argument("--path", dest="path", default="", type=str, help="File Path")

    parser.add_argument("--colname", dest="colname", default="", type=str, help="Collection Name")



    return parser


