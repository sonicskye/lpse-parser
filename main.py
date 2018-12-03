'''
sonicskye @2018

main.py is the main script to call whatever necessary

'''

from pengumumanlelang import *
import vars as v


def main():
    #initialising and executing pengumumanlelang
    pl = pengumumanlelang()
    pl.iterate(v.lowNum, v.highNum)


if __name__ == '__main__':
    main()