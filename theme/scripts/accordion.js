define([
    "/scripts/utils.js"
], function(utils) {

    var accordion = {};

    var _defaults = {
        accordionToggle: '.js-accordion-item',
        accordionToggleActive: 'js-accordion-item--active',
        accordionElement: '.js-accordion-content',
        accordionActiveMarker: 'c-pane__main--active',
        accordionFunctionMap: {
            'toggle': 'toggle',
            'show': 'add',
            'hide': 'remove'
        }
    };

    function addClass(el, klass) {
        el.classList.add(klass);
    }

    function removeClass(el, klass) {
        el.classList.remove(klass);
    }

    function closePanes(options) {
        let accordionPanes = Array.prototype.slice.call(document.querySelectorAll(options.accordionElement)),
            accordionToggle = Array.prototype.slice.call(document.querySelectorAll(options.accordionToggle));
        accordionToggle.forEach(function(el) {
            removeClass(el, "show");
            removeClass(el, options.accordionToggleActive);
        });
        accordionPanes.forEach(function(content) {
            removeClass(content, options.accordionActiveMarker);
            addClass(content, "hidden");
        });
    }

    function accordionHandler(element, options, event, command) {
        let accordionPanes = Array.prototype.slice.call(document.querySelectorAll(options.accordionElement));
        accordionPanes.forEach(function(content) {
            let paneHeader = content.previousElementSibling;
            if (paneHeader === event.currentTarget) {
                removeClass(content, "hidden");
                addClass(content, options.accordionActiveMarker);
            } else {
                removeClass(content, options.accordionActiveMarker);
                addClass(content, "hidden");
            }
        });
        // let accordionItem = element.parentNode.getElementsByClassName(options.accordionElement)[0];
        // accordionItem.classList.toggle(options.accordionActiveMarker);
    }

    function initializeAccordion(options) {
        // Collapsible toggle
        var accordionToggle = Array.prototype.slice.call(document.querySelectorAll(options.accordionToggle));
        accordionToggle.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                if (el.classList.contains(options.accordionToggleActive)) {
                    closePanes(options);
                    removeClass(el, options.accordionToggleActive);
                    removeClass(el, 'show');
                }
                else {
                    closePanes(options);
                    addClass(el, options.accordionToggleActive);
                    addClass(el, 'show');
                    accordionHandler(el, options, event, 'toggle');
                }
            })
        });
    }

    accordion.init = function (_options) {
        // Initialize here
        var options = utils.extendDefaultOptions(_defaults, _options);
        return initializeAccordion(options);
    };

    // return init;
    return accordion;

});
