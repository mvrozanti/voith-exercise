#!/bin/bash

file='../data/historical_data_last_4_days.csv'
container_path='/var/lib/mysql-files'

if [ ! -f "$file" ]; then
  echo "File not found: $file"
  exit 1
fi

echo "Copying $file to MySQL container..."
docker cp "$file" mysql:"$container_path/" || { echo "Failed to copy $file to the container"; exit 1; }

echo "Setting file permissions..."
docker exec -i mysql chmod 644 "$container_path/$(basename "$file")" || { echo "Failed to set permissions"; exit 1; }

echo "Importing data from $file into the database..."
docker exec -i mysql mysql -uroot -prootpass -e "
    LOAD DATA INFILE '$container_path/$(basename "$file")'
    INTO TABLE historical_data
    FIELDS TERMINATED BY ',' ENCLOSED BY '\"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;" timeseries_db || { echo "Failed to import $file"; exit 1; }

echo "Deleting $file from the MySQL container..."
docker exec -i mysql rm "$container_path/$(basename "$file")" || { echo "Failed to delete $file from the container"; exit 1; }

echo "Successfully imported $file"

