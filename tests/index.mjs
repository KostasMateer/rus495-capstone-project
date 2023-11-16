import fetch from 'node-fetch';
import { fetchAndParseData } from './getPervyiKanalArticles.mjs';


const url = "https://www.1tv.ru/search.js?limit=5&offset=100&q=text%3A%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F"

const test = fetchAndParseData(url)
console.log('nice')