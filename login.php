<?php

  session_start();

  $username = $_POST['username'];

  $password = $_POST['password'];

  if ($username == "user" && $password == "password") {

    $_SESSION['username'] = $username;

    header("Location: home.php");

    exit();

  } else {

    header("Location: login.html");

    exit();

  }

?>

