/**
 * getNovayaGazetaArticles.mjs
 * 
 * This module provides functionality to fetch articles from Novaya Gazeta based on a given search term.
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
async function fetchAllNovayaGazetaData(searchTerm, filename) {
    let pageNumber = 0
    let apiURL = `https://novayagazeta.ru/api/v1/search?q=${searchTerm}&typeList=authors,records&page=${pageNumber}`
    let novayagazetaArticles = {
        'news site': 'novaya gazeta',
        'search term' : `${searchTerm}`,
        'total articles': 0,
        'articles' : []
    }
    try {
        // Fetch the initial data from the API
        const response = await fetch(apiURL);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let novayagazetaData = await response.json();
        
        let i = 1
        // Loop through all pages until no more articles are found

        // loop label, so can break once the year is past 2014
        outerLoop:
        while (true) {
            // Process articles on the current page
            const articleArray = novayagazetaData.records
            for (let index = 0; index < articleArray.length; index++) {
                const article = articleArray[index];
                const timestamp = article.date;
                const date = new Date(timestamp); // Convert timestamp to Date object
                if (date.getUTCFullYear() < 2014) break outerLoop
                const formattedDate = `${date.getUTCMonth() + 1}/${date.getUTCDate()}/${date.getUTCFullYear()}`; // Format the date
                const articleObject = {
                    [`article${i}`]: {
                        'title': article.title.replace(/<[^>]+>/g, ''),
                        'subtitle': article.subtitle,
                        'date': formattedDate,
                        'url': `https://novayagazeta.ru/articles/${article.slug}`
                    }
                }
                novayagazetaArticles.articles.push(articleObject);
                i++
            }        
            
            // Check if more pages exist
            if (!novayagazetaData.records.length) {
                break;
            }
            
            // Update the URL for the next page
            pageNumber++;
            apiURL = `https://novayagazeta.ru/api/v1/search?q=${searchTerm}&typeList=authors,records&page=${pageNumber}`
            
            // Fetch data for the next page
            const nextResponse = await fetch(apiURL);
            if (!nextResponse.ok) {
                throw new Error(`HTTP error! Status: ${nextResponse.status}`);
            }

            novayagazetaData = await nextResponse.json();
            console.log(`in progress... page ${pageNumber}`)
        }

        novayagazetaArticles['total articles'] = novayagazetaArticles['articles'].length

        // Save the collected articles to a file
        await saveJsonToFile(novayagazetaArticles, filename)
        return novayagazetaArticles
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
        await writeFile(filename+'novayagazeta.json', JSON.stringify(jsonObj, null, 4)); // The "4" argument is for indentation
        console.log(`Data saved to ${filename}`);
    } catch (error) {
        console.error('Error writing to file:', error);
    }
}

export {fetchAllNovayaGazetaData};