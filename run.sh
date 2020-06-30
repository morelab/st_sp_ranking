#!/bin/sh

ORIGIN_DIRECTORTY=$(pwd)
BASEDIR=$(dirname "$0")
{
  cd "$BASEDIR"
  python -m st_sp_ranking.main
} ||{
  :
}
cd "$ORIGIN_DIRECTORTY"