define(["jquery",
], function($) {

    var navBar = {};

    var _defaults = {
        backdropClass: "u-backdrop",
        backdropDisplay: false,
        bodyMarkerClass: "u-no-scroll",
        containedDropdownClass: "app-nav__item--has-dropdown",
        drawerCloseTrigger: ".js-drawer-close",
        drawerToggle: '[data-toggle="fly-out"]',
        dropdownOpenClass: "app-nav__link--open",
        menu: ".app-nav",
        menuContainer: ".app-header",
        menuContainerActive: "app-header--overlay",
        menuDropdown: "app-nav__dropdown",
        menuDropdownDisabled: "app-nav__dropdown--hidden",
        navBar: ".c-nav-bar",
        navBarHidden: "c-nav-bar--hidden",
        navBarOverlay: "c-nav-bar--overlay",
        navBarToggle: ".js-nav-toggle",
        navBarToggleActiveClass: ".js-nav-toggle--active"
    };

    function extend_defaults(){
        for(var i=1; i<arguments.length; i++)
            for(var key in arguments[i])
                if(arguments[i].hasOwnProperty(key)) {
                    if (typeof arguments[0][key] === 'object'
                        && typeof arguments[i][key] === 'object')
                        extend(arguments[0][key], arguments[i][key]);
                    else
                        arguments[0][key] = arguments[i][key];
                }
        return arguments[0];
    }

    function navigationToggleHandler(element, options) {
        var $elBody = document.getElementsByTagName('body')[0],
            $menuContainer = document.querySelector(options.menuContainer),
            $menuContainerActiveClass = options.menuContainerActive,
            $navBar = document.querySelector(options.navBar);
        if ($navBar !== null) {
            $navBar.classList.toggle(options.navBarOverlay);
            $navBar.classList.toggle(options.navBarHidden);
            $menuContainer.classList.toggle($menuContainerActiveClass);
            $elBody.classList.toggle(options.bodyMarkerClass);
            if (options.backdropDisplay === true) {
                $menuContainer.classList.toggle(options.backdropClass);
            }
            element.classList.toggle(options.navBarToggleActiveClass);
            // TODO: Refactor active dropdown handler
            $(".app-nav__link--open").removeClass("app-nav__link--open");
            $("." + options.menuDropdown).removeClass(options.menuDropdown);
            $("." + options.containedDropdownClass).removeClass(
                options.containedDropdownClass
            );
        }
    }

    function toggleNavigation(options) {
        // Nav bar toggle
        var navBarToggle = Array.prototype.slice.call(document.querySelectorAll(options.navBarToggle));
        navBarToggle.forEach(function(el) {
            el.addEventListener("click", function(event) {
                event.preventDefault();
                navigationToggleHandler(el, options);
            })
        });
    }

    navBar.init = function (_options) {
        // Initialize here
        var options = extend_defaults(_defaults, _options);
        return toggleNavigation(options);
    };

    // return init;
    return navBar;

});
