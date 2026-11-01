# bash scripting tutorial - full course by terminal velocity
# https://www.youtube.com/watch?v=4ygaA_y1wvQ

#!/usr/bin/env bash
set -euo pipefail

echo "this message was an echo"

language="bash script"
echo "this is a $language program"

pwd

hour=14

if (( hour >= 7 && hour < 12 )); then
    state="morning"
elif (( hour >= 12 && hour < 21 )); then
    state="afternoon"
else
    state="night"
fi

echo "at $hour it is the $state"

# string comparations
val="a"
[[ "$val" == "a" ]] # equal
[[ "$val" != "b" ]] # not equal

# numerical comparaitions
num=1
[[ "$num" -eq 1 ]] # equal
[[ "$num" -ne 2 ]] # not equal
[[ "$num" -lt 3 ]] # less than
[[ "$num" -le 4 ]] # less than or equal
[[ "$num" -gt 0 ]] # greater than
[[ "$num" -ge 1 ]] # greater than or equal

# variable existence
val=""
[[ -z $val ]] # var is null
[[ -n $num ]] # var is not null

# file checks and permition checks
file="./bash.sh"
dir=../examples
[[ -f $file ]] # file exists
[[ -d $dir ]] # dir exists
[[ -e $file ]] # file/dir exists
[[ -r $file ]] # file is readable
[[ -w $file ]] # file is writable
[[ -x $file ]] # file is executable

# combinations internal and external 
val=7
[[ $val -gt 5 && $val -lt 10 ]] # logical AND
[[ $val -lt 8 || $val -gt 16 ]] # logical OR
[[ $val -gt 5 ]] && [[ $val -lt 10 ]] # logical AND
[[ $val -lt 8 ]] || [[ $val -gt 16 ]] # logical OR

array=(26 52 78)
echo "array: ${array[@]}" # @ refers to all the elementa
index=1
echo "array at index $index is ${array[index]}"
echo "the lenth of the array is ${#array[@]}"

total=0
for item in "${array[@]}"; do
    total=$((total + item))
done
echo "the total of the array is $total"

# iterate
for ((i = 0; i < 10; i++)); do
    continue
done

# range
for i in {1..10}; do
    continue
done

# pattern matching
for item in ./*.sh; do
    continue
done

# command result
for item in $(ls); do
    continue
done

counter=0
while [[ $counter -lt 5 ]]; do
    ((++counter))
done

greater_than() {z
    local num_A=$1
    local num_B=$2
    if [[ $num_A -gt $num_B ]]; then
        return 0
    else
        return 1
    fi
}

num_A=5
num_B=7
if greater_than "$num_A" "$num_B"; then
    echo "$num_A is greater than $num_B"
else
    echo "$num_A is not greater than $num_B"
fi

false

echo "whats your name?"
read -r name
sleep 1
echo "hello $name"
