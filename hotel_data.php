<?php
    if (isset($_POST['hotel_name'], $_POST['country'], $_POST['area'], $_POST['amenities'], $_POST['room_services'], $_POST['room_types'])) {
        header("Location: /login.html");
    }

    // Retrieve hotel form data
    $hotel_name = $_POST['hotel_name'];
    $country = $_POST['country'];
    $area = $_POST['area'];
    $amenities = $_POST['amenities'];
    $room_services = $_POST['room_services'];
    $room_types = $_POST['room_types'];

    // Database connection parameters
    $servername = "localhost";
    $usernameDB = "root";
    $passwordDB = "";
    $dbname = "hrs";

    // Create connection
    $conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }


    // Insert hotel data into table
    $query = $conn->prepare("INSERT INTO hotel_data (hotel_name, country, area, amenities, room_services, room_types) VALUES (?, ?, ?, ?, ?, ?)");
    $query->bind_param("ssssss", $hotel_name, $country, $area, $amenities, $room_services, $room_types);

    if ($query1->execute()) {
        echo "Hotel data added successfully!";
    } else {
        echo "Error: " . $query->error;
    }
?>