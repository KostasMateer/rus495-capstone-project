import { fetchAllTassData } from "./getTassArticles.mjs";

// fetchDataFromURL("мобилизация", "test.json")
const data = await fetchAllTassData("мобилизация", "tassmobilizatsiya.json")
console.log('sweet')