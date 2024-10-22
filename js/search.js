const url = new URL(window.location.href);
const searchParams = window.location.search;
const urlParams = new URLSearchParams(searchParams);

const query = urlParams.get('query');

function searchArticles(data, query, maxResults = 30) {
    // Convert query to lowercase for case-insensitive search
    const lowerQuery = query.toLowerCase();

    // Filter the dataset
    const results = data.filter(article => {
        // Check if the query is in the title, text, or summary
        return (
            article.title.toLowerCase().includes(lowerQuery) ||
            article.text.toLowerCase().includes(lowerQuery) ||
            article.summary.toLowerCase().includes(lowerQuery)
        );
    });

    // Return only the first `maxResults` articles
    return results.slice(0, maxResults);
}