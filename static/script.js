document.addEventListener("DOMContentLoaded", function() {
    const analyzeButton = document.getElementById('analyzeButton');
    const imageUpload = document.getElementById('imageUpload');
    const productList = document.getElementById('productList');

    analyzeButton.addEventListener('click', function() {
        const file = imageUpload.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('image', file);

            // Send the image to the backend for analysis
            fetch('http://localhost:5000/analyze', { // Replace with your backend URL
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                // Clear previous recommendations
                productList.innerHTML = '';

                // Display recommended products
                data.recommendations.forEach(product => {
                    const productDiv = document.createElement('div');
                    productDiv.classList.add('product');
                    productDiv.innerHTML = `
                        <img src="${product.imageUrl}" alt="${product.name}">
                        <h4>${product.name}</h4>
                        <p>$${product.price}</p>
                        <button>Learn More</button>
                    `;
                    productList.appendChild(productDiv);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while analyzing the image.");
            });
        } else {
            alert("Please upload an image.");
        }
    });
});
