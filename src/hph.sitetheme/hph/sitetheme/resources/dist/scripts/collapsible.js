define([
    "/scripts/utils.js"
], function(utils) {

    var collapsible = {};

    var _defaults = {
        collapsibleToggle: '.js-collapsible-toggle',
        collapsibleToggleActive: 'js-collapsible-toggle--active',
        collapsibleElement: 'js-collapsible-item',
        collapsibleActiveMarker: 'c-collapsible__item--active',
        collapsibleFunctionMap: {
            'toggle': 'toggle',
            'show': 'add',
            'hide': 'remove'
        }
    };

    function collapseHandler(element, options, command) {
        let collapsibleItem = element.parentNode.getElementsByClassName(options.collapsibleElement)[0];
        collapsibleItem.classList.toggle(options.collapsibleActiveMarker);
        const functionMap = options.collapsibleFunctionMap;
        element.classList[functionMap[command]]('show');
    }

    function initializeCollapsible(options) {
        // Collapsible toggle
        var collapsibleToggle = Array.prototype.slice.call(document.querySelectorAll(options.collapsibleToggle));
        collapsibleToggle.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                collapseHandler(el, options, 'toggle');
            })
        });
    }

    collapsible.init = function (_options) {
        // Initialize here
        var options = utils.extendDefaultOptions(_defaults, _options);
        return initializeCollapsible(options);
    };

    // return init;
    return collapsible;

});
