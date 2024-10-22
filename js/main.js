(function ($) {
    "use strict";

    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    try {


        // Tranding carousel
        $(".tranding-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 2000,
            items: 1,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="fa fa-angle-left"></i>',
                '<i class="fa fa-angle-right"></i>'
            ]
        });


        // Carousel item 1
        $(".carousel-item-1").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            items: 1,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="fa fa-angle-left" aria-hidden="true"></i>',
                '<i class="fa fa-angle-right" aria-hidden="true"></i>'
            ]
        });

        // Carousel item 2
        $(".carousel-item-2").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            margin: 30,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="fa fa-angle-left" aria-hidden="true"></i>',
                '<i class="fa fa-angle-right" aria-hidden="true"></i>'
            ],
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 1
                },
                768: {
                    items: 2
                }
            }
        });


        // Carousel item 3
        $(".carousel-item-3").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            margin: 30,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="fa fa-angle-left" aria-hidden="true"></i>',
                '<i class="fa fa-angle-right" aria-hidden="true"></i>'
            ],
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 1
                },
                768: {
                    items: 2
                },
                992: {
                    items: 3
                }
            }
        });


        // Carousel item 4
        $(".carousel-item-4").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            margin: 30,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="fa fa-angle-left" aria-hidden="true"></i>',
                '<i class="fa fa-angle-right" aria-hidden="true"></i>'
            ],
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 1
                },
                768: {
                    items: 2
                },
                992: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });

    }
    catch { }

    const searchBox = document.querySelector('.form-control');
    const searchIcon = document.querySelector('.input-group-append');

    searchBox.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            window.open(`/search/?query=${searchBox.value}`, "_self");
        }
    })

    searchIcon.addEventListener('click', () => {
        window.open(`/search/?query=${searchBox.value}`, "_self");
    })

    setTrending();

})(jQuery);

function cleanString(str) {
    // Remove special symbols and keep only alphanumeric characters and spaces
    let cleanedStr = str.replace(/[^a-zA-Z0-9 ]/g, '');

    // Replace all spaces with hyphens and convert the string to lowercase
    let result = cleanedStr.replace(/\s+/g, '-').toLowerCase();

    return result;
}

function setTrending() {

    const trendingContainer = document.querySelector('.trending-container');
    const trendingContainerLoader = document.querySelector('.trending-loader');
    if (trendingContainer) {
        fetch('/data/trending.json')
            .then((res) => res.json())
            .then((data) => {

                console.log(data);

                for (let i = 0; i < 5; i++) {
                    let div = document.createElement('div');
                    div.classList.add('d-flex')
                    div.classList.add('mb-3')

                    let imageSource = '/img/last24hrnews.webp'
                    if (data[i]['image'] !== imageSource && data[i]['image'].indexOf('ANI-News-Logo-96x96.jpg') === -1) {
                        imageSource = `/img/articles/${data[i]['id']}.jpg`
                    }

                    let categoryHtml = ''

                    if ('category' in data[i]) {
                        categoryHtml = `<a href="/${data[i]['category']}">${data[i]['category']}</a>
                                    <span class="px-1">/</span>`
                    }

                    // Create a Date object
                    const dateObj = new Date(data[i]['publish_date']);

                    // Extract year, month, and day
                    const year = dateObj.getFullYear();
                    const month = dateObj.getMonth(); // Months are zero-indexed (0 = January, 1 = February, etc.)
                    const day = dateObj.getDate();

                    // Convert month to string (optional for custom formatting)
                    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];

                    const formattedDate = `${monthNames[month]} ${day}, ${year}`;

                    div.innerHTML = `
                            <img src="${imageSource}" style="width: 100px; height: 100px; object-fit: cover;">
                            <div class="w-100 d-flex flex-column justify-content-center bg-light px-3"
                                style="height: 100px;">
                                <div class="mb-1" style="font-size: 13px;">
                                    ${categoryHtml}
                                    <span>${formattedDate}</span>
                                </div>
                                <h3 class="m-txt">
                                    <a class="h6 m-0" href="/news/${year}/${month + 1}/${cleanString(data[i]['title'])}">${data[i]['title']}</a>
                                </h3>
                            </div>
                        `

                    if (!trendingContainerLoader.classList.contains('hidden')) {
                        trendingContainerLoader.classList.add('hidden');
                    }
                    trendingContainer.appendChild(div);
                }

            })
    }
}