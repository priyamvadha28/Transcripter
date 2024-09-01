<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['video']) && $_FILES['video']['error'] === UPLOAD_ERR_OK) {
        $targetDir = 'uploads/'; // Specify the directory where you want to store uploaded videos.
        $targetFile = $targetDir . basename($_FILES['video']['name']);

        if (move_uploaded_file($_FILES['video']['tmp_name'], $targetFile)) {
            echo 'Video uploaded successfully!';
        } else {
            echo 'Error uploading the video.';
        }
    } else {
        echo 'Please select a video file to upload.';
    }
}
?>
