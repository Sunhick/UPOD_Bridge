<?PHP
include("auth.php"); //include auth.php file on all secure pages
$uploaded = $_FILES['csv']['name'];
if ($_FILES[csv][size] > 0) { 
$hostname = "localhost";
$username = "root";
$password = "hanniganlab";

// Connect to Database and Table
$dbhandle = mysql_connect($hostname, $username, $password)
    or die("Unable to connect to MySQL");

$selectdatabase = mysql_select_db("ypod",$dbhandle)
    or die("Could not select ypod database");

// Text File to read in
$uploaded = $_FILES['csv']['name'];
move_uploaded_file($_FILES["csv"]["tmp_name"],
            "C:\Bitnami\wampstack-5.6.19-0\apache2\htdocs\login-site/" . $_FILES["csv"]["name"]);

$requiredHeaders = array("Rtc Date","Rtc Time","BMP Temp(C)",
"BMP Pres(mb)", "SHT25 Temp(C)", "SHT25 Humidity", "CO2(ADC VAL)",
"Wind Speed(mph)", "Wind Direction(deg)", "Quad-Aux-1(microVolts)",
"Quad-Main-1(microVolts)", "Quad-Aux-2(microVolts)", "Quad-Main-2(microVolts)",
"Quad-Aux-3(microVolts)", "Quad-Main-3(microVolts)", "Quad-Aux-4(microVolts)",
"Quad-Main-4(microVolts)", "Fig 210 Heat(milliVolts)", "Fig 210 Sens(milliVolts)",
"Fig 280 Heat(milliVolts)", "Fig 280 Sens(milliVolts)", "BL Moccon sens(milliVolts)",
"ADC2 Channel-2(empty)", "E2VO3 Heat(milliVolts)", "E2VO3 Sens(milliVolts)", "GPS Date", "GPS Time(UTC)",
"Latitude", "Longitude", "Fix Quality", "Altitude(meters above sea level)", "Statellites"); //headers we expect

$f = fopen($uploaded, 'r');
$firstLine = fgets($f); //get first line of csv file
fclose($f);


$foundHeaders = str_getcsv(trim($firstLine), ',', '"'); //parse to array

if ($foundHeaders !== $requiredHeaders) {
   die('.csv file does not match required format. Make sure youre uploading a valid POD file.<br>' . mysql_error());
}

else if($foundHeaders == $requiredHeaders){
if (!empty($uploaded)) {
	$query = "LOAD DATA LOCAL INFILE '" . $uploaded . "' INTO TABLE AQIQ_raw FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES ";
	mysql_query($query) 
		or die('Error Loading Data File.<br>' . mysql_error());
	echo "Upload success!";
	if (is_file($uploaded)) {
		unlink($uploaded );
	}

	//Data processing to be addded here.
	$processing = "INSERT INTO `aqiq_processed`(`userid`, `session_id`, `Rtc Date (GMT)`,
	`Rtc Time (GMT)`,`BMP Temp(C)`,`BMP Pres(mb)`,`SHT25 Temp(C)`,`SHT25 Humidity`,
	`CO2(ppm)`,`Wind Speed(mph)`,`Wind Direction(deg)`,`Quad-Aux1`,
	`Quad-Main1`,`Quad-Aux2`,`Quad-Main2`,`Quad-Aux3`,`Quad-Main3`,
	`Quad-Aux4`,`Quad-Main4`, `Fig 210 Heat`,`Fig 210 Sens`,`Fig 280 Heat`,
	`Fig 280 Sens`,`BL Moccon`, `E2VO3(heat)`, `E2VO3(sens ppb)`, `GPS Date`,
	`GPS Time(UTC)`,`Latitude`,`Longitude`, `Fix Quality`,
	`Altitude(meters above sea level)`, `Satellites`)
	SELECT `userid`,
	`session_id`,
	`Rtc Date`,
	`Rtc Time`,
	(`BMP Temp(C)`*9.0)/5.0 + 32,
	`BMP Pres(mb)`,
	`SHT25 Temp(C)`,
	`SHT25 Humidity`,
	`CO2 (ADC VAL)`,
	`Wind Speed(mph)`,
	`Wind Direction(deg)`,
	`Quad-Aux-1(microVolts)`,
	`Quad-Main-1(microVolts)`,
	`Quad-Aux-2(microVolts)`,
	`Quad-Main-2(microVolts)`,
	`Quad-Aux-3(microVolts)`,
	`Quad-Main-3(microVolts)`,
	`Quad-Aux-4(microVolts)`,
	`Quad-Main-4(microVolts)`,
	`Fig 210 Heat(milliVolts)`,
	`Fig 210 Sens(milliVolts)`,
	`Fig 280 Heat(milliVolts)`,
	`Fig 280 Sens(milliVolts)`,
	`BL Moccon sens(milliVolts)`,
	`E2VO3 Heat(milliVolts)`,
	`E2VO3 Sens(milliVolts)`,
	`GPS Date`,
	`GPS Time (UTC)`,
	`Latitude`, 
	`Longitude`, 
	`Fix Quality`, 
	`Altitude(meters above sea level)`, 
	`Satellites`

	FROM `aqiq_raw`";
	mysql_query($processing)
		or die ('Error Loading Data File.<br>' . mysql_error());
}
}
}
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
  Choose your POD file to be uploaded and processed: <br /> 
  <input name="csv" type="file" id="csv" /> 
  <input type="submit" name="Submit" value="Submit" /> 
</form>

<div class="form">
<p>Welcome <?php echo $_SESSION['username']; ?>!</p>
<p><a href="dashboard.php">Download Processed Data</a></p>
<a href="logout.php">Logout</a>
</div>
</body> 
</html> 
