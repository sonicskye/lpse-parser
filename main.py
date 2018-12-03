'''
sonicskye @2018

main.py is the main script to call whatever necessary

'''

from pengumumanlelang import *
from pemenang import *
import vars as v


def pengumumanlelangexecute():
    # initialising and executing pengumumanlelang
    pl = pengumumanlelang()
    pl.iterate(v.lowNum, v.highNum)


def pemenangexecute():
    pm = pemenang()
    pm.iterate(v.lowNum, v.highNum)


def main():
    #pengumumanlelangexecute()
    pemenangexecute()


if __name__ == '__main__':
    main()