#!/usr/bin/env bash
# -*- coding: utf-8 -*- 

# this calls the getleaderboards.py script and saves all leaderboard data
# to an output file. the data is saved as a .jsonl (line delim json)
# 

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

run_getleaderboards() {
    RAW_JSON="$(readlink -f data/leaderboard-pages.jsonl)"
    if [ ! -f "$RAW_JSON" ]; then
        echo -e "Running getleaderboards.py...this will take a few hours...ZzzZ\n"
        ipython -c "%time %run getleaderboards.py $RAW_JSON"
        return "$?"
    else
        while true; do
            read -rep $'Do you want to re-download data from r6stats (takes several hours)? (Y/N)\n' yn
            case $yn in
                [Yy]* ) ipython3 -c "%time %run getleaderboards.py $RAW_JSON"; break;;
                [Nn]* ) break;;
                * ) echo -e "Answer. Dammit.\n";;
            esac
        done
        return "$?"
    fi
}
 
# trap keyboard interrupt (control-c)
# will call control_c function
trap control_c SIGINT
main() {
    run_getleaderboards
}

main "$@"
