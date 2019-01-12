define([
    "jquery",
    "/scripts/utils.js"
], function($, utils) {

    var navBar = {};

    var _defaults = {
        backdropClass: "u-backdrop",
        backdropDisplay: false,
        bodyMarkerClass: "u-no-scroll",
        containedDropdownClass: "c-nav__item--has-dropdown",
        drawerCloseTrigger: ".js-drawer-close",
        drawerToggle: '.js-dropdown-toggle',
        dropdownOpenClass: "c-nav__link--open",
        menu: ".c-nav",
        menuContainer: ".app-header",
        menuContainerActive: "app-header--overlay",
        menuContainerOffsetMarker: "app-header--offset",
        menuDropdown: "c-nav__dropdown",
        menuDropdownDisabled: "c-nav__dropdown--hidden",
        navBar: ".c-nav-bar",
        navBarHidden: "c-nav-bar--hidden",
        navBarOverlay: "c-nav-bar--overlay",
        navBarToggle: ".js-nav-toggle",
        navBarToggleActiveClass: ".js-nav-toggle--active"
    };

    function navigationOffsetMarker(options) {
        var $menuContainer = document.querySelector(options.menuContainer),
            $menuContainerScrolled = $menuContainer.offsetTop;
        window.addEventListener("scroll", function() {
            if (window.pageYOffset > $menuContainerScrolled) {
                $menuContainer.classList.add(options.menuContainerOffsetMarker);
            } else {
                $menuContainer.classList.remove(options.menuContainerOffsetMarker);
            }
        })
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
            let $activeNavLink = document.querySelector(options.dropdownOpenClass),
                $menuDropDown = document.querySelector(options.menuDropdown),
                $menuDropDownContained = document.querySelector(options.containedDropdownClass);
            if ($activeNavLink !== null) {
                $activeNavLink.classList.remove(options.dropdownOpenClass);
                $menuDropDown.classList.remove(options.menuDropdown);
                $menuDropDownContained.classList.remove(options.containedDropdownClass);
            }
        }
    }

    function navigationDrawerOpen(options) {
        // Initialize drop down menu
        let $dropdownToggle = document.querySelectorAll(options.drawerToggle),
            isCurrentToggle = false;
        [].forEach.call($dropdownToggle, function(element) {
            element.addEventListener('click', function(event) {
                let currentDropDown = event.target.nextElementSibling;
                isCurrentToggle = !isCurrentToggle;
                element.classList.toggle(options.dropdownOpenClass);
                console.log(event.target.nextElementSibling);
                if (currentDropDown.matches('.c-nav--level-1')) {
                    event.preventDefault();
                    console.log("Navigation Dropdown Open Event");
                    currentDropDown.classList.remove(options.menuDropdownDisabled);
                    let backLink = '<li class="c-nav__item c.nav__item--parent">Parent Link (X)</li>',
                        backLinkElement = document.createElement(backLink);
                    currentDropDown.insertBefore(backLinkElement, currentDropDown.firstChild);
                } else {
                    if (element !== element) {

                    }
                }

            })
        })

    }

    function navigationDrawerClose(options) {
        // Close open active sub level navigation drawers
        [].forEach.call(document.querySelectorAll(options.drawerCloseTrigger), function(el) {
            el.addEventListener('click', function() {
                event.preventDefault();
                event.stopPropagation();
                console.log("Drawer close triggered");
                let $elementParent = el.closest(options.menu),
                    $activeNavLink = document.querySelector(options.dropdownOpenClass),
                    $menuDropDownContained = document.querySelector(options.containedDropdownClass);
                $elementParent.classList.add(options.menuDropdownDisabled);
                setTimeout(function() {
                    $elementParent.classList.remove(options.menuDropdown);
                    if ($activeNavLink !== null) {
                        $activeNavLink.classList.remove(options.dropdownOpenClass);
                        $menuDropDownContained.classList.remove(options.containedDropdownClass);
                    }
                }, 250);
            })
        })
    }

    function toggleNavigation(options) {
        // Add navigation marker
        navigationOffsetMarker(options);
        // Sub Navigation drawer
        navigationDrawerOpen(options);
        navigationDrawerClose(options);
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
        let options = utils.extendDefaultOptions(_defaults, _options);
        // navigationOffsetMarker(options);
        return toggleNavigation(options);
    };

    // return init;
    return navBar;

});
