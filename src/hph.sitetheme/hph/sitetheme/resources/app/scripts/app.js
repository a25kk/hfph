requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/html.sortable.js',
        '/scripts/medium-editor.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js',
        '/scripts/a25.navbar.js'
    ],
    function(require, Flickity) {
        'use strict';

        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('Open Sans');

        fontPrimary.load().then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        Promise.all([fontPrimary.load()]).then(function () {
            document.documentElement.className += " fonts--loaded";
        });

        // Ticker bar
        var $tickerBar = document.querySelectorAll('.js-ticker');
        if ($tickerBar !== null) {
            var tickerflkty = new Flickity('.js-ticker', {
                autoPlay: 5000,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-marquee__item',
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28,
                prevNextButtons: false
            });
        }

        var $bannerBar = document.querySelector('.app-js-carousel'),
            $galleryContainer = document.querySelector('.js-gallery');
        if ($bannerBar !== null) {
            var bannerflkty = new Flickity('.app-js-carousel', {
                pauseAutoPlayOnHover: false,
                autoPlay: 7000,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-banner-item',
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28
            });
            $bannerBar.classList.add('app-banner--loaded');
        }
        // Content image galleries
        if ($galleryContainer !== null) {
            var flkty = new Flickity('.js-gallery', {
                autoPlay: true,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-gallery-cell',
                cellAlign: 'left'
            });
            $galleryContainer.classList.add('app-banner--loaded');
        }

        // Initialize scripts

        // Load Slider Resize
        window.addEventListener('load', function() {
            var sliders = Array.prototype.slice.call(document.querySelectorAll('.js-slider-resize'));
            if (sliders) {
                sliders.forEach(function(slider) {
                    var flkty = Flickity.data(slider);
                    flkty.resize()
                });
            }
        });
    }
)
