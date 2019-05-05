#!/bin/sh

INTERFACE=xds110
TARGET=bbb
SOURCE_DIR=`pwd`
TRANSPORT=jtag

openocd -s $SOURCE_DIR -f $INTERFACE.cfg -c "transport select $TRANSPORT" -f $TARGET.cfg
