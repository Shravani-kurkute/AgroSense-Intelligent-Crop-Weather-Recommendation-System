
<?php
// signup.php

// --- Database connection ---
$host = "localhost";
$user = "root";          // your MySQL username
$pass = "";              // your MySQL password
$db   = "agripredict";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// --- Get POST data ---
$fullname = trim($_POST['fullname'] ?? '');
$village  = trim($_POST['village'] ?? '');
$region   = trim($_POST['region'] ?? '');
$mobile   = trim($_POST['mobile'] ?? '');
$password = $_POST['password'] ?? '';
$confirm_password = $_POST['confirm_password'] ?? '';

// --- Basic validation ---
$errors = [];

if (!$fullname || !$village || !$region || !$mobile || !$password || !$confirm_password) {
    $errors[] = "All fields are required.";
}

if (!preg_match('/^\d{10}$/', $mobile)) {
    $errors[] = "Mobile number must be exactly 10 digits.";
}

if (strlen($password) < 6) {
    $errors[] = "Password must be at least 6 characters.";
}

if ($password !== $confirm_password) {
    $errors[] = "Passwords do not match.";
}

if ($errors) {
    foreach ($errors as $err) {
        echo "<p style='color:red;'>$err</p>";
    }
    echo "<p><a href='signup.html'>Go back to Sign Up</a></p>";
    exit;
}

// --- Check if mobile already exists ---
$stmt = $conn->prepare("SELECT id FROM users WHERE mobile = ?");
$stmt->bind_param("s", $mobile);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    echo "<p style='color:red;'>This mobile number is already registered.</p>";
    echo "<p><a href='signup.html'>Go back to Sign Up</a></p>";
    exit;
}

$stmt->close();

// --- Insert new user ---
$password_hash = password_hash($password, PASSWORD_BCRYPT);

$stmt = $conn->prepare("INSERT INTO users (fullname, village, region, mobile, password_hash) VALUES (?, ?, ?, ?, ?)");
$stmt->bind_param("sssss", $fullname, $village, $region, $mobile, $password_hash);

if ($stmt->execute()) {
    // Success → redirect to dashboard or login page
    header("Location: login.html");
    exit;
} else {
    echo "<p style='color:red;'>Error: " . $stmt->error . "</p>";
    echo "<p><a href='signup.html'>Go back to Sign Up</a></p>";
}

$stmt->close();
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriPredict - Sign Up</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }

        body {
            
            background: url('farm_image.png') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .signup-container {
            background: #ffffff6d;
            padding: 50px 40px;
            border-radius: 15px;
            width: 400px;
            max-width: 90%;
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .signup-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        }

        .signup-container h1 {
            color: #2c7a2c;
            margin-bottom: 25px;
        }

        .signup-container p {
            color: #666;
            margin-bottom: 30px;
        }

        .signup-container input {
            width: 100%;
            padding: 12px 15px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        .signup-container input:focus {
            outline: none;
            border-color: #4caf50;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.5);
        }

        .signup-btn {
            width: 100%;
            padding: 12px;
            margin-top: 20px;
            background-color: #4caf50;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
        }

        .signup-btn:hover {
            background-color: #2c7a2c;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .login-link {
            margin-top: 20px;
            color: #666;
            font-size: 14px;
        }

        .login-link a {
            color: #4caf50;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .login-link a:hover {
            color: #2c7a2c;
        }

        @media (max-width: 480px) {
            .signup-container {
                padding: 40px 25px;
            }
        }
    </style>
</head>
<body>
    <div class="signup-container">
        <h1>AgriPredict</h1>
        <p>Create your account</p>
        <form action="signup.php" method="post" accept-charset="UTF-8">
          <input type="text" name="fullname" placeholder="Full Name" required>
          <input type="text" name="village" placeholder="Village" required>
          <input type="text" name="region" placeholder="Region" required>
          <input type="tel" name="mobile" placeholder="Mobile No." pattern="\d{10}" maxlength="10" required>
          <input type="password" name="password" placeholder="Password (min 6 chars)" minlength="6" required>
          <input type="password" name="confirm_password" placeholder="Confirm Password" minlength="6" required>
          <button type="submit" class="signup-btn">Sign Up</button>
        </form>
        
        <div class="login-link">
            Already have an account? <a href="login.html">Login</a>
        </div>
    </div>
</body>
</html>
