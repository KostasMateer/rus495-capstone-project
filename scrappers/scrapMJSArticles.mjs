import { fetchAllTassData } from "./tass scrapper/getTassArticles.mjs";
import { fetchAllMeduzaData } from "./meduza scrapper/getMeduzaArticles.mjs";
import { fetchAllNovayaGazetaData } from "./novaya gazeta scrapper/getNovayaGazetaArticles.mjs";

let SEARCH_TERM = 'военная служба по контракту'
let FILE_NAME = `${SEARCH_TERM}`
// let meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'военная служба'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'воинская обязанность'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'война украина'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'контрактник'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'призывать'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'рекрут'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

SEARCH_TERM = 'специальная военная операция'
FILE_NAME = `${SEARCH_TERM}`
meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)

// const tassData = fetchAllTassData(SEARCH_TERM, FILE_NAME)
// meduzaData = fetchAllMeduzaData(SEARCH_TERM, FILE_NAME)
// const novayagazetaData = fetchAllNovayaGazetaData(SEARCH_TERM, FILE_NAME)
