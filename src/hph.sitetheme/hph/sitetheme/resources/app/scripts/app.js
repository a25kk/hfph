requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js',
        '/scripts/a25.navbar.js'
    ],
    function(require, Flickity) {
        'use strict';

        if (typeof a25 == 'undefined') {
            var a25 = {};
        }


        // Trigger font face observer protection
        //var fontPrimary = new FontFaceObserver('Raleway');
        //var fontSecondary = new FontFaceObserver('Special Elite');

        //fontPrimary.load().then(function () {
        //    document.documentElement.className += " font__primary--loaded";
        //});

        //fontSecondary.load().then(function () {
        //    document.documentElement.className += " font__secondary--loaded";
        //});

        //Promise.all([fontPrimary.load(), fontSecondary.load()]).then(function () {
        //    document.documentElement.className += " fonts--loaded";
        //});

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



    });
