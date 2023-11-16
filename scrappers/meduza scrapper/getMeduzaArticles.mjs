/**
 * getMeduzaArticles.mjs
 * 
 * This module provides functionality to fetch articles from Meduza based on a given search term.
 * It retrieves articles from multiple pages and saves them to a specified JSON file. The main functions
 * in this module include fetchAllData (which fetches articles) and saveJsonToFile (which saves the articles to a file).
 * 
 * Author: Kostas Mateer
 * Date: October 28, 2023
 * RUS 495 Capstone - Dr. Ewington
 */
import fetch from 'node-fetch';
import { writeFile } from 'fs/promises';


/**
 * Fetches articles from Meduza based on a search term and saves them to a specified file.
 * 
 * @param {string} searchTerm - The term to search for in articles.
 * @param {string} filename - The name of the file where the articles should be saved.
 * @returns {Object} An object containing the fetched articles.
 */
async function fetchAllMeduzaData(searchTerm, filename) {
    let pageNumber = 0
    let apiURL = `https://meduza.io/api/w5/search?term=${searchTerm}&page=${pageNumber}&per_page=100&locale=ru`
    let meduzaArticles = {
        'news site': 'meduza',
        'search term' : `${searchTerm}`,
        'total articles' : 0,
        articles : []
    }
    try {
        // Fetch the initial data from the API
        const response = await fetch(apiURL);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let meduzaData = await response.json();
        let i = 1
        
        // Loop through all pages until no more articles are 
        outerLoop: // loop label to break out if articles are older than 2014
        while (true) {
            // Process articles on the current page
            Object.entries(meduzaData.documents).forEach(([key, value]) => {
                const timestamp = value.datetime;
                const date = new Date(timestamp * 1000); // Convert timestamp to Date object
                const formattedDate = `${date.getUTCMonth() + 1}/${date.getUTCDate()}/${date.getUTCFullYear()}`; // Format the date
                const articleObject = {
                    [`article${i}`]: {
                        'title': value.title,
                        'date': formattedDate,
                        'url': `https://meduza.io/${value.url}`
                    }
                }
                meduzaArticles.articles.push(articleObject);
                i++;
            });
            
            // Check if more pages exist
            if (!meduzaData.has_next) {
                break;
            }
            
            // Update the URL for the next page
            pageNumber++;
            apiURL = `https://meduza.io/api/w5/search?term=${searchTerm}&page=${pageNumber}&per_page=100&locale=ru`;
            
            // Fetch data for the next page
            const nextResponse = await fetch(apiURL);
            if (!nextResponse.ok) {
                throw new Error(`HTTP error! Status: ${nextResponse.status}`);
            }
            meduzaData = await nextResponse.json();
            console.log(`in progress... page ${pageNumber}`)
        }

        meduzaArticles['total articles'] = meduzaArticles['articles'].length

        // Save the collected articles to a file
        await saveJsonToFile(meduzaArticles, filename)
        return meduzaArticles
    } catch (error) {
        console.error("Failed to fetch the data:", error);
    }
}


/**
 * Saves a JSON object to a specified file.
 * 
 * @param {Object} jsonObj - The JSON object to be saved.
 * @param {string} filename - The name of the file where the JSON object should be saved.
 */
async function saveJsonToFile(jsonObj, filename) {
    try {
        // Convert the JSON object to a formatted string and write it to the file
        await writeFile(filename+'meduza.json', JSON.stringify(jsonObj, null, 4)); // The "4" argument is for indentation
        console.log(`Data saved to ${filename}`);
    } catch (error) {
        console.error('Error writing to file:', error);
    }
}

export {fetchAllMeduzaData};