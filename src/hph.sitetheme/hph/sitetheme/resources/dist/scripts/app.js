requirejs(['require',
        '/scripts/svg4everybody.js',
        '/scripts/flickity.pkgd.js',
        '/scripts/eventbox.js',
        '/scripts/interdependentselect.js',
        '/scripts/navbar.js',
        '/scripts/dropdown.js',
        '/scripts/x-ray.js',
        '/scripts/dropmic.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js'
    ],
    function(require, svg4everybody, Flickity, eventbox, interdependentselect, navbar, dropdown, xray, Dropmic) {
        'use strict';

        if (typeof a25 == 'undefined') {
            var a25 = {};
        }

        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('EB Garamond', {
            weight: 400
        });
        var fontSecondary = new FontFaceObserver('TAZ');

        fontPrimary.load(null, 3000).then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        fontSecondary.load(null, 3000).then(function () {
            document.documentElement.className += " font__secondary--loaded";
        });

        Promise.all([fontPrimary.load(null, 3000),
                     fontSecondary.load(null, 3000)
        ])
            .then(function () {
                document.documentElement.className += " fonts--loaded";
        });

        // SVG Sprite polyfill
        svg4everybody();

        xray.init();

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
