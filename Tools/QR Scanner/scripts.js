document.getElementById('qr-input').addEventListener('change', event => {
    const file = event.target.files[0];
    if (!file) {
        console.error('No file selected');
        return;
    }

    const reader = new FileReader();
    reader.onload = function() {
        const img = new Image();
        img.onload = function() {
            const canvas = document.getElementById('qr-canvas');
            const context = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0, canvas.width, canvas.height);

            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            const code = jsQR(imageData.data, imageData.width, imageData.height);

            if (code) {
                document.getElementById('result').textContent = `URL: ${code.data}`;
            } else {
                document.getElementById('result').textContent = 'No QR code found.';
            }
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
});