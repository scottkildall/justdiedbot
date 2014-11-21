#!/bin/sh
# Execute from the command line, will add all git files
# by Scott Kildall www.kildall.com
# execute with commit message

echo "Pushing to Git"

# files we add are here, we assume a .gitignore, so right now we add everything, but can be modified 
git add .
git commit -m "$1"
git push -u origin master


