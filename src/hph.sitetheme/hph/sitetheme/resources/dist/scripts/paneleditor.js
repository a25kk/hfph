define([
    "/scripts/utils.js"
], function(utils) {

    var panelEditor = {};

    var _defaults = {
        widgetSelectForm: 'js-widget-select-form',
        widgetSelectable: '.js-widget-selectable',
        widgetSelected: 'c-widget-selector__item--selected',
        dropDownActiveMarker: 'o-dropdown--active'
    };

    function widgetSelector(options) {
        let widgetSelect = document.querySelectorAll(options.widgetSelectable);
        [].forEach.call(widgetSelect, function(element) {
            element.addEventListener('click', function(event) {
                console.log('Selected: ' + event.target);
                // let checkBoxID = widgetSelect.getAttributes('data-connected-control'),
                //  checkEvent = new Event('change');
                // Get checkbox and toggle state like so:
                // checkBox.checked = !checkBox.checked;
                // checkBox.dispatchEvent(checkEvent);
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
