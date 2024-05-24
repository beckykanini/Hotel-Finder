<?php 

include "config.php";

    if (isset($_POST['update'])) {
        $username = $_POST['username'];
        $email = $_POST['email'];
        $passwd = $_POST['passwd'];
        $sql = "UPDATE admin SET 'username'='$username','email'='$email','passwd'='$passwd'"; 

        $result = $conn->query($sql); 
        if ($result == TRUE) {
            echo "Record updated successfully.";
        }else{
            echo "Error:" . $sql . "<br>" . $conn->error;
        }
    } 

?>

</body>
</html> 