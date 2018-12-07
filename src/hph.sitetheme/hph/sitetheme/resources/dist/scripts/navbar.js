define(["jquery",
], function($) {

    var navBar = {};

    var _defaults = {
        drawerCloseTrigger: ".js-drawer-close",
        drawerToggle: '[data-toggle="fly-out"]',
        menuContainer: ".app-header",
        menuContainerActive: "app-header--overlay",
        menuDropdown: "app-nav__dropdown",
        menuDropdownDisabled: "app-nav__dropdown--hidden",
        menu: ".app-nav",
        navBar: ".c-nav-bar",
        navBarToggle: ".js-nav-toggle",
        navBarOverlay: "c-nav-bar--overlay",
        navBarHidden: "c-nav-bar--hidden",
        dropdownOpenClass: "app-nav__link--open",
        containedDropdownClass: "app-nav__item--has-dropdown",
        backdropClass: ".o-backdrop",
        backdropDisplay: false
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
        var $menuContainer = $(options.menuContainer),
            $menuContainerActiveClass = options.menuContainerActive,
            $navBar = document.querySelector(options.navBar);
        if ($navBar !== null) {
            $navBar.classList.toggle(options.navBarOverlay);
            $navBar.classList.toggle(options.navBarHidden);
        }
        // $(options.navBar).toggleClass("c-nav-bar--overlay");
        // $(options.navBar).toggleClass("c-nav-bar--hidden");
        $menuContainer.toggleClass($menuContainerActiveClass);
        $menuContainer.toggleClass("u-backdrop");
        $("body").toggleClass("no-scroll");
        $(this).toggleClass("c-nav-bar__toggle--active");
        $(".app-nav__link--open").removeClass("app-nav__link--open");
        $("." + options.menuDropdown).removeClass(options.menuDropdown);
        $("." + options.containedDropdownClass).removeClass(
            options.containedDropdownClass
        );
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
