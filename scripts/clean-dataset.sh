#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

# trap keyboard interrupt (control-c)
# will call control_c function

cleanup() {
    # cleanup function
    # rm data/leaderboard-pages.jsonl
    local status="$?"
    echo -en "\nCleaning up...\n"
    if [ "$status" -ne 0 ]; then
        echo -en "Aborting...\n" >&2
        echo -en "exit($status)\n" >&2
    else
        echo -en "exit(0)\n"
    fi
    return "$status"
}
 
control_c() {
    # run if user hits control-c
    cleanup
    exit $?
}

run_pipeline() {
    START_TIME=$SECONDS
    # convert dataset from .jsonl to .csv. 
    echo -e "running scripts/json2csv.py\n"
    ipython3 -c "%time %run scripts/json2csv.py $(readlink -f data/leaderboard-pages.jsonl)"

    # read the csv data. do some cleaning. save normalize columns to features.csv.
    echo -e "running scripts/features.py\n"
    ipython3 -c "%time %run scripts/features.py $(readlink -f data/leaderboard-pages.csv) --keep-all-cols"

    ipython3 -c "%time %run scripts/features.py $(readlink -f data/leaderboard-pages.csv)"

    echo -e "cleaning up...\n"
    # rm intermediary files. we don't need 'em.
    rm "$(readlink -f data/leaderboard-pages-flat.jsonl)"
    rm "$(readlink -f data/leaderboard-pages.csv)"

    echo -e "done. completed in $(( SECONDS - START_TIME )) seconds.\n"
}

trap control_c SIGINT

main() { 
 run_pipeline   
}

main "$@"
