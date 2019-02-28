#! /bin/bash
set -e

INPUT=$1

# Pi shrink in place will crash most of the time
# so it's copied to a temp file first
pishrink.sh -s /image/$INPUT /output/$INPUT.tmp
