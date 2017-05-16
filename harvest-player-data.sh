#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

cleanup() {
    # example cleanup function
    # rm -f /tmp/tempfile
    echo -en "Exiting"
    return $?
}
 
control_c() {
    # run if user hits control-c
    cleanup
    exit $?
}
 
RAW_JSON="data/leaderboard-pages.jsonl"

# trap keyboard interrupt (control-c)
# will call control_c function
trap control_c SIGINT
main() {
    if [ ! -f "$RAW_JSON" ]; then
        echo -e "Running getleaderboards.py...this will take a few hours...ZzzZ\n"
        ipython -c "%time %run getleaderboards.py $RAW_JSON"
    else
        while true; do
            read -rep $'Do you want to re-download data from r6stats (takes several hours)? (Y/N)\n' yn
            case $yn in
                [Yy]* ) ipython -c "%time %run getleaderboards.py $RAW_JSON"; break;;
                [Nn]* ) break;;
                * ) echo -e "Answer. Dammit.\n";;
            esac
        done
    fi

    echo "Running json2csv.py..."
    ipython -c "%time %run json2csv.py $RAW_JSON"

    echo "Running features.py..."
    ipython -c "%time %run features.py data/leaderboard-pages.csv"

    echo "done"
    return 0    
}

main "$@"
