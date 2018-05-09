requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/eventbox.js',
        '/scripts/fontfaceobserver.js',
        //'/scripts/hideShowPassword.js',
        //'/scripts/jvfloat.js',
        //'/scripts/html.sortable.js',
        //'/scripts/medium-editor.js',
        //'/scripts/respimage.js',
        //'/scripts/ls.parent-fit.js',
        //'/scripts/lazysizes-umd.js',
        //'/scripts/a25.js',
        //'/scripts/a25.helpers.js',
        // '/scripts/a25.slider.js',
        //'/scripts/a25.navbar.js',
    ],
    function(require, Flickity, eventbox) {
        'use strict';

        eventbox.init()
        // console.log(eventbox.init());

        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('Open Sans');

        fontPrimary.load().then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        Promise.all([fontPrimary.load()]).then(function () {
            document.documentElement.className += " fonts--loaded";
        });

        // Integrate carousel for news ticekr content
        var $tickerBar = document.querySelectorAll('.js-ticker');
        if ($tickerBar.length) {
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

    }
)
