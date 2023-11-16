function searchArticles(keyword, start=1) {
    var apiKey = 'AIzaSyAoDnvSPEeywzGy4VWm6aw5sh0LA4oZej0';
    var searchEngineId = 'a0d52d4cc41014081';
    var currentYear = new Date().getFullYear();
    var yearsSince2014 = currentYear - 2014;

    var url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=site:meduza.io ${keyword}&start=${start}&dateRestrict=y${yearsSince2014}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Search Results:', data);

            // Calculate total number of pages (assuming 10 results per page)
            const totalResults = parseInt(data.searchInformation.totalResults, 10);
            const totalPages = Math.ceil(totalResults / 10);
            console.log(`Total results: ${totalResults}, Total pages: ${totalPages}`);

            // Recursively fetch next page
            if (data.queries.nextPage) {
                searchArticles(keyword, data.queries.nextPage[0].startIndex);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Example usage
searchArticles('мобилизация');