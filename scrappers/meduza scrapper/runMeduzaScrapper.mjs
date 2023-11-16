import { fetchAllMeduzaData } from "./getMeduzaArticles.mjs";

// fetchDataFromURL("мобилизация", "test.json")
const data = await fetchAllMeduzaData("мобилизация", " meduzamobilizatsiya.json")
console.log('sweet')