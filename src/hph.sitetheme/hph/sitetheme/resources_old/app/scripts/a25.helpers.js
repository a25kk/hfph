if (typeof a25 == "undefined") var a25 = {};

a25.helpers = (function($, undefined) {
    "use strict";

    var _defaults = {
        anonymousUserClass: ".userrole-anonymous",
        passwordInput: "input[type=\"password\"]"
    };

    function init(_options) {
        signUpFormHelpers(_options);
        uiHelpers(_options);
    }

    function signUpFormHelpers(_options) {
        var options = $.extend({}, _defaults, _options);
        var $anonymousUser = document.querySelector(options.anonymousUserClass);
        if ($anonymousUser !== null) {
            var inputPassword = $(options.passwordInput);
            inputPassword.hideShowPassword(true, "focus");
        }
    }

    function uiHelpers(_options) {

        var $ajaxContainer = $('#appui-container');
        $('div[data-appui="ajaxified"]').each(function () {
            var $wrapper = $(this).parent(),
                $sourceUrl = $(this).data('appui-target');
            $(this).load($sourceUrl + '&ajax_load=1 #content-core >*');
        });
        $('a[data-appui="pjaxed"]').each(function () {
            var $targetUrl = $(this).attr('href'), $hideEl = $(this).data('appui-hide');
            $(this).on('click', function (e) {
                e.preventDefault();
                $(this).addClass('selected');
                $('#app-box-footer').removeClass('hide').addClass('show');
                $($hideEl).hide();
                $ajaxContainer.load($targetUrl + '?ajax_load=1 #content-core >*').fadeIn('slow');
            });
        });

        $('a[data-appui="overslide"]').on({
            click: function (e) {
                e.preventDefault();
                var targetBlock = $(this).data('target');
                if ($(targetBlock).hasClass('fadeOutTop')) {
                    $(targetBlock).removeClass('fadeOutTop').addClass('slideInRight').show();
                } else {
                    $(targetBlock).addClass('slideInRight').show();
                }
            }
        });
        $('a[data-appui="overslide-close"]').on({
            click: function (e) {
                e.preventDefault();
                $(this).closest('.panelpage-slide').removeClass('slideInRight').addClass('fadeOutTop').hide();
            }
        });
        $('a[data-appui="contextmenu"]').on({
            click: function (e) {
                e.preventDefault();
                var $contextMenu = $(this).data('target');
                $($contextMenu).toggleClass('cbp-spmenu-open');
            }
        });
        $('a[data-appui="contextmenu-close"]').on({
            click: function (e) {
                e.preventDefault();
                $(this).closest('.cbp-spmenu').removeClass('cbp-spmenu-open');
            }
        });
        $('a[data-appui="modal"]').on({
            click: function (e) {
                e.preventDefault();
                var $modal = $(this).data('target');
                $modal.on('show.bs.modal', function () {
                    var $modalBody = $(this).find('.modal-body');
                    $modalBody.load(e.currentTarget.href);
                })
                    .modal();
            }
        });
        $('a[data-appui="ajaxified"]').each(function () {
            var $targetUrl = $(this).data('source'),
                $container = $(this).data('target');
            $($container).load($targetUrl + '?ajax_load=1 #content-core >*')
                .fadeIn('slow');
        });

        $('div[data-appui="editable"]').on({
            mouseenter: function () {
                $(this).find('.contentpanel-editbar')
                    .removeClass('fadeOutUp')
                    .addClass('fadeInLeft')
                    .show();
            },
            mouseleave: function () {
                $(this).find('.contentpanel-editbar')
                    .removeClass('fadeInLeft')
                    .addClass('fadeOutUp');
            }
        });
    }

    return {
        init: init
    };
})(jQuery);

jQuery(function() {
    a25.helpers.init();
});
