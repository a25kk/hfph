if (typeof a25 == "undefined") var a25 = {};

a25.helpers = (function($, undefined) {
    "use strict";

    var _defaults = {
        anonymousUserClass: ".userrole-anonymous",
        passwordInput: "input[type=\"password\"]"
    };

    function init(_options) {
        signUpFormHelpers(_options);
    }

    function signUpFormHelpers(_options) {
        var options = $.extend({}, _defaults, _options);
        var $anonymousUser = document.querySelector(options.anonymousUserClass);
        if ($anonymousUser !== null) {
            var inputPassword = $(options.passwordInput);
            inputPassword.hideShowPassword(true, "focus");
        }
    }

    return {
        init: init
    };
})(jQuery);

jQuery(function() {
    a25.helpers.init();
});
