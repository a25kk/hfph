requirejs(['require',
        '/scripts/svg4everybody.js',
        '/scripts/flickity.pkgd.js',
        '/scripts/eventbox.js',
        '/scripts/interdependentselect.js',
        '/scripts/navbar.js',
        '/scripts/dropdown.js',
        '/scripts/collapsible.js',
        '/scripts/accordion.js',
        '/scripts/slider.js',
        '/scripts/paneleditor.js',
        '/scripts/x-ray.js',
        '/scripts/dropmic.js',
        '/scripts/choices.min.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js'
    ],
    function(require, svg4everybody, Flickity, eventbox, interdependentselect, navbar, dropdown, collapsible, accordion, slider, panelEditor, xray, Dropmic, Choices) {
        'use strict';

        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('adobe-garamond-pro', {
            weight: 400
        });
        var fontSecondary = new FontFaceObserver('Taz-SemiBold');
        var fontTertiary = new FontFaceObserver('Taz-SemiLight');

        fontPrimary.load(null, 3000).then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        fontSecondary.load(null, 3000).then(function () {
            document.documentElement.className += " font__secondary--loaded";
        });

        fontTertiary.load(null, 3000).then(function () {
            document.documentElement.className += " font__tertiary--loaded";
        });

        Promise.all([fontPrimary.load(null, 3000),
            fontSecondary.load(null, 3000),
            fontTertiary.load(null, 3000)
        ])
            .then(function () {
                document.documentElement.className += " fonts--loaded";
            });

        if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
            document.documentElement.className += " u-device--ios";
        };

        // SVG Sprite polyfill
        svg4everybody();

        // Viewport height variable helper
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        var resizeTimeout;
        window.addEventListener('resize', () => {
            if (resizeTimeout) {
                window.cancelAnimationFrame(resizeTimeout);
            }
            resizeTimeout = window.requestAnimationFrame(function () {
                let vh = window.innerHeight * 0.01;
                document.documentElement.style.setProperty('--vh', `${vh}px`);
            });
        });

        // Choices select
        let choicesSelector = document.querySelector('.js-choices-selector');
        if (choicesSelector !== null) {
            const choices = new Choices('.js-choices-selector', {
                itemSelectText: 'auswählen',
            });
        }
        // Drop mic initialization
        let dropMicSelector = document.querySelector('[data-dropmic="quick-link-menu"]');
        if (dropMicSelector !== null) {
            var dropmic = new Dropmic(document.querySelector('[data-dropmic="quick-link-menu"]'), {
                onOpen: function() {
                    // dropmic.updateTargetBtn("Click to close");
                },
                onClose: function() {
                    // dropmic.updateTargetBtn("Bottom right (default)");
                }
            });
        }

        // Nav Bar
        navbar.init({
            backdropDisplay: true
        });

        // Quick links
        // dropdown.init({});
        // Initialize XHR Event Box
        eventbox.init();

        // Collapsible element
        collapsible.init();

        // Collapsible element
        accordion.init();

        // Panel page and widget editor
        panelEditor.init();

        slider.init({
            autoPlay: 6000
        });

        // Default interdependent select boxes used in module editor
        var _selector_defaults = {
            selector: '.js-module-selector',
            classVisible: 'o-form__control--visible fadeIn',
            classHidden: 'o-form__control--hidden fadeOut',
            themeSelectorBaseId: '#selector__core-theme--',
            filterFormAction: '.js-filter-action',
            filterFormActionHidden: 'filter__block--hidden',
            filterFormActionVisible: 'filter__block--visible'
        };
        interdependentselect.init(_selector_defaults);

        // Course filter select boxes
        var _selector_filter = {
            selector: '.js-filter-box',
            classVisible: 'o-form__control--visible fadeIn',
            classHidden: 'o-form__control--hidden fadeOut',
            themeSelectorBaseId: '#selector__core-theme--',
            filterFormAction: '.js-filter-action',
            filterFormActionHidden: 'filter__block--hidden',
            filterFormActionVisible: 'filter__block--visible'
        };
        interdependentselect.init(_selector_filter);

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
