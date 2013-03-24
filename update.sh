#!/bin/bash
for i in `ls`
do
    if [[ -d $i ]]; then
        echo "Updating $i"
        pushd .
        
        cd $i
        git pull --all

        popd
        echo
    fi
done

