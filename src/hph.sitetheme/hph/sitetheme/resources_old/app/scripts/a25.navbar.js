if (typeof a25 == "undefined") var a25 = {};

a25.navbar = (function($, undefined) {
    "use strict";

    var _defaults = {
        drawerCloseTrigger: ".js-drawer-close",
        drawerToggle: '[data-toggle="fly-out"]',
        menuContainer: ".app-header",
        menuContainerActive: "app-header--overlay",
        menuDropdown: "app-nav__dropdown",
        menuDropdownDisabled: "app-nav__dropdown--hidden",
        menu: ".app-nav",
        navBar: ".app-nav-bar",
        navBarToggle: ".js-nav-toggle",
        navBarOverlay: "app-nav-bar--overlay",
        navBarHidden: "app-nav-bar--hidden",
        dropdownOpenClass: "app-nav__link--open",
        containedDropdownClass: "app-nav__item--has-dropdown"
    };

    function init(_options) {
        // Responsive breakpoint
        var $mq = window.matchMedia("(max-width: 992px)");

        toggleNavigation(_options);

        if ($mq.matches) {
            menuDrawer(_options);
            closeDrawer(_options);
        }
    }

    function toggleNavigation(_options) {
        var options = $.extend({}, _defaults, _options);
        // Navbar toggle
        $(options.navBarToggle).on("click", function(event) {
            var $menuContainer = $(options.menuContainer),
                $menuContainerActiveClass = options.menuContainerActive;
            event.preventDefault();
            $(options.navBar).toggleClass("app-nav-bar--overlay");
            $(options.navBar).toggleClass("app-nav-bar--hidden");
            $menuContainer.toggleClass($menuContainerActiveClass);
            $("body").toggleClass("no-scroll");
            $(this).toggleClass("app-nav-bar__toggle--active");
            $(".app-nav__link--open").removeClass("app-nav__link--open");
            $("." + options.menuDropdown).removeClass(options.menuDropdown);
            $("." + options.containedDropdownClass).removeClass(
                options.containedDropdownClass
            );
        });
    }

    function menuDrawer(_options) {
        var options = $.extend({}, _defaults, _options);
        // Initialize drop down menu
        var $dropdownToggle = $(options.drawerToggle),
            $navTree = $(".app-nav--level-1"),
            $openClass = "app-nav__dropdown",
            $dropdownOpenClass = "app-nav__link--open",
            $containedDropdownClass = "app-nav__item--has-dropdown";
        // $dropdownToggle.dropdown();
        $(document).on("click", function(e) {
            e.stopPropagation();
            var $ignoredElements = $(
                '.js-nav-toggle, .js-drawer-close, .app-nav__tab--trigger, .app-nav__tab--action, [data-toggle="fly-out"], .app-nav__dropdown, .app-nav__item--has-children'
            );
            //check if the clicked area is dropDown or not
            if (!$(e.target).is($ignoredElements)) {
                $dropdownToggle.removeClass($dropdownOpenClass);
                $navTree.removeClass($openClass);
                $(".app-nav--level-1").removeClass($openClass);
                $(options.navBar)
                    .removeClass(options.navBarOverlay)
                    .addClass(options.navBarHidden);
                $("body").removeClass("no-scroll");
                if ($(".app-header--overlay").length === 0) {
                    $("body").removeClass("no-scroll");
                }
            }
        });
        $dropdownToggle.on("click", function(e) {
            var $el = $(this),
                $currentDropdown = $(this).next(".app-nav--level-1"),
                $activeOverlay = $(".app-header--overlay");
            if ($el.next().hasClass("app-nav--level-1")) {
                e.preventDefault();
                $navTree.removeClass($openClass);
                $currentDropdown.removeClass($openClass).removeAttr("style");
                var $currentToggle = $(this);
                if ($el.hasClass($dropdownOpenClass)) {
                    $el.removeClass($dropdownOpenClass);
                    $el.parent().removeClass($containedDropdownClass);
                    if ($activeOverlay.length === 0) {
                        $("body").removeClass("no-scroll");
                    }
                } else {
                    $el.not($el).removeClass($dropdownOpenClass);
                    $el
                        .not($el)
                        .parent()
                        .removeClass($containedDropdownClass);
                    $el.addClass($dropdownOpenClass);
                    $el.parent().addClass($containedDropdownClass);
                    $currentDropdown.addClass($openClass);
                    $currentDropdown.removeClass(options.menuDropdownDisabled);
                    if ($activeOverlay.length == 0) {
                        $("body").addClass("no-scroll");
                    }
                }
            }
        });
    }

    function closeDrawer(_options) {
        var options = $.extend({}, _defaults, _options);
        $(options.drawerCloseTrigger).on("click", function(event) {
            event.preventDefault();
            event.stopPropagation();
            console.log("Drawer close triggered");
            var $el = $(this),
                $elParent = $el.closest(options.menu),
                $parentNavItem = $el.closest(options.dropdownOpenClass);
            console.log($elParent);
            $elParent.addClass(options.menuDropdownDisabled);
            setTimeout(function() {
                $elParent.removeClass(options.menuDropdown);
                $(".app-nav__link--open").removeClass("app-nav__link--open");
                $("." + options.containedDropdownClass).removeClass(
                    options.containedDropdownClass
                );
            }, 250);
        });
    }

    return {
        init: init
    };
})(jQuery);

jQuery(function() {
    a25.navbar.init();
});
