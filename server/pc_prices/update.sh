#! /bin/bash

# Price Bracket Settings
# i.e.) 27.99 is changed to 24.99 (5 & 20) but 17.99 stays
pricebracketing=5
pricebracketbegin=20

# Selection Menu ------------------------------------------------------------
shopt -u | grep -q dotglob && dgchanged=true && shopt -s dotglob
shopt -u | grep -q nullglob && ngchanged=true && shopt -s nullglob
array=(Pricing/*/)
echo
PS3="Select system to update :"
select dir in "${array[@]}"; do echo "Updating CSV in ${dir}"; break; done
echo
[ $dgchanged ] && shopt -u dotglob; unset dgchanged
[ $ngchanged ] && shopt -u nullglob; unset ngchanged

echo "preparing to wget data"

# Pricing coefficents --------------------------------------------------------
source "$dir"price-config
function apply_settings {
   # pricing brackets
   gameislow=`echo "$tempmathvar < 8" | bc`
   gameismid=`echo "($tempmathvar > 7.99) && ($tempmathvar < 20)" | bc`
   gameishigh=`echo "$tempmathvar > 19.99" | bc`
   if [ $gameislow -eq 1 ]; then
     tempmathvar=`echo "scale=2; $tempmathvar * $pricingcoefficientlow"| bc`
   fi
   if [ $gameismid -eq 1 ]; then
     tempmathvar=`echo "scale=2; $tempmathvar * $pricingcoefficientmid"| bc`
   fi
   if [ $gameishigh -eq 1 ]; then
     tempmathvar=`echo "scale=2; $tempmathvar * $pricingcoefficienthigh"| bc`
   fi
   tempmathvar=`echo "($tempmathvar+0.5)/1" | bc`
   if [ $tempmathvar -gt $pricebracketbegin ]; then
      tempmathvar=`echo "($tempmathvar / $pricebracketing) * $pricebracketing"| bc`
   fi
}

# price calculation loop vars -----------------------------------------------
ciblineindex=0
newlineindex=0
uselineindex=0
eoflineindex=0
cibgameprice=0
usegameprice=0
newgameprice=0
cibdatamissing=0
usedatamissing=0
newdatamissing=0
gamechartiterator=0
verifyindexline=0
lineoffset=0
tempmathvar=0
# ---------------------------------------------------------------------------

# Delete CSV from last use
rm "$dir"pricing.csv

while read line1
do read line2
   # Download page listed in index
   wget "$line1" --no-check-certificate -q -O temphtml.txt
#   curl -L "$line1" > temphtml.txt
   if [ $? -ne 0 ]; then
      echo "Wget failed to download page"
   fi

   # Testing REMOVE ME
   echo "$line1"

   # Extract chart data
   grep "chart_data" temphtml.txt > temp.txt

   # Format chart data
   sed -e 's/[0-9]\{13\},//g' -e 's/VGPC.chart_data = //g' -e 's/\],\[/\n/g' -e 's/\[\[/\n/g' -e 's/\]\]/\n/g' -e 's/[ }{,:;]//g' temp.txt > tempchartdata.txt

   # Get condition indicies
   ciblineindex=$(sed -n '/cib/=' tempchartdata.txt)
   newlineindex=$(sed -n '/new/=' tempchartdata.txt)
   uselineindex=$(sed -n '/use/=' tempchartdata.txt)
   gradedlineindex=$(sed -n '/graded/=' tempchartdata.txt)
   eoflineindex=$(sed -n '$=' tempchartdata.txt)

   # Get CIB history array
   lineoffset=12
   verifyindexline=$(($ciblineindex + $lineoffset))
   if [ $verifyindexline -lt $gradedlineindex ]; then
      gamechartiterator=$gradedlineindex
      for (( i = 1; i <= 12; i++ ))
      do
         let "gamechartiterator--"
         cibgamehistory[$i]=$(sed -n "${gamechartiterator}p" tempchartdata.txt)
      done
      cibdatamissing=0
   else
      cibdatamissing=1
   fi

   #get USED history array
   lineoffset=12
   verifyindexline=$(($uselineindex + $lineoffset))
   if [ $verifyindexline -lt $eoflineindex ]; then
      gamechartiterator=$eoflineindex
      for (( i = 1; i <= 12; i++ ))
      do
         let "gamechartiterator--"
         usegamehistory[$i]=$(sed -n "${gamechartiterator}p" tempchartdata.txt)
      done
      usedatamissing=0
   else
      usedatamissing=1
   fi

   #get NEW history array
   lineoffset=12
   verifyindexline=$(($newlineindex + $lineoffset))
   if [ $verifyindexline -lt $uselineindex ]; then
      gamechartiterator=$uselineindex
      for (( i = 1; i <= 12; i++ ))
      do
         let "gamechartiterator--"
         newgamehistory[$i]=$(sed -n "${gamechartiterator}p" tempchartdata.txt)
      done
      newdatamissing=0
   else
      newdatamissing=1
   fi

   # COVID OVERRIDE
   startmonth=1
   # endmonth=12
   endmonth=3
   # totalmonths=12
   totalmonths=3


   # calculate average prices and apply settings
   # -------------------------------------------------------------------
   # new game calculations
   if [ $newdatamissing -eq 0 ]; then
      tempmathvar=0
      for ((i=startmonth; i<=endmonth; i++))
      do
         tempmathvar=`echo "scale=2; ${newgamehistory[$i]} /100 + $tempmathvar" | bc`
         # TEMP
         echo "(${newgamehistory[$i]})"
      done
      tempmathvar=`echo "scale=2; $tempmathvar / $totalmonths" | bc`
         # TEMP
         echo "[$tempmathvar]"
      apply_settings
      newgameprice=`echo "scale=2; $tempmathvar - 0.01" | bc`
   else
      newgameprice="ND"
   fi

   # --------------------------------------------------------------------
   # cib game calculations
   if [ $cibdatamissing -eq 0 ]; then
      tempmathvar=0
      for ((i=startmonth; i<=endmonth; i++))
      do
         tempmathvar=`echo "scale=2; ${cibgamehistory[$i]} /100 + $tempmathvar" | bc`
      done
      tempmathvar=`echo "scale=2; $tempmathvar / $totalmonths" | bc`
      apply_settings 
      cibgameprice=`echo "scale=2; $tempmathvar - 0.01" | bc`
   else
      cibgameprice="ND"
   fi

   # ---------------------------------------------------------------------
   # used game calculations
   if [ $usedatamissing -eq 0 ]; then
      tempmathvar=0
      for ((i=startmonth; i<=endmonth; i++))
      do
         tempmathvar=`echo "scale=2; ${usegamehistory[$i]} /100 + $tempmathvar" | bc`
      done
      tempmathvar=`echo "scale=2; $tempmathvar / $totalmonths" | bc`
      apply_settings
      usegameprice=`echo "scale=2; $tempmathvar - 0.01" | bc`
   else
      usegameprice="ND"
   fi

   # ----------------------------------------------------------------------
   # get VGPC uid
   grep -A 5 "VGPC.product" temphtml.txt > temp.txt
   grep -w "id" temp.txt > tempid.txt
   gameidnumber=$(sed 's/[^0-9]//g' tempid.txt)

   # get game upc
   grep -A 6 "UPC:" temphtml.txt > temp.txt
   grep '[0-9]\{12\}' temp.txt > tempupc.txt
   gameupc=$(sed 's/[^0-9]//g' tempupc.txt)

   # write out data ----------------------------------------------------------
   #      name   used          cib           new           upc      id            url  
   echo "$line2,$usegameprice,$cibgameprice,$newgameprice,$gameupc,$gameidnumber,$line1 "
   echo "$line2,$usegameprice,$cibgameprice,$newgameprice,$gameupc,$gameidnumber,$line1 " >> "$dir"pricing.csv

   # randomized sleep
   randsleeptime=$RANDOM
   let "randsleeptime %= 5"
   echo "sleeping for $randsleeptime seconds"
   sleep $randsleeptime

done < "$dir"index.txt

# cleanup from this use
# rm ./tempchartdata.txt
# rm ./temphtml.txt
rm ./tempid.txt
rm ./tempupc.txt
# rm ./temp.txt

echo "Pricing Update Completed on CSV"
echo
read -p "Update Database (y or n)? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
   ./import_game_data.php "$dir"pricing.csv "$gamesysname" "$defaultcondition"
fi
