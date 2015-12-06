#!/bin/bash

TESTS=`dirname $0`
VENV=$TESTS/../$1
shift
. $VENV/bin/activate && $@
