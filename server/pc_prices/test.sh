#! /bin/bash


# Selection Menu ------------------------------------------------------------
shopt -u | grep -q dotglob && dgchanged=true && shopt -s dotglob
shopt -u | grep -q nullglob && ngchanged=true && shopt -s nullglob
array=(Pricing/*/)
echo
PS3="Select system to pull :"
select dir in "${array[@]}"; do echo "Updating CSV in ${dir}"; break; done
echo
[ $dgchanged ] && shopt -u dotglob; unset dgchanged
[ $ngchanged ] && shopt -u nullglob; unset ngchanged

echo "preparing to wget data"

# ---------------------------------------------------------------------------

# Delete CSV from last use
rm "$dir"sellrate.csv

while read line1
do read line2
   # Download page listed in index
   wget "$line1" -q -O temphtml.txt
   if [ $? -ne 0 ]; then
      echo "Wget failed to download page"
   fi

   # Extract sell-through rates
   grep 'sales per\|sale per' temphtml.txt > temp.txt

   # strip leading indent
   sed "s/^[ \t]*//" -i temp.txt
   # strip html and seperate game conditions
   sed "s/<[^>]*>//g" -i temp.txt
   loosestring=$(sed -n 1p temp.txt)
   loosenumber=$(echo "$loosestring" | tr -dc '0-9')
   cibstring=$(sed -n 2p temp.txt)
   cibnumber=$(echo "$cibstring" | tr -dc '0-9')
   newstring=$(sed -n 3p temp.txt)
   newnumber=$(echo "$newstring" | tr -dc '0-9')

   # FIXME Debug
   echo "loose : $loosestring, $loosenumber"
   echo "loose : $cibstring, $cibnumber"
   echo "loose : $newstring, $newnumber"

   # convert all 3 from day, week, year to month
   if [[ $loosestring == *"day"* ]]; then
      let "loosenumber *= 30"
   elif [[ $loosestring == *"week"* ]]; then
      let "loosenumber *= 4"
   elif [[ $loosestring == *"year"* ]]; then
      let "loosenumber = 0"
   fi

   if [[ $cibstring == *"day"* ]]; then
      let "cibnumber *= 30"
   elif [[ $cibstring == *"week"* ]]; then
      let "cibnumber *= 4"
   elif [[ $cibstring == *"year"* ]]; then
      let "cibnumber = 0"
   fi
   
   if [[ $newstring == *"day"* ]]; then
      let "newnumber *= 30"
   elif [[ $newstring == *"week"* ]]; then
      let "newnumber *= 4"
   elif [[ $newstring == *"year"* ]]; then
      let "newnumber = 0"
   fi

   # TODO name, loosesell, cibsell, newsell, url
   # write out data ----------------------------------------------------------
   #      name   loosesell     cibsell   newsell    url  
   echo "$line2,$loosenumber,$cibnumber,$newnumber,$line1 "
   echo "$line2,$loosenumber,$cibnumber,$newnumber,$line1 " >> "$dir"sellrate.csv

   # randomized sleep
   randsleeptime=$RANDOM
   let "randsleeptime %= 8"
   echo "sleeping for $randsleeptime seconds"
   sleep $randsleeptime

done < "$dir"index.txt

# cleanup from this use
rm ./temphtml.txt
rm ./temp.txt

echo "Completed creating CSV"
