#!/bin/bash
rm -rf ./dist/
CSTRING="Autocommit at $(date '+%Y-%m-%d %H:%M:%S')"
git add .
git commit -m "\"$CSTRING\""
git push origin
python -m build --no-isolation 
twine upload --skip-existing -r testpypi dist/*
twine upload --skip-existing dist/*
rm -rf ./dist/