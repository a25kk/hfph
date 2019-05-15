define([
    "/scripts/utils.js"
], function(utils) {

    var panelEditor = {};

    var _defaults = {
        widgetSelectForm: 'js-widget-select-form',
        widgetSelectable: '.js-widget-selectable',
        widgetSelected: 'c-widget-selector__item--selected',
        widgetSelectedInputID: 'panel-page-widget',
        dropDownActiveMarker: 'o-dropdown--active'
    };

    function widgetSelector(options) {
        let widgetSelect = document.querySelectorAll(options.widgetSelectable),
            formControl = document.getElementById(options.widgetSelectedInputID);
        [].forEach.call(widgetSelect, function(element) {
            element.addEventListener('click', function(event) {
                event.preventDefault();
                [].forEach.call(widgetSelect, function(element) {
                    if(element !== this) {
                        element.classList.remove(options.widgetSelected);
                    }
                }, this);
                console.log('Selected: ' + event.currentTarget);
                element.classList.add(options.widgetSelected);
                formControl.value = element.getAttribute('data-widget-type');
            });
        });
    }

    function initializePanelEditor(options) {
        // Widget Selector
        widgetSelector(options);

    }

    panelEditor.init = function (_options) {
        // Initialize here
        let options = utils.extendDefaultOptions(_defaults, _options);
        return initializePanelEditor(options);
    };

    // return init;
    return panelEditor;

});
