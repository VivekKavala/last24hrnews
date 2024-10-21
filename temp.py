# importing required libraries
import requests
import re
import json
from datetime import datetime
from PIL import Image
from io import BytesIO
import os
import time

start_time = time.time()

def setApiKey():
    apiKeys = [
        '990022febd8941e99194654a6fb37e9f',
        '94e362f65b7444d7bc782f89bfdf06bb'
    ]

    return apiKeys[int(input('Which Key you wanna use 1 or 2 : ')) - 1]

def getFormattedDates(date):
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


    return date.strftime("%B %d, %Y"), date.strftime('%Y-%m-%d'), date.strftime('%d-%m-%Y'), date.isoformat()

def getJsonFileData(location):
    with open(location, 'r', encoding='utf-8') as file:
        return json.load(file)

def saveHTMLFile(location, content):
    try:
        if not os.path.exists(location):
            os.makedirs(location, exist_ok=True)

        with open(location + r'index.html', 'w', encoding='utf-8') as file:
            file.write(content)

        print(f'File saved at {location}')

    except:
        print(f"Some error occured while saving the file at {location}")
def saveJSONFile(location, content):
    try:
        with open(location, 'w') as f:
            json.dump(content, f, indent=4)
    except:
        print(f"Some error occured while saving the file at {location}")

def getMaxAuthor(news):

    authors = {}

    for i in news:
        if 'authors' in i:
            for j in i['authors']:
                if j in authors:
                    authors[j] += 1
                else:
                    authors[j] = 1

    max_key = max(authors, key=authors.get)
    return max_key

def getArticleAnchor(date, title):
    date = date.split('-')
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    return '/news/' + date[0] + '/' + date[1] + '/' + title.replace(' ', '-') + '/'

