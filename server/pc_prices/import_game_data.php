#!/usr/bin/php
<?php
//  usage: from import_game_data.php directory
//  import_game_data.php test.csv

$servername = 'localhost';
$username = 'user';
$password = 'goodwillsp';
$datab = 'game_pricing';

// --------------------------------------------------------------------
// ARGUMENT: CSV File to be imported

$argv = $_SERVER['argv'];
if($argc <= 1) {
   echo "Usage: import_game_data.php filename console highlight \n";
   echo "   ie. import_game_data.php Pricing/PS-2/pricing.csv PS-2 cib\n"; 
   exit;
}
if($argv[1]) { $file = $argv[1];}
else {
   echo "Please provide a file name\n";
   exit; 
}
if($argv[2]) {$makeconsole = $argv[2];}
else {
   echo "Please provide console name(i.e. PS-2)\n";
   exit;
}
if($argv[3]) {
   if ($argv[3] == 'loose'){ $highlight = '0';}
   elseif ($argv[3] == 'cib'){ $highlight = '1';}
   else{
      echo "highlighting must be either loose or cib\n";
      exit;
   }
}
else {
   echo "Please state: loose or cib\n";
   exit;
}
// --------------------------------------------------------------------

// Create connection
$conn = mysqli_connect($servername, $username, $password, $datab);

// Check connection
if (!$conn) {
   die("Connection failed: " . mysqli_connect_error());
}

$row = 1;
if (($handle = fopen($file, "r")) !== FALSE) {
   // Main update loop
   while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
      $num = count($data);
      // verify 7 fields in row
      if ($num != 7) {
         echo "malformed line: $row\n";  
      }
      else {
         $activeid = $data['5'];
         // query for game by id from csv
         $result = mysqli_query($conn, "SELECT * FROM gameprices WHERE 
                                        id = '$activeid' LIMIT 1");
         // IF game exists in database
         if ($dbrow = mysqli_fetch_assoc($result)) {
            echo "Updating :" . $dbrow['Title'] . "\n";
            $updateloose = $data['1'];
            $updatecib = $data['2'];
            $updatenew = $data['3'];

            $sql = "UPDATE gameprices SET `PriceLoose`='$updateloose',
                    `PriceCIB`='$updatecib', `Console`='$makeconsole', `PriceNew`='$updatenew',
                    `Highlight`='$highlight' WHERE `id`='$activeid'";

            if (!mysqli_query($conn, $sql)) {
               echo "Error: " . $sql . "\n" . mysqli_error($conn);
            }
         }
         // IF game doesn't exist in database
         else { 
            echo "Creating :" . $data['0'] . "\n";
            $makeid = $data['5'];
            $maketitle = $data['0'];
            // add escape characters to title
            $maketitle = addslashes($maketitle);
            $makebarcode = $data['4'];
            $makeloose = $data['1'];
            $makecib = $data['2'];
            $makenew = $data['3'];
            $makeweblink = $data['6'];
            // add escape characters to hyperlink
            $makeweblink = addslashes($makeweblink);

            $sql = "INSERT INTO `game_pricing`.`gameprices` (`id`, 
                    `Title`, `Console`, `Barcode`, `PriceLoose`, 
                    `PriceCIB`, `PriceNew`, `Highlight`, `Weblink`) 
                    VALUES 
                    ('$makeid', '$maketitle', '$makeconsole', 
                     '$makebarcode', '$makeloose', '$makecib', 
                     '$makenew', '$highlight','$makeweblink');";
            if (!mysqli_query($conn, $sql)) {
               echo "Error: " . $sql . "\n" . mysqli_error($conn);
            }
         }
      }
   }
   // cleanup
   mysqli_close($conn);
   fclose($handle);
}
?>

