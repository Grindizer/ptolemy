#! /bin/bash

source_files="$(find src -type f -name '*.yaml')"
for source_file in $source_files; do
  source_file_without_extension=${source_file%.*}
  source_file_with_json_extension=${source_file_without_extension}.json
  destination_file=mappings${source_file_with_json_extension#src}
  mkdir -p "$(dirname $destination_file)"
  ptolemy $source_file > $destination_file
done
