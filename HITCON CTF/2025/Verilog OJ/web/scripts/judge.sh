#!/bin/sh

set -e

cd "$1"

iverilog module.v testbench.v -o judge
vvp judge
