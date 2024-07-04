#!/bin/bash

level=1

if [[ -n $1 ]]
then
  level=$1
fi

if [[ level -lt 1 || level -gt 3 ]]
then
  echo "Invalid $level level! Value needs to be: 1-3."
  exit
fi

example_maze=$(<example_maze_${level}.txt)

dotnet ./DTMazeChallenge.MazeTester.dll "$example_maze" $LANGUAGE $2