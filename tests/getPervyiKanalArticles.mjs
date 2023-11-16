import fetch from 'node-fetch';
import { JSDOM } from 'jsdom';

async function fetchAndParseData(url) {
  try {
    // Fetch the data
    const response = await fetch(url);
    const htmlString = await response.text();

    // Create a new DOMParser instance
   // Parse the HTML string into a DOM Document using jsdom
   const dom = new JSDOM(htmlString);
   const doc = dom.window.document;
 
   // Select all .result elements
   const articleElements = doc.querySelectorAll('.result');
 
   // Map over each article element and extract the relevant data
   const articles = Array.from(articleElements).map(article => {
     const title = article.querySelector('.show-name')?.textContent.trim() || '';
     const date = article.querySelector('.date')?.textContent.trim() || '';
     const lead = article.querySelector('.lead')?.textContent.trim() || '';
     const link = article.getAttribute('href') || '';
 
     return { title, date, lead, link };
   });
 
   return articles;

 // Use the function to extract the articles
 
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// Use this function with your URL
export {fetchAndParseData}