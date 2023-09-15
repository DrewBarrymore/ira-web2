// Check if the user is accessing from a Windows PC
const isWindows = /* logic to detect Windows */;

if (isWindows) {
    document.getElementById('download-link').removeAttribute('disabled');
} else {
    document.getElementById('access-message').style.display = 'block';
}

// Handle download button click
document.getElementById('download-link').addEventListener('click', function () {
    document.getElementById('content').style.display = 'none';
    document.getElementById('confirmation').style.display = 'block';

    // Start download tracking and record IP address to CSV file
    const ipAddress = /* logic to get IP address */;
    const downloadTime = new Date().toISOString();
    const csvData = `${ipAddress},${downloadTime}\n`;

    // Send CSV data to server or handle it as needed
    /* AJAX or other logic to save data to CSV */

    // Redirect to home page after a few seconds
    setTimeout(function () {
        window.location.href = 'home.html'; // Replace with your home page URL
    }, 5000); // 5000 milliseconds = 5 seconds
});
