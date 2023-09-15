// Check if the user is accessing from a Windows PC
function isWin() {
    const userAgent = navigator.userAgent;
    return /Windows/i.test(userAgent);

}
const isWindows = isWin()


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
    // const ipAddress =  logic to get IP address ;
    // const downloadTime = new Date().toISOString();
    // const csvData = `${ipAddress},${downloadTime}\n`;

    // Send CSV data to server or handle it as needed
    /* AJAX or other logic to save data to CSV */

    // Redirect to home page after a few seconds
    setTimeout(function () {
        window.location.href = 'http://127.0.0.1:8000/ira'; // Replace with your home page URL
    }, 3000); // 5000 milliseconds = 5 seconds
});
