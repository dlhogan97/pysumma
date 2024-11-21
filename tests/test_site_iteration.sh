#!/bin/bash

# Define your sets of inputs
site_codes=("679:WA:SNTL" "791:WA:SNTL" "642:WA:SNTL" "909:WA:SNTL") # "974:WA:SNTL" "863:WA:SNTL" "679:WA:SNTL" "791:WA:SNTL"  "788:WA:SNTL" "672:WA:SNTL")
site_names=("Paradise" "Stevens_Pass" "Morse_Lake" "Wells_Creek") # "Waterhole" "White Pass" "Stampede Pass" "Olallie Meadows")

# Get the length of the arrays
length=${#site_codes[@]}

# Initialize the water_years array
water_years=()
for ((i = 0; i < length; i++)); do
    water_years+=("2025")
done

# Initialize the output_names array
output_names=()
for site_name in "${site_names[@]}"; do
    output_names+=("$site_name")
done

# Loop over the arrays
for ((i=0; i<$length; i++)); do
  # Get the inputs for this iteration
  input1=${site_codes[$i]}
  input2=${water_years[$i]}
  input3=${output_names[$i]}

  # Provide input to the first Python script
  echo -e "$input1\n$input2\n$input3" | python3 ./src/snotel_to_pysumma.py

  echo "forcing file created, now running summa"

  # Replace the content of the text file with input3
  echo "'$input3.nc'" > src/forcings/forcing_file_list.txt

  # Run the second Python script
  python3 ./src/run_summa.py

  echo "summa run for $input3 complete, check output folder for output file"

done