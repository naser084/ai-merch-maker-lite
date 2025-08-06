<?php
// Get the raw POST data
$json = file_get_contents('php://input');

// Decode it
$data = json_decode($json, true);

// Check if data is valid JSON
if (!$data) {
    echo json_encode([
        "success" => false,
        "message" => "Invalid JSON or no data received."
    ]);
    exit;
}

// Log the product data
file_put_contents("log.txt", date("Y-m-d H:i:s") . " - " . json_encode($data) . PHP_EOL, FILE_APPEND);

// Return fake product ID
echo json_encode([
    "success" => true,
    "message" => "Product received and processed successfully.",
    "product_id" => "product_" . uniqid()
]);
?>
