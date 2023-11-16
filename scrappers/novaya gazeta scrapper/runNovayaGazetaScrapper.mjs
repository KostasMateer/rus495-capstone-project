import { fetchAllNovayaGazetaData } from "./getNovayaGazetaArticles.mjs";

// fetchDataFromURL("мобилизация", "test.json")
const data = await fetchAllNovayaGazetaData("мобилизация", "novayagazetamobilizatsiya.json")
console.log('sweet')