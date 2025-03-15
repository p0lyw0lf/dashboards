#!/usr/bin/env bash

set -euo pipefail
shopt -s globstar

output_folder="$1"
mkdir -p $output_folder
output_file="$1.html"
touch $output_file

zcat $output_folder/**/*.gz | sed '/^#/d'
