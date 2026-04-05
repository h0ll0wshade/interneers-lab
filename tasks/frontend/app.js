// Replace this URL with your actual Django API URL for getting products
const API_URL = "http://127.0.0.1:8000/proj/products/"; 

console.log("Starting API Call...");

// fetch() goes to the URL and asks for data
fetch(API_URL)
    .then(response => {
        // We have to tell the browser to read the response as JSON
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Here is the incoming data! Let's view it in the console.
        console.log("Successfully fetched products from Django:");
        console.log(data);
    })
    .catch(error => {
        console.error("Uh oh, the API call failed:", error);
    });