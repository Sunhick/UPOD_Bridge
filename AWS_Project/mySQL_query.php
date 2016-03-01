<?php echo "YPOD mySQL Data Import and Display"; ?>

<?php

$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "YPOD";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "INSERT INTO Temperature (tempC, tempF, time)
VALUES ('12', '53', '12:35')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
<html>

<head>
<title>YPOD Data</title>
</head>

<body>

<table width="600" border="1" cellpadding="1" cellspacing="1">
<tr>

<th>Temperature (Celcius)</th>
<th>Temperature (Farenheight) </th>
<th>Time</th>
<tr>
<?php
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "YPOD";

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql2= "SELECT * FROM Temperature";

$records=mysqli_query($conn, $sql2);
while($Temperature=mysqli_fetch_assoc($records)){
	echo "<tr>";
	echo "<td>".$Temperature["tempC"]."</td>";
	echo "<td>".$Temperature["tempF"]."</td>";
	echo "<td>".$Temperature["time"]."</td>";
	echo "</tr>";
}
?>

</table>
</body>
</html>
