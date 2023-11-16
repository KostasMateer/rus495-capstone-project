const fs = require('fs');
const https = require('https');

function fetchDataFromURL(url, outputFilename) {
    https.get(url, (response) => {
        let data = '';

        response.on('data', (chunk) => {
            data += chunk;
        });

        response.on('end', () => {
            // Parse the data as JSON and then stringify it.
            // This will convert the Unicode escaped sequences to actual characters.
            console.log(data)
            let parsedData = JSON.parse(data);
            let stringifiedData = JSON.stringify(parsedData, null, 2);  // Beautify the JSON with 2-space indentation

            fs.writeFile(outputFilename, stringifiedData, 'utf8', (err) => {
                if (err) {
                    console.error("Error writing to file:", err);
                } else {
                    console.log(`Data saved to ${outputFilename}`);
                }
            });
        });

    }).on('error', (error) => {
        console.error("Error fetching the data:", error);
    });
}


let outputFile = 'responsenovaya.json';
// Example usage
let apiEndpoint = "https://novayagazeta.ru/api/v1/search?q=%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F"; // Replace with your actual API endpoint
fetchDataFromURL(apiEndpoint, outputFile);

apiEndpoint = "https://tass.ru/tbp/api/v1/search?search=%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F&lang=ru&offset=0&limit=20"
outputFile = 'responsetass.json'
fetchDataFromURL(apiEndpoint, outputFile);

apiEndpoint = "https://meduza.io/api/w5/search?term=%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F&page=15&per_page=1000&locale=ru"
outputFile = 'responsemeduza.json'
fetchDataFromURL(apiEndpoint, outputFile)
