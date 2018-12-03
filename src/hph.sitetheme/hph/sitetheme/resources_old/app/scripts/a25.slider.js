requirejs(['require',
        'jquery',
        '/scripts/flickity.pkgd.js',
    ],
    function(require, Flickity) {
        'use strict';

        a25.slider = (function($, Flickity, undefined) {
            "use strict";

            var _defaults = {
                sliderSelector: ".js-slider",
                sliderContainer: ".app-slider",
                sliderCell: ".app-slider__item",
                sliderResize: ".js-slider-resize",
                sliderLoaded: "app-slider--loaded",
                sliderActive: "js-slider--active",
                autoPlay: 5000,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28,
                prevNextButtons: false
            };

            function init(_options) {
                slider(_options);
                sliderResize(_options);
            }

            function initResize(_options) {
                sliderResize(_options);
            }

            function slider(_options) {
                var options = $.extend({}, _defaults, _options);
                var $slider = document.querySelectorAll(options.sliderSelector);
                if ($slider !== null) {
                    var sliderInstance = new Flickity(options.sliderSelector, {
                        autoPlay: options.autoPlay,
                        contain: options.contain,
                        wrapAround: options.wrapAround,
                        imagesLoaded: options.imagesLoaded,
                        cellSelector: options.sliderCell,
                        cellAlign: options.cellAlign,
                        selectedAttraction: options.selectedAttraction,
                        friction: options.friction,
                        prevNextButtons: options.prevNextButtons
                    });
                    if (sliderInstance !== null) {
                        sliderInstance.classList.add(options.sliderActive);
                        $slider.classList.add(options.sliderLoaded);
                    }
                }
            }

            function sliderResize(_options) {
                var options = $.extend({}, _defaults, _options);
                // Load Slider Resize
                window.addEventListener('load', function() {
                    var sliders = Array.prototype.slice.call(document.querySelectorAll(options.sliderResize));
                    if (sliders) {
                        sliders.forEach(function(slider) {
                            var sliderInstance = Flickity.data(slider);
                            sliderInstance.resize()
                        });
                    }
                });
            }

            return {
                init: init
            };
        })(jQuery, Flickity);
    }
)

jQuery(function() {
    a25.slider.init();
});

