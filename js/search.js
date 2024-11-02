(async function () {
    const url = new URL(window.location.href);
    const searchParams = window.location.search;
    const urlParams = new URLSearchParams(searchParams);

    const searchContainerA = document.querySelector('.search-results');
    const searchResultsContainer = document.querySelector('.res-container');
    const trendingContainerA = document.querySelector('.trending-articles');
    const trendingResultsContainer = document.querySelector('.trending-res');

    const searchInput = document.querySelector('.input-box');

    const query = urlParams.get('query');

    let data;

    if (query && query != '') {
        trendingContainerA.classList.add('display-none');
        await getData()
        setSearchResults(query);
    } else {
        searchContainerA.classList.add('display-none');
        showTrendingArticles();
    }

    async function showTrendingArticles() {

        const trendingData = await loadJSONFile('/data/trending.json');

        for (let i = 0; i < trendingData.length; i++) {
            trendingResultsContainer.appendChild(createCard(trendingData[i]))
            if (i == 0) {
                trendingResultsContainer.innerHTML = '';
                trendingResultsContainer.classList.add('display-grid');
            }
        }

        await getData();

    }

    async function getData() {
        data = await loadJSONFile('/data/all_articles.json');
    }

    async function setSearchResults(query) {
        //for checking if a query is present or not
        if (!query || query === '') {
            try {
                searchResultsContainer.classList.remove('display-grid');
            } catch { }
            searchResultsContainer.innerHTML = "<p>Search for any Keyword.</p>"
            return
        }

        //for setting loader again
        try {
            searchResultsContainer.classList.remove('display-grid');
        } catch { }

        if (!searchResultsContainer.querySelector('.loader-c-a')) {
            searchResultsContainer.innerHTML = `<div class="loader-c-a">
                        <div class="loader-a"></div>
                    </div>`
        }

        const lowerQuery = query.toLowerCase();

        let count = 0;
        for (let i = 0; i < data.length; i++) {
            if (
                data[i].title.toLowerCase().includes(lowerQuery) ||
                data[i].text.toLowerCase().includes(lowerQuery) ||
                data[i].summary.toLowerCase().includes(lowerQuery)
            ) {
                count += 1
                if (count == 1) {
                    searchResultsContainer.innerHTML = '';
                    searchResultsContainer.classList.add('display-grid');
                }
                searchResultsContainer.appendChild(createCard(data[i]))

                if (count >= 30) {
                    break
                }
            }
        }

        if (count == 0) {
            try {
                searchResultsContainer.classList.remove('display-grid');
            } catch { }
            searchResultsContainer.innerHTML = `<p>No Results found for ${query}.</p>`
        }
    }

    function createCard(data) {
        let div = document.createElement('div');
        div.classList.add('res');

        divAnchor = cleanString2(data['title']);

        // Create a Date object
        let dateObj = new Date(data['publish_date']);

        // Extract year, month, and day
        let year = dateObj.getFullYear();
        let month = dateObj.getMonth(); // Months are zero-indexed (0 = January, 1 = February, etc.)
        let day = dateObj.getDate();

        let imgSource = `/img/articles/${data['id']}.jpg`
        if (data['image'] == '/img/last24hrnews.webp' || data['image'].indexOf('ANI-News-Logo-96x96.jpg') !== -1) {
            imgSource = '/img/last24hrnews.webp'
        }
        div.innerHTML = `
                        <div class="res-img-c" style="background-image:url(${imgSource});">
                        </div>
                        <a href="/news/${year}/${month + 1}/${divAnchor}" class="res-details small-txt">
                            <h3 class="m-l-txt">
                                ${data['title']}
                            </h3>
                            <p>${data['text'].slice(0, 120)}</p>
                        </a>
                        `
        return div
    }

    async function loadJSONFile(path) {
        return fetch(path)
            .then((res) => res.json())
            .then((res) => { return res })
    }

    function cleanString2(str) {

        let cleanedStr = str.replace(/[^a-zA-Z0-9 ]/g, '');


        let result = cleanedStr.split(" ").join("-").toLowerCase();

        return result;
    }

    searchInput.addEventListener('keyup', () => {

        if (!trendingContainerA.classList.contains('display-none')) {
            trendingContainerA.classList.add('display-none');
        }

        if (searchContainerA.classList.contains('display-none')) {
            searchContainerA.classList.remove('display-none');
        }

        history.pushState(null, "", `/search/?query=${searchInput.value}`);

        setSearchResults(searchInput.value);

    })
})();
