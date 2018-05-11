requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/eventbox.js',
        '/scripts/interdependentselect.js',
        '/scripts/fontfaceobserver.js',
        //'/scripts/hideShowPassword.js',
        //'/scripts/jvfloat.js',
        //'/scripts/html.sortable.js',
        //'/scripts/medium-editor.js',
        //'/scripts/respimage.js',
        //'/scripts/ls.parent-fit.js',
        //'/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js',
        // '/scripts/a25.slider.js',
        //'/scripts/a25.navbar.js',
    ],
    function(require, Flickity, eventbox, interdependentselect) {
        'use strict';

        eventbox.init()
        // console.log(eventbox.init());

        // Default interdependent select boxes used in module editor
        var _selector_defaults = {
            selector: '.js-module-selector',
            classVisible: 'module__select--visible fadeInDown',
            classHidden: 'module__select--hidden fadeOutUp',
            themeSelectorBaseId: '#selector__core-theme--',
            filterFormAction: '.js-filter-action',
            filterFormActionHidden: 'filter__block--hidden',
            filterFormActionVisible: 'filter__block--visible'
        };
        interdependentselect.init(_selector_defaults);

        // Course filter select boxes
        var _selector_filter = {
            selector: '.js-filter-box',
            classVisible: 'form-field__select--visible fadeIn',
            classHidden: 'form-field__select--hidden fadeOut',
            themeSelectorBaseId: '#selector__core-theme--',
            filterFormAction: '.js-filter-action',
            filterFormActionHidden: 'filter__block--hidden',
            filterFormActionVisible: 'filter__block--visible'
        };
        interdependentselect.init(_selector_filter);

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
