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
        drawerToggleClass: 'js-dropdown-toggle',
        dropdownOpenClass: "c-nav__link--open",
        menu: ".c-nav",
        menuContainer: ".app-header",
        menuContainerActive: "app-header--overlay",
        menuContainerOffsetMarker: "app-header--offset",
        menuDropdown: ".c-nav__dropdown",
        menuDropdownOpen: "c-nav__dropdown--open",
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

    function navigationDrawerToggle(options) {
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
                    currentDropDown.classList.add(options.menuDropdownOpen);
                    let backLinkElement = document.createElement('li'),
                        backLinkText = document.createTextNode('Parent Link (X)');
                    backLinkElement.classList.add('c-nav__item');
                    backLinkElement.classList.add('c-nav__item--parent');
                    backLinkElement.appendChild(backLinkText);
                    currentDropDown.insertBefore(backLinkElement, currentDropDown.firstChild);
                } else {
                    if (element !== element) {

                    }
                }

            })
        })

    }

    function navigationDrawerClose(options) {
        let $activeNavLink = document.querySelector(options.dropdownOpenClass),
            $menuDropDownContained = document.querySelector(options.containedDropdownClass);
        //$dropdownElements.classList.add(options.menuDropdownDisabled);
        [].forEach.call(document.getElementsByClassName(options.menuDropdownOpen), function(el) {
            el.classList.remove(options.menuDropdownOpen);
            el.classList.add(options.menuDropdownDisabled);
        });
        setTimeout(function() {
            if ($activeNavLink !== null) {
                $activeNavLink.classList.remove(options.dropdownOpenClass);
                $menuDropDownContained.classList.remove(options.containedDropdownClass);
            }
        }, 250);
    }

    function navigationDrawerOpen(el, options) {
        // Toggle sub level navigation drawers
        let $dropdownToggle = el,
            $elementParent = el.closest(options.menu),
            currentDropDown = el.nextElementSibling,
            $activeNavLink = document.querySelector(options.dropdownOpenClass),
            $menuDropDownContained = document.querySelector(options.containedDropdownClass);
        currentDropDown.classList.remove(options.menuDropdownDisabled);
        currentDropDown.classList.add(options.menuDropdownOpen);
        setTimeout(function() {
            $elementParent.classList.remove(options.menuDropdown);
            if ($activeNavLink !== null) {
                $activeNavLink.classList.remove(options.dropdownOpenClass);
                $menuDropDownContained.classList.remove(options.containedDropdownClass);
            }
        }, 250);
    }

    function navigationDrawer(options) {
        let navItem = document.getElementsByClassName('c-nav__item--has-children');
        [].forEach.call(navItem, function(el) {
            // Setup parent Links
            let navLink = el.firstChild,
                navLinkNode = navLink.cloneNode(true),
                backLinkElement = document.createElement('li'),
                currentDropDown = el.querySelector(options.menuDropdown);
            backLinkElement.classList.add('c-nav__item');
            backLinkElement.classList.add('c-nav__item--parent');
            navLinkNode.removeAttribute('aria-haspopup');
            backLinkElement.appendChild(navLinkNode);
            currentDropDown.insertBefore(backLinkElement, currentDropDown.firstChild);
        });
        document.addEventListener('click', function(event) {
            let element = event.target;
            console.log(event.target.classList);
            if (!event.target.classList.contains(options.drawerToggleClass)) {
                console.log('Close all navigation drawers');
                navigationDrawerClose(options);
            } else {
                console.log('Open navigation drawer');
                navigationDrawerOpen(element, options);
            }
        })
    }

    function toggleNavigation(options) {
        // Add navigation marker
        navigationOffsetMarker(options);
        // Sub Navigation drawer
        navigationDrawer(options);
        //navigationDrawerOpen(options);
        // navigationDrawerClose(options);
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
