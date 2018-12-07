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
        containedDropdownClass: "app-nav__item--has-dropdown"
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

    function eventLoader(_options, callback) {
        var options = $.extend({}, _defaults, _options);
        var navBares = Array.prototype.slice.call(document.querySelectorAll(options.navBarIdentifier));
        navBares.forEach(function(navBar) {
            var sourceUrl = navBar.dataset.source,
                targetEl = navBar;
            var request = new XMLHttpRequest();
            request.open('GET', sourceUrl, true);

            request.onload = function(e) {
                if (request.status >= 200 && request.status < 400) {
                    // Success!
                    var response = request.responseText,
                        returnData = JSON.parse(response);
                    if (returnData.items && returnData.items.length) {
                        var content = '';
                        returnData.items.forEach(function(item) {
                            content += '<a class="app-card-item app-card__item"  href="' + item.url + '">';
                            content += '<time class="app-card-date app-card__date h5">' + item.date + '</time>';
                            content += '<p>' + item.title + '</p>';
                            content += '</a>';
                            // Rebuild
                            var link = document.createElement('a'),
                                timeStamp = document.createElement('time'),
                                timeStampText = document.createTextNode(item.date),
                                linkText = document.createElement('p'),
                                linkTextContent = document.createTextNode(item.title)
                            ;
                            timeStamp.setAttribute('class', 'app-card__date');
                            timeStamp.appendChild(timeStampText);
                            linkText.appendChild(linkTextContent);
                            link.setAttribute('href', item.url);
                            link.appendChild(timeStamp);
                            link.appendChild(linkText);
                            targetEl.appendChild(link);
                        });
                    }
                    // callback(JSON.parse(response), element);
                } else {
                    // We reached our target server, but it returned an error
                    console.log('Events could not be retrieved.')
                }
            };

            request.onerror = function() {
                // There was a connection error of some sort
                console.log('Connection error while retrieving events.')
            };

            request.send();
        });
    }

    navBar.my_method = function () {
        // do something
    }

    navBar.init = function (_options) {
        // Initialize here
        // var options = $.extend({}, _defaults, _options);
        var options = extend_defaults(_defaults, _options);
        return eventLoader(options);
    };

    // return init;
    return navBar;

});