def createArticlePage(articleData):
    articlePublishDate = articleData['publish_date']
    formattedDates = getFormattedDates(articlePublishDate)

    articleTitle = articleData['title']
    articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)
    if os.path.exists(mainlocation + articleAnchor):
        return

    articleCategory = ''
    if 'category' in articleData and articleData['category'] in categories:
        articleCategory = articleData['category']
    
    articleImage = '/img/last24hrnews.webp'
    if articleData['image'] != articleImage and 'ANI-News-Logo-96x96' not in articleData['image']:
        fileLocation = f"C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews/img/articles/{articleData['id']}.jpg"
        if not os.path.exists(fileLocation):
            try :
                # Send a GET request to the URL
                response = requests.get(articleData['image'])

                # Open the image from the response content
                img = Image.open(BytesIO(response.content))

                # Convert the image to RGB mode if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Save the image locally
                img.save(f"C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews/img/articles/{articleData['id']}.jpg")
            except:
                pass
        
        articleImage = f"/img/articles/{articleData['id']}.jpg"

    

    relatedArticlesHtml = ''

    #for related articles
    if articleCategory != '':
        relatedArticlesHtml += """
                        <h2 class="m-l-txt">Related Articles</h2>
                        <div class="articles">
                                """
        relatedArticleData = categoriesData[articleCategory]
        maxI = 3 if len(relatedArticleData) >= 3 else len(relatedArticleData)
        for i in range(0, maxI):

            if relatedArticleData[i]['id'] == articleData['id']:
                maxI += 1
                continue

            if relatedArticleData[i]['id'] not in addedArticlesIds:
                addedArticlesIds.append(relatedArticleData[i]['id'])
                createArticlePage(relatedArticleData[i])
            articlePublishDate1 = relatedArticleData[i]['publish_date']
            formattedDates1 = getFormattedDates(articlePublishDate1)
            
            articleImage1 = '/img/last24hrnews.webp'
            if relatedArticleData[i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in relatedArticleData[i]['image']:
                articleImage1 = f"/img/articles/{relatedArticleData[i]['id']}.jpg"

            articleTitle1 = relatedArticleData[i]['title']
            articleAnchor1 = getArticleAnchor(formattedDates1[1], articleTitle1)

            paragraphsList = relatedArticleData[i]['text'].split('.')

            paragraphHtml = ''

            maxIn = 2 if len(paragraphsList) >= 2 else len(paragraphsList)

            for i in range(0,maxIn):

                paragraphHtml += f"""
                                <p class="m-b-5 small-txt">{paragraphsList[i]}.</p>
                                """

            relatedArticlesHtml += f"""
                            <div class="article">
                                <p class="small-txt">
                                    <i class="fa fa-chevron-right t-txt"></i>
                                    {articleCategory}
                                </p>
                                <h3 class="m-txt">
                                    <a href="{articleAnchor1}">
                                        {articleTitle1}
                                    </a>
                                </h3>
                                <p class="t-txt">{formattedDates1[0]}</p>
                                <div class="img-container">
                                    <img src="{articleImage1}" alt="{articleTitle1}">
                                </div>
                                {paragraphHtml}
                                <a class="small-txt" href="{articleAnchor1}">read more</a>
                            </div>
                                """
    relatedArticlesHtml += '</div>'
    articleParagraphList = articleData['text'].split('.')

    articleParaHtml = ''

    for para in articleParagraphList:
        articleParaHtml += f"""
                            <p class='m-b-5 small-txt'>{para}.</p>
                            """

    articleHtml = f"""
<!DOCTYPE html>
<html lang="en">

<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5707347915371687"
        crossorigin="anonymous"></script>
    <meta charset="utf-8">
    <title>{articleTitle} | Last24hrnews</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
    <meta content="news, last24hrnews, latest news, trending news" name="keywords">
    <meta
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates."
        name="description">
    <meta property="og:type" content="website" />

    <link rel="apple-touch-icon" sizes="180x180" href="/img/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="/img/favicon_io/site.webmanifest">

    <meta property="og:url" content="https://last24hrnews.com{articleAnchor}" />
    <meta property="article:modified_time" content="{formattedDates[3]}">
    <meta property="og:title" content="Breaking News, Every Hour – Stay Informed with Last24HRNews!" />
    <meta property="og:image" content="/img/last24hrnews.webp" />
    <meta property="og:image:width" content="650">
    <meta property="og:image:height" content="350">
    <meta property="og:description"
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates." />
    <link rel="canonical" href="https://last24hrnews.com{articleAnchor}">

    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css" rel="stylesheet">


    <link href="/css/style.css" rel="stylesheet">
    <link rel="stylesheet" href="/css/article.css">
</head>

<body>
    <!-- Navbar Start -->
    <header class="container-fluid p-0 mb-3">
        <nav class="navbar navbar-expand-lg bg-light navbar-light py-2 py-lg-0 px-lg-5">
            <a href="/" class="navbar-brand d-lg-block">
                <img src="/img/logo.png" class="logo" />
            </a>
            <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-between px-0 px-lg-3" id="navbarCollapse">
                <div class="navbar-nav mr-auto py-0">
                    <a href="/" class="nav-item nav-link">Home</a>
                    <a href="/search" class="nav-item nav-link">Search News</a>
                    <div class="nav-item dropdown">
                        <a href="" class="nav-link dropdown-toggle" data-toggle="dropdown">Categories</a>
                        <div class="dropdown-menu rounded-0 m-0">
                            <a href="/categories/politics/" class="dropdown-item mb-1">Politics</a>
                            <a href="/categories/technology/" class="dropdown-item mb-1">Technology</a>
                            <a href="/categories/sports/" class="dropdown-item mb-1">Sports</a>
                            <a href="/categories/business/" class="dropdown-item mb-1">Business</a>
                            <a href="/categories/" class="dropdown-item mb-1">View More</a>
                        </div>
                    </div>
                    <a href="/contact/" class="nav-item nav-link">Contact</a>
                </div>
                <div class="input-group ml-auto" style="width: 100%; max-width: 300px;">
                    <input type="text" class="form-control" placeholder="Keyword">
                    <div class="input-group-append">
                        <button class="input-group-text text-secondary"><i class="fa fa-search"></i></button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
    <!-- Navbar End -->

    <!-- Breadcrumb Start -->
    <div class="container-fluid">
        <div class="container small-txt">
            <nav class="breadcrumb bg-transparent m-0 p-0">
                <a class="breadcrumb-item" href="/">Home</a>
                <a class="breadcrumb-item" href="/categories/">Category</a>
                <a class="breadcrumb-item" href="/categories/{articleCategory}/">{articleCategory}</a>
                <span class="breadcrumb-item active">{articleTitle}</span>
            </nav>
        </div>
    </div>
    <!-- Breadcrumb End -->


    <!-- News With Sidebar Start -->
    <div class="container-fluid py-3">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <!-- News Detail Start -->
                    <div class="position-relative mb-3">
                        <img class="img-fluid w-100"
                            src="{articleImage}"
                            style="object-fit: cover;">
                        <div class="overlay position-relative bg-light">
                            <div class="mb-3 small-txt">
                                <a href="/categories/{articleCategory}">{articleCategory}</a>
                                <span class="px-1">/</span>
                                <span>{formattedDates[0]}</span>
                            </div>
                            <div>
                                <h1 class="mb-3 x-l-txt">{articleTitle}
                                </h1>

                                {articleParaHtml}
                            
                            </div>
                        </div>
                    </div>
                    <!-- News Detail End -->
                    <div>




                        <!-- COMMENTS SHAREBAR: Place it where you want SHARES to be displayed -->
                        <div class="vuukle-sharebar"></div>





                        <!-- EMOTES WRAPPER: Place it where you want emotes to be displayed -->
                        <div id="vuukle-emote"></div>





                        <!-- COMMENTS WRAPPER: Place it where you want comments to be displayed -->
                        <div id="vuukle-comments"></div>


                        <script type="text/javascript">

                            var VUUKLE_CONFIG = {{
                                "apiKey": "e831e786-825c-4472-b4eb-f74e501ee03c",
                                "host": "last24hrnews.com",
                                "articleId": "{articleAnchor}",
                                "img": "{articleImage}",
                                "tags": "{articleCategory}",
                                "url": "https://last24hrnews.com/{articleAnchor}",
                                "title": "{articleTitle}",
                                "author": "Vivek",
                                "language": "en",
                                "recommendedArticles": false,
                                "globalRecommendations": false,
                                "wideImages": true,
                                "comments": {{
                                    "enabled": true,
                                    "editorOptions": [
                                        "bold",
                                        "italic",
                                        "underline",
                                        "url",
                                        "blockquote",
                                        "code",
                                        "list",
                                        "image",
                                        "gif"
                                    ],
                                    "transliteration": {{
                                        "language": "en",
                                        "enabledByDefault": false
                                    }},
                                    "commentingClosed": false,
                                    "countToLoad": 5
                                }},
                                "emotes": {{
                                    "enabled": true,
                                    "disable": [
                                        5,
                                        6
                                    ]
                                }},
                                "sharebar": {{
                                    "enabled": true,
                                    "verticalPosition": "10px",
                                    "mode": "horizontal"
                                }}
                            }};

                            (function () {{
                                var d = document,
                                    s = d.createElement('script');

                                s.src = 'https://cdn.vuukle.com/platform.js';
                                (d.head || d.body).appendChild(s);
                            }})();
                        </script>

                    </div>

                    <div class="related-articles m-b-20">
                        
                            {relatedArticlesHtml}
                    </div>

                </div>

                <div class="col-lg-4 pt-3 pt-lg-0">
                    <!-- Ads Start -->
                    <!-- <div class="mb-3 pb-3">
                        <a href=""><img class="/img-fluid" src="/img/news-500x280-4.jpg" alt=""></a>
                    </div> -->
                    <!-- Ads End -->

                    <!-- Popular News Start -->
                    <div class="pb-3 trending-container">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Trending</h3>
                        </div>
                        <div class="loader-container trending-loader">

                            <div class="loader">

                            </div>
                        </div>
                    </div>
                    <!-- Popular News End -->

                    <!-- Tags Start -->
                    <div class="pb-3">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Tags</h3>
                        </div>
                        <div class="d-flex flex-wrap m-n1">
                            <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                            <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                            <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                            <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                            <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                            <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                            <a href="/categories/technology/"
                                class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                            <a href="/categories/entertainment/"
                                class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                            <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                            <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                        </div>
                    </div>
                    <!-- Tags End -->
                </div>
            </div>
        </div>
    </div>
    </div>
    <!-- News With Sidebar End -->


    <!-- Footer Start -->
    <footer class="container-fluid bg-light pt-5 px-sm-3 px-md-5">
        <div class="row align-items-center">
            <div class="col-lg-3 col-md-6 mb-5">
                <a href="/" class="navbar-brand">
                    <img src="/img/logo.png" class="logo" alt="">
                </a>
                <p>Breaking News, Every Hour – Stay Informed with Last24HRNews!</p>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Categories</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Tags</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Quick Links</h4>
                <div class="d-flex flex-column justify-content-start">
                    <a class="text-secondary mb-2" href="/about/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>About</a>
                    <a class="text-secondary mb-2" href="/advertise/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Advertise</a>
                    <a class="text-secondary mb-2" href="/privacy-policy/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Privacy &
                        policy</a>
                    <a class="text-secondary mb-2" href="/terms/"><i class="fa fa-angle-right text-dark mr-2"></i>Terms
                        &
                        conditions</a>
                    <a class="text-secondary" href="/contact/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Contact</a>
                </div>
            </div>
        </div>
    </footer>
    <div class="container-fluid py-4 px-sm-3 px-md-5">
        <p class="m-0 text-center">
            &copy;
            <span id="presentYear">
                <script>
                    document.querySelector("#presentYear").innerText = new Date().getFullYear()
                </script>
            </span>
            <a class="font-weight-bold" href="/">Last24hrnews.com</a>. All Rights Reserved.
        </p>
    </div>
    <!-- Footer End -->


    <!-- Back to Top -->
    <a href="#" class="btn btn-dark back-to-top"><i class="fa fa-angle-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>

    <!-- Template Javascript -->
    <script src="/js/main.js"></script>
</body>

</html>
                    """

    if not os.path.exists(mainlocation +  articleAnchor):
        os.makedirs(mainlocation + articleAnchor, exist_ok=True)
    
    with open(mainlocation + articleAnchor + r'index.html', 'w', encoding='utf-8') as file:
        file.write(articleHtml)
    
    print('Article Created Succesfully at ', mainlocation + articleAnchor)

def createCategoryPage(categoryData):

    presentCategory = categoryData[0]['category']

    maxPages = len(categoryData) // 14 + 1
    if len(categoryData) % 14 == 0:
        maxPages -= 1 
    
    print(maxPages)

    def saveCategoryPage(htmlContent, activePage=1):
        print(activePage)

        paginationHtml = ''
        if maxPages > 1:

            #setting prev button
            if activePage > 1:
                prevPageNumber = activePage - 1
                if prevPageNumber  == 1:
                    paginationHtml += f'''<li class="page-item">
                                        <a class="page-link" href="/categories/{presentCategory}" aria-label="Previous">
                                            <span class="fa fa-angle-double-left" aria-hidden="true"></span>
                                            <span class="sr-only">Previous</span>
                                        </a>
                                    </li>'''
                else:
                    paginationHtml += f'''<li class="page-item">
                                        <a class="page-link" href="/categories/{presentCategory}/{prevPageNumber}" aria-label="Previous">
                                            <span class="fa fa-angle-double-left" aria-hidden="true"></span>
                                            <span class="sr-only">Previous</span>
                                        </a>
                                    </li><li class="page-item"><a class="page-link" href="/categories/{presentCategory}/">1</a></li>'''

            if maxPages <= 5:
                minI = 2
                if activePage == 1:
                    minI = 1
                for pageNumber in range(minI, maxPages + 1):
                    if pageNumber != activePage:
                        paginationHtml += f"""<li class="page-item"><a class="page-link" href="/categories/{presentCategory}/{pageNumber}">{pageNumber}</a></li>"""
                    else:
                        paginationHtml += f"""<li class="page-item active"><a class="page-link" href>{pageNumber}</a></li>"""

            else:

                if activePage == 1:

                    paginationHtml += f'<li class="page-item active"><a class="page-link" href="">1</a></li>'
                    paginationHtml += f'<li class="page-item"><a class="page-link" href="/categories/{presentCategory}/2">2</a></li>'

                if activePage > 2:

                    paginationHtml += f'<li class="page-item"><a class="page-link" href="#">...</a></li>'


                if activePage == maxPages:

                    paginationHtml += f'<li class="page-item"><a class="page-link" href="/categories/{presentCategory}/{activePage - 1}">{activePage - 1}</a></li>'
                    paginationHtml += f'<li class="page-item active"><a class="page-link" href="">{activePage}</a></li>'

                if activePage >= 2 and activePage + 1 <= maxPages:


                    paginationHtml += f'<li class="page-item"><a class="page-link" href="/categories/{presentCategory}/{activePage - 1}">{activePage - 1}</a></li>'
                    paginationHtml += f'<li class="page-item active"><a class="page-link" href="">{activePage}</a></li>'
                    paginationHtml += f'<li class="page-item"><a class="page-link" href="/categories/{presentCategory}/{activePage + 1}">{activePage + 1}</a></li>'


                if activePage + 2 <= maxPages:

                    paginationHtml += f'<li class="page-item"><a class="page-link" href="">..</a></li>'

            #setting next button
            if activePage < maxPages:
                paginationHtml += f'''<li class="page-item">
                                        <a class="page-link" href="/categories/{presentCategory}/{activePage + 1}" aria-label="Next">
                                            <span class="fa fa-angle-double-right" aria-hidden="true"></span>
                                            <span class="sr-only">Next</span>
                                        </a>
                                    </li>'''

        categoryHtmlContent = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5707347915371687"
        crossorigin="anonymous"></script>
        <meta charset="utf-8">
        <title>{presentCategory.capitalize()} | Last24hrnews</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
        <meta
            content="news, last24hrnews, latest news, trending news, politics, education, sports, entertainment, lifestyle, business, science, technology, travel"
            name="keywords">
        <meta
            content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates."
            name="description">
        <meta property="og:type" content="website" />

        <link rel="apple-touch-icon" sizes="180x180" href="/img/favicon_io/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon_io/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon_io/favicon-16x16.png">
        <link rel="manifest" href="/img/favicon_io/site.webmanifest">

        <meta property="og:url" content="https://last24hrnews.com/categories/{presentCategory}/" />
        <meta property="article:modified_time" content="{presentFormattedDates[-1]}">
        <meta property="og:title" content="Categories | last24hrnews" />
        <meta property="og:image" content="/img/last24hrnews.png" />
        <meta property="og:image:width" content="650">
        <meta property="og:image:height" content="350">
        <meta property="og:description"
            content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates." />
        <link rel="canonical" href="https://last24hrnews.com/categories/{presentCategory}/">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css" rel="stylesheet">

        <link href="/lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">

        <link href="/css/style.css" rel="stylesheet">
    </head>

    <body>
        <!-- Topbar Start -->
        <header class="container-fluid p-0 mb-3">
            <nav class="navbar navbar-expand-lg bg-light navbar-light py-2 py-lg-0 px-lg-5">
                <a href="/" class="navbar-brand d-lg-block">
                    <img src="/img/logo.png" class="logo" />
                </a>
                <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-between px-0 px-lg-3" id="navbarCollapse">
                    <div class="navbar-nav mr-auto py-0">
                        <a href="/" class="nav-item nav-link">Home</a>
                        <a href="/search" class="nav-item nav-link">Search News</a>
                        <!-- <a href="" class="nav-item nav-link">Politics</a> -->
                        <div class="nav-item dropdown">
                            <a href="" class="nav-link dropdown-toggle" data-toggle="dropdown">Categories</a>
                            <div class="dropdown-menu rounded-0 m-0">
                                <a href="/categories/politics/" class="dropdown-item mb-1">Politics</a>
                                <a href="/categories/technology/" class="dropdown-item mb-1">Technology</a>
                                <a href="/categories/sports/" class="dropdown-item mb-1">Sports</a>
                                <a href="/categories/business/" class="dropdown-item mb-1">Business</a>
                                <a href="/categories/" class="dropdown-item mb-1">View More</a>
                            </div>
                        </div>
                        <a href="/contact/" class="nav-item nav-link">Contact</a>
                    </div>
                    <div class="input-group ml-auto" style="width: 100%; max-width: 300px;">
                        <input type="text" class="form-control" placeholder="Keyword">
                        <div class="input-group-append">
                            <button class="input-group-text text-secondary"><i class="fa fa-search"></i></button>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
        <!-- Topbar End -->

        <!-- Breadcrumb Start -->
        <div class="container-fluid">
            <div class="container small-txt">
                <nav class="breadcrumb bg-transparent m-0 p-0">
                    <a class="breadcrumb-item" href="/">Home</a>
                    <a class="breadcrumb-item" href="/categories/">Category</a>
                    <span class="breadcrumb-item active">{presentCategory}</span>
                </nav>
            </div>
        </div>
        <!-- Breadcrumb End -->


        <!-- News With Sidebar Start -->
        <div class="container-fluid py-3 categories-container">
            <div class="container">
                <div class="row">
                    <div class="col-lg-8">
                        
                        {htmlContent}
                        </div>
                        <!-- pagination -->
                        <div class="row">
                        <div class="col-12">
                            <nav aria-label="Page navigation">
                                <ul class="pagination justify-content-center">
                                    {paginationHtml}
                                </ul>
                            </nav>
                        </div>
                        </div>
                    </div>

                    <div class="col-lg-4 pt-3 pt-lg-0">

                        <!-- Popular News Start -->
                        <div class="pb-3">
                            <div class="bg-light py-2 px-4 mb-3">
                                <h3 class="m-0">Trending</h3>
                            </div>
                            <div class="d-flex mb-3">
                                <img src="/img/news-100x100-1.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="">Technology</a>
                                        <span class="px-1">/</span>
                                        <span>January 01, 2045</span>
                                    </div>
                                    <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                                </div>
                            </div>
                            <div class="d-flex mb-3">
                                <img src="/img/news-100x100-2.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="">Technology</a>
                                        <span class="px-1">/</span>
                                        <span>January 01, 2045</span>
                                    </div>
                                    <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                                </div>
                            </div>
                            <div class="d-flex mb-3">
                                <img src="/img/news-100x100-3.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="">Technology</a>
                                        <span class="px-1">/</span>
                                        <span>January 01, 2045</span>
                                    </div>
                                    <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                                </div>
                            </div>
                            <div class="d-flex mb-3">
                                <img src="/img/news-100x100-4.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="">Technology</a>
                                        <span class="px-1">/</span>
                                        <span>January 01, 2045</span>
                                    </div>
                                    <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                                </div>
                            </div>
                            <div class="d-flex mb-3">
                                <img src="/img/news-100x100-5.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="">Technology</a>
                                        <span class="px-1">/</span>
                                        <span>January 01, 2045</span>
                                    </div>
                                    <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                                </div>
                            </div>
                        </div>
                        <!-- Popular News End -->

                        <!-- Tags Start -->
                        <div class="pb-3">
                            <div class="bg-light py-2 px-4 mb-3">
                                <h3 class="m-0">Tags</h3>
                            </div>
                            <div class="d-flex flex-wrap m-n1">
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                                <a href="" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                            </div>
                        </div>
                        <!-- Tags End -->
                    </div>
                </div>
            </div>
        </div>
        </div>
        <!-- News With Sidebar End -->


        <!-- Footer Start -->
        <footer class="container-fluid bg-light pt-5 px-sm-3 px-md-5">
            <div class="row align-items-center">
                <div class="col-lg-3 col-md-6 mb-5">
                    <a href="/" class="navbar-brand">
                        <img src="/img/logo.png" class="logo" alt="">
                    </a>
                    <p>Breaking News, Every Hour – Stay Informed with Last24HRNews!</p>
                </div>
                <div class="col-lg-3 col-md-6 mb-5">
                    <h4 class="font-weight-bold mb-4">Categories</h4>
                    <div class="d-flex flex-wrap m-n1">
                        <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                        <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                        <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                        <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                        <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                        <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                        <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                        <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                        <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                        <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-5">
                    <h4 class="font-weight-bold mb-4">Tags</h4>
                    <div class="d-flex flex-wrap m-n1">
                        <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                        <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                        <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                        <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                        <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                        <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                        <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                        <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                        <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                        <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 mb-5">
                    <h4 class="font-weight-bold mb-4">Quick Links</h4>
                    <div class="d-flex flex-column justify-content-start">
                        <a class="text-secondary mb-2" href="/about/"><i
                                class="fa fa-angle-right text-dark mr-2"></i>About</a>
                        <a class="text-secondary mb-2" href="/advertise/"><i
                                class="fa fa-angle-right text-dark mr-2"></i>Advertise</a>
                        <a class="text-secondary mb-2" href="/privacy-policy/"><i
                                class="fa fa-angle-right text-dark mr-2"></i>Privacy &
                            policy</a>
                        <a class="text-secondary mb-2" href="/terms/"><i class="fa fa-angle-right text-dark mr-2"></i>Terms
                            &
                            conditions</a>
                        <a class="text-secondary" href="/contact/"><i
                                class="fa fa-angle-right text-dark mr-2"></i>Contact</a>
                    </div>
                </div>
            </div>
        </footer>
        <div class="container-fluid py-4 px-sm-3 px-md-5">
            <p class="m-0 text-center">
                &copy;
                <span id="presentYear">
                    <script>
                        document.querySelector("#presentYear").innerText = new Date().getFullYear()
                    </script>
                </span>
                <a class="font-weight-bold" href="/">Last24hrnews.com</a>. All Rights Reserved.
            </p>
        </div>
        <!-- Footer End -->


        <!-- Back to Top -->
        <a href="#" class="btn btn-dark back-to-top"><i class="fa fa-angle-up"></i></a>


        <!-- JavaScript Libraries -->
        <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
        <script src="/lib/easing/easing.min.js"></script>
        <script src="/lib/owlcarousel/owl.carousel.min.js"></script>

        <!-- Contact Javascript File -->
        <script src="/mail/jqBootstrapValidation.min.js"></script>
        <script src="/mail/contact.js"></script>

        <!-- Template Javascript -->
        <script src="/js/main.js"></script>
    </body>

    </html>

                            """
        
        if activePage == 1:
            saveHTMLFile(mainlocation + '/categories/' + presentCategory + '/', categoryHtmlContent)

        else:
            saveHTMLFile(mainlocation + '/categories/' + presentCategory + f'/{activePageNumber}/', categoryHtmlContent)

    categoryHtmlData = f"""<div class="row">
                        <div class="col-12">
                            <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                                <h1 class="m-0 l-txt">{presentCategory.capitalize()}</h1>
                            </div>
                        </div>"""
    
    activePageNumber = 1
    articleNumber = 1

    for articleIndex in range(0, len(categoryData)):
        articlePublishDate = categoryData[articleIndex]['publish_date']
        formattedDates = getFormattedDates(articlePublishDate)

        articleTitle = categoryData[articleIndex]['title']
        articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

        articleImage = '/img/last24hrnews.webp'
        if categoryData[articleIndex]['image'] != articleImage and 'ANI-News-Logo-96x96' not in categoryData[articleIndex]['image']:
            fileLocation = f"C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews/img/articles/{categoryData[articleIndex]['id']}.jpg"
            if not os.path.exists(fileLocation):
                try :
                    # Send a GET request to the URL
                    response = requests.get(categoryData[articleIndex]['image'])

                    # Open the image from the response content
                    img = Image.open(BytesIO(response.content))

                    # Convert the image to RGB mode if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Save the image locally
                    img.save(f"C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews/img/articles/{categoryData[articleIndex]['id']}.jpg")
                except:
                    pass
            
            articleImage = f"/img/articles/{categoryData[articleIndex]['id']}.jpg"

        if articleNumber <= 4:
            categoryHtmlData += f"""

                        <div class="col-lg-6">
                            <div class="position-relative mb-3">
                                <img class="img-fluid w-100" src="{articleImage}" style="object-fit: cover; height: 300px;">
                                <div class="overlay position-relative bg-light">
                                    <div class="mb-2" style="font-size: 14px;">
                                        <a href="/categories/{presentCategory}">{presentCategory.capitalize()}</a>
                                        <span class="px-1">/</span>
                                        <span>{formattedDates[0]}</span>
                                    </div>
                                    <h2>
                                        <a class="h4" href="{articleAnchor}">
                                            {articleTitle}
                                        </a>
                                    </h2>
                                    <p class="m-0">{categoryData[articleIndex]['text'][:120]}</p>
                                </div>
                            </div>N
                        </div>
                        """

        elif articleNumber > 4:
            categoryHtmlData += f"""
                        <div class="col-lg-6">
                            <div class="d-flex mb-3">
                                <img src="{articleImage}"
                                    style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        <a href="/categories/{presentCategory}">{presentCategory.capitalize()}</a>
                                        <span class="px-1">/</span>
                                        <span>{formattedDates[0]}</span>
                                    </div>
                                    <h2>
                                        <a class="h6 m-0" href="{articleAnchor}">{articleTitle}</a>
                                    </h2>
                                </div>
                            </div>
                        </div>
            """
        if articleNumber == 4:
            categoryHtmlData += '</div><div class="row">'
        
        if articleNumber == 14:
            saveCategoryPage(categoryHtmlData, activePage=activePageNumber)
            categoryHtmlData = """<div class="row">
                        <div class="col-12">
                            <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                                <h1 class="m-0 l-txt">Politics</h1>
                            </div>
                        </div>"""
            
            activePageNumber += 1
            articleNumber = 0
        
        articleNumber += 1
    saveCategoryPage(htmlContent=categoryHtmlData, activePage=activePageNumber)

def getCategoryData(category):
    res = requests.get(f"https://api.worldnewsapi.com/search-news?language=en&sort=publish-time&sort-direction=DESC&number=100&api-key={apiKey}&source-countries=in&categories={category}")

    if res.status_code == 200:
        print(f'{category.capitalize()} data fetched succesfully...')
        data = res.json()

        data = data['news']

        newData = []

        for i in data:
            if 'category' in i and i['category'] == category:
                newData.append(i)

        # adding new news articles into the lists
        for article in newData:
            if article['id'] not in addedArticlesIds:
                categoriesData[category].insert(0, article)
                articlesTobeCreated.append(article)

        print("Data Updated...")

def getDataForHomePage(date):
    
    #getting trending news
    response = requests.get(f'https://api.worldnewsapi.com/top-news?source-country=in&language=en&date={date}&api-key={apiKey}')

    if response.status_code == 200:
        data = response.json()

        topNews = []

        for i in data['top_news']:
            for j in i['news']:
                topNews.append(j)

        maxAuthor = getMaxAuthor(topNews)

        for i in topNews:
            if 'authors' in i and maxAuthor in i['authors'] and i['id'] not in addedArticlesIds:
                articlesTobeCreated.append(i)
                if len(trendingArticlesData) > 15:
                    trendingArticlesData.pop()
                trendingArticlesData.insert(0, i)

    #getting latest news data
    response = requests.get(f'https://api.worldnewsapi.com/search-news?source-country=in&language=ensort=publish-time&sort-direction=DESC&number=100&date={date}&api-key={apiKey}')

    if response.status_code == 200:
        data = response.json()

        latestNews = data['news']

        maxAuthor = getMaxAuthor(latestNews)

        for i in latestNews:
            if 'authors' in i and maxAuthor in i['authors'] and i['id'] not in addedArticlesIds:
                articlesTobeCreated.append(i)
                if len(latestNewsArticlesData) > 15:
                    latestNewsArticlesData.pop()
                latestNewsArticlesData.insert(0, i)

def createHomePage():

    #for main swiper
    def getMainSliderHtml():
        html = ''

        for i in range(0, 3):
            articlePublishDate = trendingArticlesData[i]['publish_date']
            formattedDates = getFormattedDates(articlePublishDate)
            
            articleImage = '/img/last24hrnews.webp'
            if trendingArticlesData[i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in trendingArticlesData[i]['image']:
                
                articleImage = f"/img/articles/{trendingArticlesData[i]['id']}.jpg"

            articleTitle = trendingArticlesData[i]['title']
            articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)
           
            categoryHtml = ''
            if 'category' in trendingArticlesData[i]:
                category = trendingArticlesData[i]['category']
                categoryHtml = f'<a href="/{str.lower(category)}">{str.capitalize(category)}</a><span class="px-2 text-white">/</span>'

            html += f"""
    <div class="position-relative overflow-hidden" style="height: 435px;object-fit:cover;">
                                <img class="img-fluid h-100" src="{articleImage}" style="object-fit: cover;">
                                <div class="overlay">
                                    <div class="mb-1 small-txt">
                                        {categoryHtml}
                                        <span class="text-white">{formattedDates[0]}</span>
                                    </div>
                                    <h2>
                                    <a class="h2 m-0 text-white font-weight-bold" href="{articleAnchor}">
                                        {articleTitle}
                                    </a>
                                    </h2>
                                </div>
                            </div>
    """

        return html
    
    #for top slider
    def getTopSliderHtml():
        html = ''
        for i in range(3, 7):
            articlePublishDate = trendingArticlesData[i]['publish_date']
            formattedDates = getFormattedDates(articlePublishDate)
            
            articleImage = '/img/last24hrnews.webp'
            if trendingArticlesData[i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in trendingArticlesData[i]['image']:
                
                articleImage = f"/img/articles/{trendingArticlesData[i]['id']}.jpg"

            articleTitle = trendingArticlesData[i]['title']
            articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

            
            html += f"""
        <div class="d-flex">
                        <img src="{articleImage}" style="width: 80px; height: 80px; object-fit: cover;">   q
                        <div class="d-flex align-items-center bg-light px-3" style="height: 80px;">
                        <h3 class="small-txt">
                            <a class="text-secondary font-weight-semi-bold" href="{articleAnchor}">
                                {articleTitle}
                            </a>
                        </h3>
                        </div>
                    </div>
        """
        
        return html
        
    #for bottom slider
    def getBottomSliderHtml():
        html = ''
        for i in range(7, 13):
            articlePublishDate = trendingArticlesData[i]['publish_date']
            formattedDates = getFormattedDates(articlePublishDate)
            
            articleImage = '/img/last24hrnews.webp'
            if trendingArticlesData[i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in trendingArticlesData[i]['image']:
                
                articleImage = f"/img/articles/{trendingArticlesData[i]['id']}.jpg"

            articleTitle = trendingArticlesData[i]['title']
            articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

            categoryHtml = ''
            if 'category' in trendingArticlesData[i]:
                category = trendingArticlesData[i]['category']
                categoryHtml = f'<a href="/{str.lower(category)}">{str.capitalize(category)}</a><span class="px-2 text-white">/</span>'
            html += f"""
        <div class="position-relative overflow-hidden" style="height: 300px;">
                            <img class="/img-fluid w-100 h-100" src="{articleImage}" style="object-fit: cover;">
                            <div class="overlay">
                                <div class="mb-1 small-txt">
                                    {categoryHtml}
                                    <span class="text-white">{formattedDates[0]}</span>
                                </div>
                                <h3 class="m-l-txt">
                                    <a class="h4 m-0 text-white" href="{articleAnchor}">{articleTitle}</a>
                                </h3>
                            </div>
                        </div>
        """
        
        return html
            
    #for categories
    def getCategoriesHtmlForHome():

        htmltext = ""
        
        count = 0
        for category in categories:
            if count % 2 == 0:
                htmltext += """<div class="container-fluid">
                <div class="container">
                    <div class="row">"""
            tempHtml = ""
            for i in range(0,3):

                articlePublishDate = categoriesData[category][i]['publish_date']
                formattedDates = getFormattedDates(articlePublishDate)
                
                articleImage = '/img/last24hrnews.webp'
                if categoriesData[category][i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in categoriesData[category][i]['image']:
                    
                    articleImage = f"/img/articles/{categoriesData[category][i]['id']}.jpg"

                articleTitle = categoriesData[category][i]['title']
                articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

                tempHtml += f"""<div class="position-relative">
                            <img class="img-fluid w-100" src="{articleImage}" style="height:200px;object-fit: cover;">
                            <div class="overlay position-relative bg-light">
                                <div class="mb-2" style="font-size: 13px;">
                                    <a href="/categories/{category}">{category.capitalize()}</a>
                                    <span class="px-1">/</span>
                                    <span>{formattedDates[0]}</span>
                                </div>
                                <h4>
                                    <a class="h4 m-0" href="{articleAnchor}">{articleTitle}</a>
                                </h4>
                            </div>
                        </div>"""
            htmltext += f"""<div class="col-lg-6 py-3 pb-0">
                <div class="bg-light py-2 px-4 mb-3">
                    <h3 class="m-0">{category.capitalize()}</h3>
                </div>
                <div class="owl-carousel owl-carousel-3 carousel-item-2 position-relative">
                    {tempHtml}
                </div>
            </div>"""
        
            count += 1
            if count % 2 == 0:
                htmltext += """</div>
                        </div>
                    </div>"""
        
        return htmltext

    #for latest news
    def getLatestNewsHtmlForHome():
        htmltext = ""

        for i in range(0, 6):

            if i == 0 or i == 3:
                htmltext += '<div class="col-lg-6">'

            articlePublishDate = latestNewsArticlesData[i]['publish_date']
            formattedDates = getFormattedDates(articlePublishDate)

            categoryHtml = ''
            if 'category' in latestNewsArticlesData[i]:
                categoryHtml = f"""<a href="/{latestNewsArticlesData[i]['category']}">{latestNewsArticlesData[i]['category'].capitalize()}</a><span class="px-2">/</span>"""

            articleImage = '/img/last24hrnews.webp'
            if latestNewsArticlesData[i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in latestNewsArticlesData[i]['image']:
                
                articleImage = f"/img/articles/{latestNewsArticlesData[i]['id']}.jpg"

            articleTitle = latestNewsArticlesData[i]['title']
            articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

            if i == 0 or i == 3:

                htmltext += f"""<div class="position-relative mb-3">
                                <img class="img-fluid w-100" src="{articleImage}"
                                    style="object-fit: cover;height:200px;">
                                <div class="overlay position-relative bg-light">
                                    <div class="mb-2 small-txt">
                                        {categoryHtml}
                                        <span>{formattedDates[0]}</span>
                                    </div>
                                    <h3 class="m-txt">
                                        <a class="h4" href="{articleAnchor}">{articleTitle}</a>
                                    </h3>
                                    <p class="m-0">{latestNewsArticlesData[i]['text'][:120]}</p>
                                </div>
                            </div>"""
            else:
                htmltext += f"""<div class="d-flex mb-3">
                                <img src="{articleImage}"
                                    style="width: 100px; height: 100px; object-fit: cover;">
                                <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                    style="height: 100px;">
                                    <div class="mb-1" style="font-size: 13px;">
                                        {categoryHtml}
                                        <span>{formattedDates[0]}</span>
                                    </div>
                                    <h3 class="m-txt">
                                        <a class="h6 m-0" href="{articleAnchor}">{articleTitle}</a>
                                    </h3>
                                </div>
                            </div>"""
            
            if i == 2 or i == 5:
                htmltext += '</div>'
            

        return htmltext

    htmltext = f"""
<!DOCTYPE html>
<html lang="en">

<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5707347915371687"
        crossorigin="anonymous"></script>
    <meta charset="utf-8">
    <title>Last24hrnews | Breaking News, Every Hour – Stay Informed with Last24HRNews!</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
    <meta content="news, last24hrnews, latest news, trending news" name="keywords">
    <meta
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates."
        name="description">
    <meta property="og:type" content="website" />

    <link rel="apple-touch-icon" sizes="180x180" href="/img/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="/img/favicon_io/site.webmanifest">

    <meta property="og:url" content="https://last24hrnews.com/" />
    <meta property="article:modified_time" content="{presentFormattedDates[3]}">
    <meta property="og:title" content="Breaking News, Every Hour – Stay Informed with Last24HRNews!" />
    <meta property="og:image" content="/img/last24hrnews.webp" />
    <meta property="og:image:width" content="650">
    <meta property="og:image:height" content="350">
    <meta property="og:description"
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates." />
    <link rel="canonical" href="https://last24hrnews.com/">

    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css" rel="stylesheet">

    <link href="/lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">

    <link href="/css/style.css" rel="stylesheet">
</head>

<body>
    <!-- Navbar Start -->
    <header class="container-fluid p-0 mb-3">
        <nav class="navbar navbar-expand-lg bg-light navbar-light py-2 py-lg-0 px-lg-5">
            <a href="/" class="navbar-brand d-lg-block">
                <img src="/img/logo.png" class="logo" />
            </a>
            <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-between px-0 px-lg-3" id="navbarCollapse">
                <div class="navbar-nav mr-auto py-0">
                    <a href="/" class="nav-item nav-link active">Home</a>
                    <a href="/search" class="nav-item nav-link">Search News</a>
                    <!-- <a href="" class="nav-item nav-link">Politics</a> -->
                    <div class="nav-item dropdown">
                        <a href="" class="nav-link dropdown-toggle" data-toggle="dropdown">Categories</a>
                        <div class="dropdown-menu rounded-0 m-0">
                            <a href="/categories/politics/" class="dropdown-item mb-1">Politics</a>
                            <a href="/categories/technology/" class="dropdown-item mb-1">Technology</a>
                            <a href="/categories/sports/" class="dropdown-item mb-1">Sports</a>
                            <a href="/categories/business/" class="dropdown-item mb-1">Business</a>
                            <a href="/categories/" class="dropdown-item mb-1">View More</a>
                        </div>
                    </div>
                    <a href="/contact/" class="nav-item nav-link">Contact</a>
                </div>
                <div class="input-group ml-auto" style="width: 100%; max-width: 300px;">
                    <input type="text" class="form-control" placeholder="Keyword">
                    <div class="input-group-append">
                        <button class="input-group-text text-secondary"><i class="fa fa-search"></i></button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
    <!-- Navbar End -->

    <!-- Top News Slider Start -->
    <div class="container-fluid py-3 pb-0">
        <div class="container">
            <div class="owl-carousel owl-carousel-2 carousel-item-3 position-relative">{getTopSliderHtml()}</div>
        </div>
    </div>
    <!-- Top News Slider End -->

    <!-- Main News Slider Start -->
    <main class="container-fluid py-3 main-slider">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="owl-carousel owl-carousel-2 carousel-item-1 position-relative mb-3 mb-lg-0">{getMainSliderHtml()}</div>
                </div>
                <div class="col-lg-4">
                    <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                        <h3 class="m-0">Categories</h3>
                        <a class="text-secondary font-weight-medium text-decoration-none" href="/categories/">View
                            All</a>
                    </div>
                    <div class="position-relative overflow-hidden mb-3" style="height: 80px;">
                        <img class="/img-fluid w-100 h-100" src="/img/politics.jpg" style="object-fit: cover;">
                        <a href=""
                            class="overlay align-items-center justify-content-center h4 m-0 text-white text-decoration-none">
                            Politics
                        </a>
                    </div>
                    <div class="position-relative overflow-hidden mb-3" style="height: 80px;">
                        <img class="/img-fluid w-100 h-100" src="/img/cat-500x80-2.jpg" style="object-fit: cover;">
                        <a href=""
                            class="overlay align-items-center justify-content-center h4 m-0 text-white text-decoration-none">
                            Technology
                        </a>
                    </div>
                    <div class="position-relative overflow-hidden mb-3" style="height: 80px;">
                        <img class="/img-fluid w-100 h-100" src="/img/cat-500x80-3.jpg" style="object-fit: cover;">
                        <a href=""
                            class="overlay align-items-center justify-content-center h4 m-0 text-white text-decoration-none">
                            Entertainment
                        </a>
                    </div>
                    <div class="position-relative overflow-hidden" style="height: 80px;">
                        <img class="/img-fluid w-100 h-100" src="/img/sports.png" style="object-fit: cover;">
                        <a href=""
                            class="overlay align-items-center justify-content-center h4 m-0 text-white text-decoration-none">
                            Sports
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <!-- Main News Slider End -->


    <!-- Featured News Slider Start -->
    <div class="container-fluid py-3 pb-0 featured">
        <div class="container">
            <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                <h3 class="m-0">Featured</h3>
                <a class="text-secondary font-weight-medium text-decoration-none" href="">View All</a>
            </div>
            <div class="owl-carousel owl-carousel-2 carousel-item-4 position-relative">{getBottomSliderHtml()}</div>
        </div>
    </div>
    </div>
    <!-- Featured News Slider End -->

    {getCategoriesHtmlForHome()}


    <!-- News With Sidebar Start -->
    <div class="container-fluid py-3 latest-news">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">

                    <div class="row">
                        <div class="col-12">
                            <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                                <h3 class="m-0">Latest</h3>
                            </div>
                        </div>

                        {getLatestNewsHtmlForHome()}
                        
                    </div>
                </div>

                <div class="col-lg-4 pt-3 pt-lg-0">

                    <!-- Ads Start -->
                    <!-- <div class="mb-3 pb-3"> -->
                    <!-- <a href=""><img class="/img-fluid" src="" alt=""></a> -->
                    <!-- </div> -->
                    <!-- Ads End -->
                    <div class="pb-3 trending-container">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Trending</h3>
                        </div>
                        <!-- Popular News Start -->
                        <div class="loader-container trending-loader">

                            <div class="loader">

                            </div>
                        </div>
                    </div>
                    <!-- Popular News End -->

                    <!-- Tags Start -->
                    <div class="pb-3">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Tags</h3>
                        </div>
                        <div class="d-flex flex-wrap m-n1">
                            <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                            <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                            <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                            <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                            <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                            <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                            <a href="/categories/technology/"
                                class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                            <a href="/categories/entertainment/"
                                class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                            <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                            <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                        </div>
                    </div>
                    <!-- Tags End -->
                </div>
            </div>
        </div>
    </div>
    </div>
    <!-- News With Sidebar End -->


    <!-- Footer Start -->
    <footer class="container-fluid bg-light pt-5 px-sm-3 px-md-5">
        <div class="row align-items-center">
            <div class="col-lg-3 col-md-6 mb-5">
                <a href="/" class="navbar-brand">
                    <img src="/img/logo.png" class="logo" alt="">
                </a>
                <p>Breaking News, Every Hour – Stay Informed with Last24HRNews!</p>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Categories</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Tags</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Quick Links</h4>
                <div class="d-flex flex-column justify-content-start">
                    <a class="text-secondary mb-2" href="/about/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>About</a>
                    <a class="text-secondary mb-2" href="/advertise/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Advertise</a>
                    <a class="text-secondary mb-2" href="/privacy-policy/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Privacy &
                        policy</a>
                    <a class="text-secondary mb-2" href="/terms/"><i class="fa fa-angle-right text-dark mr-2"></i>Terms
                        &
                        conditions</a>
                    <a class="text-secondary" href="/contact/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Contact</a>
                </div>
            </div>
        </div>
    </footer>
    <div class="container-fluid py-4 px-sm-3 px-md-5">
        <p class="m-0 text-center">
            &copy;
            <span id="presentYear">
                <script>
                    document.querySelector("#presentYear").innerText = new Date().getFullYear()
                </script>
            </span>
            <a class="font-weight-bold" href="/">Last24hrnews.com</a>. All Rights Reserved.
        </p>
    </div>
    <!-- Footer End -->


    <!-- Back to Top -->
    <a href="#" class="btn btn-dark back-to-top"><i class="fa fa-angle-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
    <script src="/lib/easing/easing.min.js"></script>
    <script src="/lib/owlcarousel/owl.carousel.min.js"></script>

    <!-- Template Javascript -->
    <script src="/js/main.js"></script>
</body>

</html>"""
    
    saveHTMLFile(mainlocation + '/', htmltext)

def createCategoriesPage():
    tempHtml = ''
    for category in categories:
        tempHtml += f"""<div class="row">
                        <div class="col-12">
                            <div class="d-flex align-items-center justify-content-between bg-light py-2 px-4 mb-3">
                                <h2 class="m-0 l-txt">{category.capitalize()}</h2>
                                <a class="text-secondary font-weight-medium text-decoration-none" href="/categories/{category}">View All</a>
                            </div>
                        </div>"""
        for i in range(0,2):

            articlePublishDate = categoriesData[category][i]['publish_date']
            formattedDates = getFormattedDates(articlePublishDate)
            
            articleImage = '/img/last24hrnews.webp'
            if categoriesData[category][i]['image'] != articleImage and 'ANI-News-Logo-96x96' not in categoriesData[category][i]['image']:
                
                articleImage = f"/img/articles/{categoriesData[category][i]['id']}.jpg"

            articleTitle = categoriesData[category][i]['title']
            articleAnchor = getArticleAnchor(formattedDates[1], articleTitle)

            categoryHtml = ''
            if 'category' in categoriesData[category][i]:
                categoryHtml = f"""<a href="/categoreis/{category}">{category.capitalize()}</a>
                                        <span class="px-1">/</span>"""

            tempHtml += f"""<div class="col-lg-6">
                            <div class="position-relative mb-3">
                                <img class="img-fluid w-100" src="{articleImage}" style="object-fit: cover;height:250px;">
                                <div class="overlay position-relative bg-light">
                                    <div class="mb-2" style="font-size: 14px;">
                                        {categoryHtml}
                                        <span>{formattedDates[0]}</span>
                                    </div>
                                    <h2>
                                        <a class="h4" href="{articleAnchor}">{articleTitle}</a>
                                    </h2>
                                    <p class="m-0">{categoriesData[category][i]['text'][:120]}</p>
                                </div>
                            </div>
                        </div>"""
        
        tempHtml += '</div>'
    
    htmlContent = f"""<!DOCTYPE html>
    
<html lang="en">

<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5707347915371687"
        crossorigin="anonymous"></script>
    <meta charset="utf-8">
    <title>Categories | Last24hrnews</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
    <meta
        content="news, last24hrnews, latest news, trending news, politics, education, sports, entertainment, lifestyle, business, science, technology, travel"
        name="keywords">
    <meta
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates."
        name="description">
    <meta property="og:type" content="website" />

    <link rel="apple-touch-icon" sizes="180x180" href="/img/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/img/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="/img/favicon_io/site.webmanifest">

    <meta property="og:url" content="https://last24hrnews.com/categories/" />
    <meta property="article:modified_time" content="{presentFormattedDates[3]}">
    <meta property="og:title" content="Categories | last24hrnews" />
    <meta property="og:image" content="/img/last24hrnews.png" />
    <meta property="og:image:width" content="650">
    <meta property="og:image:height" content="350">
    <meta property="og:description"
        content="At Last24HRNews, we keep you connected to the pulse of the world with timely updates and accurate reporting. Whether it's global events, politics, technology, or local stories, we bring you the latest breaking news as it happens, every hour of the day. With our commitment to real-time coverage, you'll always be informed and ahead of the curve. Stay tuned and never miss a headline with Last24HRNews — your go-to source for round-the-clock news updates." />
    <link rel="canonical" href="https://last24hrnews.com/categories/">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.0/css/all.min.css" rel="stylesheet">

    <link href="/lib/owlcarousel/assets/owl.carousel.min.css" rel="stylesheet">

    <link href="/css/style.css" rel="stylesheet">
</head>

<body>
    <!-- Topbar Start -->
    <header class="container-fluid p-0 mb-3">
        <nav class="navbar navbar-expand-lg bg-light navbar-light py-2 py-lg-0 px-lg-5">
            <a href="/" class="navbar-brand d-lg-block">
                <img src="/img/logo.png" class="logo" />
            </a>
            <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbarCollapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse justify-content-between px-0 px-lg-3" id="navbarCollapse">
                <div class="navbar-nav mr-auto py-0">
                    <a href="/" class="nav-item nav-link">Home</a>
                    <a href="/search" class="nav-item nav-link">Search News</a>
                    <!-- <a href="" class="nav-item nav-link">Politics</a> -->
                    <div class="nav-item dropdown">
                        <a href="" class="nav-link dropdown-toggle" data-toggle="dropdown">Categories</a>
                        <div class="dropdown-menu rounded-0 m-0">
                            <a href="/categories/politics/" class="dropdown-item mb-1">Politics</a>
                            <a href="/categories/technology/" class="dropdown-item mb-1">Technology</a>
                            <a href="/categories/sports/" class="dropdown-item mb-1">Sports</a>
                            <a href="/categories/business/" class="dropdown-item mb-1">Business</a>
                            <a href="/categories/" class="dropdown-item mb-1">View More</a>
                        </div>
                    </div>
                    <a href="/contact/" class="nav-item nav-link">Contact</a>
                </div>
                <div class="input-group ml-auto" style="width: 100%; max-width: 300px;">
                    <input type="text" class="form-control" placeholder="Keyword">
                    <div class="input-group-append">
                        <button class="input-group-text text-secondary"><i class="fa fa-search"></i></button>
                    </div>
                </div>
            </div>
        </nav>
    </header>
    <!-- Topbar End -->

    <!-- Breadcrumb Start -->
    <div class="container-fluid">
        <div class="container small-txt">
            <nav class="breadcrumb bg-transparent m-0 p-0">
                <a class="breadcrumb-item" href="/">Home</a>
                <span class="breadcrumb-item active">Categories</span>
            </nav>
        </div>
    </div>
    <!-- Breadcrumb End -->


    <!-- News With Sidebar Start -->
    <div class="container-fluid py-3">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    
                    {tempHtml}
                    
                </div>

                <div class="col-lg-4 pt-3 pt-lg-0">

                    <!-- Popular News Start -->
                    <div class="pb-3">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Trending</h3>
                        </div>
                        <div class="d-flex mb-3">
                            <img src="/img/news-100x100-1.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    <a href="">Technology</a>
                                    <span class="px-1">/</span>
                                    <span>January 01, 2045</span>
                                </div>
                                <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                            </div>
                        </div>
                        <div class="d-flex mb-3">
                            <img src="/img/news-100x100-2.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    <a href="">Technology</a>
                                    <span class="px-1">/</span>
                                    <span>January 01, 2045</span>
                                </div>
                                <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                            </div>
                        </div>
                        <div class="d-flex mb-3">
                            <img src="/img/news-100x100-3.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    <a href="">Technology</a>
                                    <span class="px-1">/</span>
                                    <span>January 01, 2045</span>
                                </div>
                                <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                            </div>
                        </div>
                        <div class="d-flex mb-3">
                            <img src="/img/news-100x100-4.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    <a href="">Technology</a>
                                    <span class="px-1">/</span>
                                    <span>January 01, 2045</span>
                                </div>
                                <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                            </div>
                        </div>
                        <div class="d-flex mb-3">
                            <img src="/img/news-100x100-5.jpg" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    <a href="">Technology</a>
                                    <span class="px-1">/</span>
                                    <span>January 01, 2045</span>
                                </div>
                                <a class="h6 m-0" href="">Lorem ipsum dolor sit amet consec adipis elit</a>
                            </div>
                        </div>
                    </div>
                    <!-- Popular News End -->

                    <!-- Tags Start -->
                    <div class="pb-3">
                        <div class="bg-light py-2 px-4 mb-3">
                            <h3 class="m-0">Tags</h3>
                        </div>
                        <div class="d-flex flex-wrap m-n1">
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                            <a href="" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                        </div>
                    </div>
                    <!-- Tags End -->
                </div>
            </div>
        </div>
    </div>
    </div>
    <!-- News With Sidebar End -->


    <!-- Footer Start -->
    <footer class="container-fluid bg-light pt-5 px-sm-3 px-md-5">
        <div class="row align-items-center">
            <div class="col-lg-3 col-md-6 mb-5">
                <a href="/" class="navbar-brand">
                    <img src="/img/logo.png" class="logo" alt="">
                </a>
                <p>Breaking News, Every Hour – Stay Informed with Last24HRNews!</p>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Categories</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Tags</h4>
                <div class="d-flex flex-wrap m-n1">
                    <a href="/categories/politics/" class="btn btn-sm btn-outline-secondary m-1">Politics</a>
                    <a href="/categories/business" class="btn btn-sm btn-outline-secondary m-1">Business</a>
                    <a href="/categories/sports/" class="btn btn-sm btn-outline-secondary m-1">Sports</a>
                    <a href="/categories/health/" class="btn btn-sm btn-outline-secondary m-1">Health</a>
                    <a href="/categories/education/" class="btn btn-sm btn-outline-secondary m-1">Education</a>
                    <a href="/categories/science/" class="btn btn-sm btn-outline-secondary m-1">Science</a>
                    <a href="/categories/technology/" class="btn btn-sm btn-outline-secondary m-1">Technology</a>
                    <a href="/categories/entertainment/" class="btn btn-sm btn-outline-secondary m-1">Entertainment</a>
                    <a href="/categories/travel/" class="btn btn-sm btn-outline-secondary m-1">Travel</a>
                    <a href="/categories/lifestyle/" class="btn btn-sm btn-outline-secondary m-1">Lifestyle</a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 mb-5">
                <h4 class="font-weight-bold mb-4">Quick Links</h4>
                <div class="d-flex flex-column justify-content-start">
                    <a class="text-secondary mb-2" href="/about/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>About</a>
                    <a class="text-secondary mb-2" href="/advertise/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Advertise</a>
                    <a class="text-secondary mb-2" href="/privacy-policy/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Privacy &
                        policy</a>
                    <a class="text-secondary mb-2" href="/terms/"><i class="fa fa-angle-right text-dark mr-2"></i>Terms
                        &
                        conditions</a>
                    <a class="text-secondary" href="/contact/"><i
                            class="fa fa-angle-right text-dark mr-2"></i>Contact</a>
                </div>
            </div>
        </div>
    </footer>
    <div class="container-fluid py-4 px-sm-3 px-md-5">
        <p class="m-0 text-center">
            &copy;
            <span id="presentYear">
                <script>
                    document.querySelector("#presentYear").innerText = new Date().getFullYear()
                </script>
            </span>
            <a class="font-weight-bold" href="/">Last24hrnews.com</a>. All Rights Reserved.
        </p>
    </div>
    <!-- Footer End -->


    <!-- Back to Top -->
    <a href="#" class="btn btn-dark back-to-top"><i class="fa fa-angle-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js"></script>
    <script src="/lib/easing/easing.min.js"></script>
    <script src="/lib/owlcarousel/owl.carousel.min.js"></script>

    <!-- Contact Javascript File -->
    <script src="/mail/jqBootstrapValidation.min.js"></script>
    <script src="/mail/contact.js"></script>

    <!-- Template Javascript -->
    <script src="/js/main.js"></script>
</body>

</html>"""

    saveHTMLFile(mainlocation + '/categories/', htmlContent)


def createAllTheArticles():
    for article in articlesTobeCreated:
        createArticlePage(article)


def startProgram():
    fetchData = int(input('Want to fetch data or not 0 or 1:'))
    if fetchData == 1:
        #getting the data
        print('Started getting the data..')
        getDataForHomePage(presentFormattedDates[1])
        time.sleep(10)
        print('Collected data for Home Page')
        for category in categories:
            print(f'Started colleting data for {category}')
            getCategoryData(category)
            time.sleep(10)
            print(f'Finished collecting data for {category}')
        print('Finised getting data...')

        print('Saving data into json files')
        saveJSONFile(dataLocation + 'trending.json', trendingArticlesData)
        saveJSONFile(dataLocation + 'latestNews.json', latestNewsArticlesData)
        
        for category in categories:
            saveJSONFile(dataLocation + f'categories/{category}.json', categoriesData[category])

        saveJSONFile(dataLocation + 'all_articles.json', allArticlesData)
        saveJSONFile(dataLocation + 'addedArticleIds.json', addedArticlesIds)
        print('Finished saving data into json files')

    #started creating pages
    print('Started Creating articles pages')
    createAllTheArticles()
    print("Creating article pages is completed")

    print('Started creating Home Page')
    createHomePage()
    print('Creating home page is completed')

    print('Started creating categories pages')
    createCategoriesPage()
    print('Creating categories page is completed')

    print('Started Creating Each category page')
    for category in categories:
        print(f'Creating {category.capitalize()} page')
        createCategoryPage(categoriesData[category])
        print(f'Creating {category.capitalize()} page is completed')

    print('Creating Each Category page is Complted')

    print('Program Finished !')

mainlocation = r'C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews'
dataLocation = r'C:/Users/vivek/OneDrive/Desktop/Animerulzzz/last24hrnews/data/'
categories = [
    'politics',
    "sports",
    "education",
    "business",
    "entertainment",
    "health",
    "lifestyle",
    "technology",
    'travel',
    'science',
    'envorinment'
]

apiKey = setApiKey()

articlesTobeCreated = a

now = datetime.now()
presentFormattedDates = getFormattedDates(now)

#collecting present available data in the json files
trendingArticlesData = getJsonFileData(dataLocation + 'trending.json')
latestNewsArticlesData = getJsonFileData(dataLocation + 'latestNews.json')
categoriesData = {}
for category in categories:
    categoriesData[category] = getJsonFileData(dataLocation + f'categories/{category}.json')

allArticlesData = getJsonFileData(dataLocation + 'all_articles.json')
addedArticlesIds = getJsonFileData(dataLocation + 'addedArticleIds.json')

if __name__ == '__main__':
    startProgram()

    end_time = time.time()
    execution_time = start_time - end_time
    minutes = execution_time // 60
    seconds = execution_time % 60

    if minutes > 0:
        print(f"Program Executed in {minutes} min and {seconds} sec")
    else:
        print(f"Program Executed in {seconds} sec")
