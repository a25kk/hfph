requirejs(['require',
        '/scripts/svg4everybody.js',
        '/scripts/flickity.pkgd.js',
        '/scripts/eventbox.js',
        '/scripts/interdependentselect.js',
        '/scripts/navbar.js',
        '/scripts/dropdown.js',
        '/scripts/collapsible.js',
        '/scripts/paneleditor.js',
        '/scripts/x-ray.js',
        '/scripts/dropmic.js',
        '/scripts/choices.min.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js'
    ],
    function(require, svg4everybody, Flickity, eventbox, interdependentselect, navbar, dropdown, collapsible, panelEditor, xray, Dropmic, Choices) {
        'use strict';

        if (typeof a25 == 'undefined') {
            var a25 = {};
        }

        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('adobe-garamond-pro', {
            weight: 400
        });
        var fontSecondary = new FontFaceObserver('TAZ');
        var fontTertiary = new FontFaceObserver('TAZSemiLight');

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

        // SVG Sprite polyfill
        svg4everybody();

        const choices = new Choices('.js-choices', {
            itemSelectText: 'auswählen',
        });

        // Drop mic initialization
        var dropmic = new Dropmic(document.querySelector('[data-dropmic="quick-link-menu"]'), {
            onOpen: function() {
                // dropmic.updateTargetBtn("Click to close");
            },
            onClose: function() {
                // dropmic.updateTargetBtn("Bottom right (default)");
            }
        });

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

        // Panel page and widget editor
        panelEditor.init();

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

        // Banner
        // TODO: refactor as independent script
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
