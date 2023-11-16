/**
 * getTassArticles.mjs
 * 
 * This module provides functionality to fetch articles from Tass based on a given search term.
 * It retrieves articles from multiple pages and saves them to a specified JSON file. The main functions
 * in this module include fetchAllData (which fetches articles) and saveJsonToFile (which saves the articles to a file).
 * 
 * Author: Kostas Mateer
 * Date: October 29, 2023
 * RUS 495 Capstone - Dr. Ewington
 */
import fetch from 'node-fetch';
import { writeFile } from 'fs/promises';


// Constants used by the fetcher module
const MAX_CONCURRENT_REQUESTS = 1000;
const MAX_RETRIES = 5;
const RETRY_DELAY = 5000; // 5 seconds
const BATCH_DELAY = 100; // 0.1 second
const MAX_CONSECUTIVE_FAILURES = 20; // Number of allowed consecutive empty pages before stopping

let consecutiveFailures = 0; // Counter for consecutive empty pages

/**
 * Delays the execution of the next line of code.
 * 
 * @param {number} ms - The number of milliseconds to delay.
 * @returns {Promise} A promise that resolves after the specified delay.
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Fetches data from a URL with retry logic.
 * It will attempt to fetch data up to a maximum number of retries.
 * If it continues to fail, it will return an empty result after reaching the max consecutive failures limit.
 * 
 * @param {string} url - The URL to fetch data from.
 * @param {number} retries - The number of times to retry the fetch on failure.
 * @returns {Promise<Object>} A promise that resolves to the fetched data or an empty result.
 */
async function fetchWithRetry(url, retries = MAX_RETRIES) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.text();
        const PATTERN = /<a class="result" href="(.*?)"[^]*?<div class="show-name[^]*?">(.*?)<\/div><div class="date">(.*?)<\/div><div class="lead">(.*?)<\/div>/gs;
        let matches;
        let results = [];

        while ((matches = PATTERN.exec(data)) !== null) {
            let [_, url, title, date, lead] = matches;
            let full_url = "https://www.1tv.ru" + url;
            const result = {
                url: matches[1],
                imageSrc: matches[2],
                showName: matches[3],
                date: matches[4],
                lead: matches[5]
            };
            results.push(result);
        }
        if (!matches || matches.length === 0) {
            consecutiveFailures++
            throw new Error('No results returned from API.');
        }
        consecutiveFailures = 0; // Reset on successful fetch
        return data;
    } catch (error) {
        console.log(`Error fetching data: ${error.message}`);
        if (retries > 0 && consecutiveFailures < MAX_CONSECUTIVE_FAILURES) {
            console.log(`Retrying... Attempts left: ${retries}`);
            await delay(RETRY_DELAY + Math.random() * 1000); // Adding jitter
            return fetchWithRetry(url, retries - 1);
        } 
        else {
            console.log(`No more retries left for the URL: ${url}, or max consecutive failures reached.`);
            return {result: []}; // or throw the error, depending on how you want to handle this
        } 
    }
}

/**
 * Fetches pages of data in parallel from the Tass API based on a search term.
 * If empty results are returned consecutively more than the allowed threshold, the fetching stops.
 * 
 * @param {string} searchTerm - The term to search for in articles.
 * @returns {Promise<Array>} A promise that resolves to an array of fetched articles.
 */
async function fetchPagesInParallel(searchTerm) {
    let pageNumber = 0;
    const allResults = new Map();
    while (true) {
        const promises = [];
        for (let i = pageNumber; i < pageNumber + MAX_CONCURRENT_REQUESTS; i++) {
            const url = `https://www.1tv.ru/search.js?limit=100&offset=${pageNumber}&q=text%3A${searchTerm}`;
            await delay(100)
            promises.push(fetchWithRetry(url))
        }

        const results = await Promise.all(promises);

        // Store the results
        for (let eachPage of results) {
            eachPage.result.forEach(article => {
                if (!allResults.has(article.id)) {
                    allResults.set(article.id, article);
                }
            });
        }

        if (results.some(result => result.result.length === 0)) {  
            break;
        }

        pageNumber += MAX_CONCURRENT_REQUESTS;

        console.log(`Fetched up to offset: ${pageNumber}`);
        await delay(BATCH_DELAY); // Add a delay here before fetching the next batch of pages
    }

    return Array.from(allResults.values()).sort();
}

/**
 * Fetches articles from Tass based on a search term and saves them to a specified file.
 * 
 * @param {string} searchTerm - The term to search for in articles.
 * @param {string} filename - The name of the file where the articles should be saved.
 * @returns {Object} An object containing the fetched articles.
 */
async function fetchAllPervyiKanalData(searchTerm, filename) {
    let pervyiKanalArticles = {
        'news site': 'pervyi kanal',
        'search term' : `${searchTerm}`,
        'articles' : []
    }

    try {
        // Fetch the initial data from the API
        let results = await fetchPagesInParallel(searchTerm)
        // Loop through all pages until no more articles are found
        // Process all articles

        // loop label to break once past 2014
        outerLoop:
        for (let index = 0; index < results.length; index++) {
            const article = results[index];
            const timestamp = article.published_dt;
            const date = new Date(timestamp); // Convert timestamp to Date object
            if (date.getUTCFullYear() < 2014) break outerLoop
            const formattedDate = `${date.getUTCMonth() + 1}/${date.getUTCDate()}/${date.getUTCFullYear()}`; // Format the date
            const articleObject = {
                [`article${index}`]: {
                    'title': article.title,
                    'subtitle': article.subtitle,
                    'date': formattedDate,
                    'url': `"https://www.1tv.ru"${article.url}`
                }
            }
            tassArticles.articles.push(articleObject);
            console.log(`article ${index} upload complete`)
        }

        // Save the collected articles to a file
        await saveJsonToFile(tassArticles, filename)
        return tassArticles
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
        await writeFile(filename+'tass.json', JSON.stringify(jsonObj, null, 2)); // The "4" argument is for indentation
        console.log(`Data saved to ${filename}`);
    } catch (error) {
        console.error('Error writing to file:', error);
    }
}

export {fetchAllPervyiKanalData};