#!/bin/bash

RED="\033[0;31m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
GREEN="\033[0;32m"
WHITE="\033[0;37m"
OCHRE="\033[38;5;95m"
RESET="\033[0m"

echo -e $BLUE
printf "
\n\t****************************************************************************
\t**                                                                        **
\t**                               FETCHER                                  **
\t**                Usage: ./fetcher.sh /path/to/repos/dir                  **
\t**                                                                        **
\t****************************************************************************\n
"
echo -e $RESET

PATH_TO_REPOS=$1

if [[ -d $PATH_TO_REPOS ]]; then
    for repo_path in $PATH_TO_REPOS/*/; do
        [ -e $repo_path ] || continue
        if git -C $repo_path rev-parse; then
            cd $repo_path
            printf "\n\nREPO:  $repo_path"
            printf "\n----------------------------------------------------------------\n\n"
            if git ls-remote --quiet &> /dev/null; then
                git status
                printf "\n----------------------------------------------------------------\n\n"
                read -p ">>> Fetch? [y/N] " fetchyn
                case $fetchyn in
                    [Yy]* )
                        git fetch --all
                        printf "\n----------------------------------------------------------------\n\n"
                        read -p ">>> Pull? [y/N] " pullyn
                        case $pullyn in
                            [Yy]* ) git pull; continue;;
                            [Nn]* ) continue;;
                            * ) printf "Enter Y[y] or N[n]"
                        esac
                        ;;
                    [Nn]* ) 
                        continue;;
                    * ) printf "Enter Y[y] or N[n]"
                esac
            else
                echo -e $RED
                printf ">>> ERROR: remote repository not found\n"
                echo -e $RESET
                continue
            fi
        fi
    done
fi
