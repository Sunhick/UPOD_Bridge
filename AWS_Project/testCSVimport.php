<?php  
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "ypod";

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

if ($_FILES[csv][size] > 0) { 
    set_time_limit(10000);
    $count = 0;
    $status = FALSE;
    //get the csv file 
    $file = $_FILES[csv][tmp_name]; 
    $handle = fopen($file,"r"); 
     
    // read header
    $data = fgetcsv($handle);

    // read the valid entry afer header
    $data = fgetcsv($handle);
    //loop through the csv file and insert into database 
    do  { 
        if ($data[0]) { 
        $sql = "INSERT INTO education_ypod (`Rtc Date`, `Rtc Time`, `BMP Temp(C)`, `BMP Pres(mb)`,  `SHT25 Temp(C)`, `SHT25 Humidity`,`CO2(ADC VAL)`,`Wind Speed(mph)`,`Wind Direction(deg)`,`Quad-Aux-1(microVolts)`,`Quad-Main-1(microVolts)`,`Quad-Aux-2(microVolts)`,`Quad-Main-2(microVolts)`,`Quad-Aux-3(microVolts)`,`Quad-Main-3(microVolts)`,`Quad-Aux-4(microVolts)`,  `Quad-Main-4(microVolts)`,`Fig 210 Heat(milliVolts)`,   `Fig 210 Sens(milliVolts)`,   `Fig 280 Heat(milliVolts)`,   `Fig 280 Sens(milliVolts)`,   `BL Moccon sens(milliVolts)`, `ADC2 Channel-2(empty)`,  `E2VO3 Heat(milliVolts)`, `E2VO3 Sens(milliVolts)`, `GPS Date`,   `GPS Time(UTC)`,  `Latitude`,   `Longitude`,  `Fix Quality`, `Altitude(meters above sea level)`,   `Statellites`) VALUES
                ( 
                    '".addslashes($data[0])."', 
                    '".addslashes($data[1])."', 
                    '".addslashes($data[2])."',
                    '".addslashes($data[3])."', 
                    '".addslashes($data[4])."', 
                    '".addslashes($data[5])."',
                    '".addslashes($data[6])."', 
                    '".addslashes($data[7])."', 
                    '".addslashes($data[8])."',
                    '".addslashes($data[9])."', 
                    '".addslashes($data[10])."', 
                    '".addslashes($data[11])."',
                    '".addslashes($data[12])."', 
                    '".addslashes($data[13])."', 
                    '".addslashes($data[14])."',
                    '".addslashes($data[15])."', 
                    '".addslashes($data[16])."', 
                    '".addslashes($data[17])."',
                    '".addslashes($data[18])."', 
                    '".addslashes($data[19])."', 
                    '".addslashes($data[20])."',
                    '".addslashes($data[21])."', 
                    '".addslashes($data[22])."', 
                    '".addslashes($data[23])."',
                    '".addslashes($data[24])."', 
                    '".addslashes($data[25])."', 
                    '".addslashes($data[26])."',
                    '".addslashes($data[27])."',
                    '".addslashes($data[28])."', 
                    '".addslashes($data[29])."', 
                    '".addslashes($data[30])."',
                    '".addslashes($data[31])."' 
                ) ;";    

             $status = $conn->query($sql);

        if ($status === TRUE) {
           echo "<p> $count inserted! </p>\n";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
        } 
        //print_r($data);
        // echo "\n";
        //echo $sql;
      
        unset($data);
        $count++;
    } //while ($data = fgetcsv($handle,2000,",", "'")); 
    while ($data = fgetcsv($handle)); 

    // $status = $conn->query($sql);
    // if ($status === TRUE) {
    //     echo "<p> inserted! </p>\n";
    // } else {
    //     echo "Error: " . $sql . "<br>" . $conn->error;
    // }
    //echo $sql;
    //redirect 
    header('Location: import.php?success=1'); die; 

}
$conn->close(); 

?> 

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" /> 
<title>Import a CSV File with PHP & MySQL</title> 
</head> 

<body> 

<?php if (!empty($_GET[success])) { echo "<b>Your file has been imported.</b><br><br>"; } //generic success notice ?> 

<form action="" method="post" enctype="multipart/form-data" name="form1" id="form1"> 
  Choose your file: <br /> 
  <input name="csv" type="file" id="csv" /> 
  <input type="submit" name="Submit" value="Submit" /> 
</form> 

</body> 
</html> 