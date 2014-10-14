/*!
* hph v1.0.0 by Ade25
* Copyright Ade25
* Licensed under [object Object].
*
* Designed and built by ade25
*/
/*!
 * Bootstrap v3.2.0 (http://getbootstrap.com)
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */

if (typeof jQuery === 'undefined') { throw new Error('Bootstrap\'s JavaScript requires jQuery') }

/* ========================================================================
 * Bootstrap: transition.js v3.2.0
 * http://getbootstrap.com/javascript/#transitions
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // CSS TRANSITION SUPPORT (Shoutout: http://www.modernizr.com/)
  // ============================================================

  function transitionEnd() {
    var el = document.createElement('bootstrap')

    var transEndEventNames = {
      WebkitTransition : 'webkitTransitionEnd',
      MozTransition    : 'transitionend',
      OTransition      : 'oTransitionEnd otransitionend',
      transition       : 'transitionend'
    }

    for (var name in transEndEventNames) {
      if (el.style[name] !== undefined) {
        return { end: transEndEventNames[name] }
      }
    }

    return false // explicit for ie8 (  ._.)
  }

  // http://blog.alexmaccaw.com/css-transitions
  $.fn.emulateTransitionEnd = function (duration) {
    var called = false
    var $el = this
    $(this).one('bsTransitionEnd', function () { called = true })
    var callback = function () { if (!called) $($el).trigger($.support.transition.end) }
    setTimeout(callback, duration)
    return this
  }

  $(function () {
    $.support.transition = transitionEnd()

    if (!$.support.transition) return

    $.event.special.bsTransitionEnd = {
      bindType: $.support.transition.end,
      delegateType: $.support.transition.end,
      handle: function (e) {
        if ($(e.target).is(this)) return e.handleObj.handler.apply(this, arguments)
      }
    }
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: alert.js v3.2.0
 * http://getbootstrap.com/javascript/#alerts
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // ALERT CLASS DEFINITION
  // ======================

  var dismiss = '[data-dismiss="alert"]'
  var Alert   = function (el) {
    $(el).on('click', dismiss, this.close)
  }

  Alert.VERSION = '3.2.0'

  Alert.TRANSITION_DURATION = 150

  Alert.prototype.close = function (e) {
    var $this    = $(this)
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = $(selector)

    if (e) e.preventDefault()

    if (!$parent.length) {
      $parent = $this.closest('.alert')
    }

    $parent.trigger(e = $.Event('close.bs.alert'))

    if (e.isDefaultPrevented()) return

    $parent.removeClass('in')

    function removeElement() {
      // detach from parent, fire event then clean up data
      $parent.detach().trigger('closed.bs.alert').remove()
    }

    $.support.transition && $parent.hasClass('fade') ?
      $parent
        .one('bsTransitionEnd', removeElement)
        .emulateTransitionEnd(Alert.TRANSITION_DURATION) :
      removeElement()
  }


  // ALERT PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.alert')

      if (!data) $this.data('bs.alert', (data = new Alert(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.alert

  $.fn.alert             = Plugin
  $.fn.alert.Constructor = Alert


  // ALERT NO CONFLICT
  // =================

  $.fn.alert.noConflict = function () {
    $.fn.alert = old
    return this
  }


  // ALERT DATA-API
  // ==============

  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)

}(jQuery);

/* ========================================================================
 * Bootstrap: button.js v3.2.0
 * http://getbootstrap.com/javascript/#buttons
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // BUTTON PUBLIC CLASS DEFINITION
  // ==============================

  var Button = function (element, options) {
    this.$element  = $(element)
    this.options   = $.extend({}, Button.DEFAULTS, options)
    this.isLoading = false
  }

  Button.VERSION  = '3.2.0'

  Button.DEFAULTS = {
    loadingText: 'loading...'
  }

  Button.prototype.setState = function (state) {
    var d    = 'disabled'
    var $el  = this.$element
    var val  = $el.is('input') ? 'val' : 'html'
    var data = $el.data()

    state = state + 'Text'

    if (data.resetText == null) $el.data('resetText', $el[val]())

    $el[val](data[state] == null ? this.options[state] : data[state])

    // push to event loop to allow forms to submit
    setTimeout($.proxy(function () {
      if (state == 'loadingText') {
        this.isLoading = true
        $el.addClass(d).attr(d, d)
      } else if (this.isLoading) {
        this.isLoading = false
        $el.removeClass(d).removeAttr(d)
      }
    }, this), 0)
  }

  Button.prototype.toggle = function () {
    var changed = true
    var $parent = this.$element.closest('[data-toggle="buttons"]')

    if ($parent.length) {
      var $input = this.$element.find('input')
      if ($input.prop('type') == 'radio') {
        if ($input.prop('checked') && this.$element.hasClass('active')) changed = false
        else $parent.find('.active').removeClass('active')
      }
      if (changed) $input.prop('checked', !this.$element.hasClass('active')).trigger('change')
    }

    if (changed) this.$element.toggleClass('active')
  }


  // BUTTON PLUGIN DEFINITION
  // ========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.button')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.button', (data = new Button(this, options)))

      if (option == 'toggle') data.toggle()
      else if (option) data.setState(option)
    })
  }

  var old = $.fn.button

  $.fn.button             = Plugin
  $.fn.button.Constructor = Button


  // BUTTON NO CONFLICT
  // ==================

  $.fn.button.noConflict = function () {
    $.fn.button = old
    return this
  }


  // BUTTON DATA-API
  // ===============

  $(document)
    .on('click.bs.button.data-api', '[data-toggle^="button"]', function (e) {
      var $btn = $(e.target)
      if (!$btn.hasClass('btn')) $btn = $btn.closest('.btn')
      Plugin.call($btn, 'toggle')
      e.preventDefault()
    })
    .on('focus.bs.button.data-api blur.bs.button.data-api', '[data-toggle^="button"]', function (e) {
      $(e.target).closest('.btn').toggleClass('focus', e.type == 'focus')
    })

}(jQuery);

/* ========================================================================
 * Bootstrap: carousel.js v3.2.0
 * http://getbootstrap.com/javascript/#carousel
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // CAROUSEL CLASS DEFINITION
  // =========================

  var Carousel = function (element, options) {
    this.$element    = $(element)
    this.$indicators = this.$element.find('.carousel-indicators')
    this.options     = options
    this.paused      =
    this.sliding     =
    this.interval    =
    this.$active     =
    this.$items      = null

    this.options.keyboard && this.$element.on('keydown.bs.carousel', $.proxy(this.keydown, this))

    this.options.pause == 'hover' && !('ontouchstart' in document.documentElement) && this.$element
      .on('mouseenter.bs.carousel', $.proxy(this.pause, this))
      .on('mouseleave.bs.carousel', $.proxy(this.cycle, this))
  }

  Carousel.VERSION  = '3.2.0'

  Carousel.TRANSITION_DURATION = 600

  Carousel.DEFAULTS = {
    interval: 5000,
    pause: 'hover',
    wrap: true,
    keyboard: true
  }

  Carousel.prototype.keydown = function (e) {
    switch (e.which) {
      case 37: this.prev(); break
      case 39: this.next(); break
      default: return
    }

    e.preventDefault()
  }

  Carousel.prototype.cycle = function (e) {
    e || (this.paused = false)

    this.interval && clearInterval(this.interval)

    this.options.interval
      && !this.paused
      && (this.interval = setInterval($.proxy(this.next, this), this.options.interval))

    return this
  }

  Carousel.prototype.getItemIndex = function (item) {
    this.$items = item.parent().children('.item')
    return this.$items.index(item || this.$active)
  }

  Carousel.prototype.getItemForDirection = function (direction, active) {
    var delta = direction == 'prev' ? -1 : 1
    var activeIndex = this.getItemIndex(active)
    var itemIndex = (activeIndex + delta) % this.$items.length
    return this.$items.eq(itemIndex)
  }

  Carousel.prototype.to = function (pos) {
    var that        = this
    var activeIndex = this.getItemIndex(this.$active = this.$element.find('.item.active'))

    if (pos > (this.$items.length - 1) || pos < 0) return

    if (this.sliding)       return this.$element.one('slid.bs.carousel', function () { that.to(pos) }) // yes, "slid"
    if (activeIndex == pos) return this.pause().cycle()

    return this.slide(pos > activeIndex ? 'next' : 'prev', this.$items.eq(pos))
  }

  Carousel.prototype.pause = function (e) {
    e || (this.paused = true)

    if (this.$element.find('.next, .prev').length && $.support.transition) {
      this.$element.trigger($.support.transition.end)
      this.cycle(true)
    }

    this.interval = clearInterval(this.interval)

    return this
  }

  Carousel.prototype.next = function () {
    if (this.sliding) return
    return this.slide('next')
  }

  Carousel.prototype.prev = function () {
    if (this.sliding) return
    return this.slide('prev')
  }

  Carousel.prototype.slide = function (type, next) {
    var $active   = this.$element.find('.item.active')
    var $next     = next || this.getItemForDirection(type, $active)
    var isCycling = this.interval
    var direction = type == 'next' ? 'left' : 'right'
    var fallback  = type == 'next' ? 'first' : 'last'
    var that      = this

    if (!$next.length) {
      if (!this.options.wrap) return
      $next = this.$element.find('.item')[fallback]()
    }

    if ($next.hasClass('active')) return (this.sliding = false)

    var relatedTarget = $next[0]
    var slideEvent = $.Event('slide.bs.carousel', {
      relatedTarget: relatedTarget,
      direction: direction
    })
    this.$element.trigger(slideEvent)
    if (slideEvent.isDefaultPrevented()) return

    this.sliding = true

    isCycling && this.pause()

    if (this.$indicators.length) {
      this.$indicators.find('.active').removeClass('active')
      var $nextIndicator = $(this.$indicators.children()[this.getItemIndex($next)])
      $nextIndicator && $nextIndicator.addClass('active')
    }

    var slidEvent = $.Event('slid.bs.carousel', { relatedTarget: relatedTarget, direction: direction }) // yes, "slid"
    if ($.support.transition && this.$element.hasClass('slide')) {
      $next.addClass(type)
      $next[0].offsetWidth // force reflow
      $active.addClass(direction)
      $next.addClass(direction)
      $active
        .one('bsTransitionEnd', function () {
          $next.removeClass([type, direction].join(' ')).addClass('active')
          $active.removeClass(['active', direction].join(' '))
          that.sliding = false
          setTimeout(function () {
            that.$element.trigger(slidEvent)
          }, 0)
        })
        .emulateTransitionEnd(Carousel.TRANSITION_DURATION)
    } else {
      $active.removeClass('active')
      $next.addClass('active')
      this.sliding = false
      this.$element.trigger(slidEvent)
    }

    isCycling && this.cycle()

    return this
  }


  // CAROUSEL PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.carousel')
      var options = $.extend({}, Carousel.DEFAULTS, $this.data(), typeof option == 'object' && option)
      var action  = typeof option == 'string' ? option : options.slide

      if (!data) $this.data('bs.carousel', (data = new Carousel(this, options)))
      if (typeof option == 'number') data.to(option)
      else if (action) data[action]()
      else if (options.interval) data.pause().cycle()
    })
  }

  var old = $.fn.carousel

  $.fn.carousel             = Plugin
  $.fn.carousel.Constructor = Carousel


  // CAROUSEL NO CONFLICT
  // ====================

  $.fn.carousel.noConflict = function () {
    $.fn.carousel = old
    return this
  }


  // CAROUSEL DATA-API
  // =================

  $(document).on('click.bs.carousel.data-api', '[data-slide], [data-slide-to]', function (e) {
    var href
    var $this   = $(this)
    var $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) // strip for ie7
    if (!$target.hasClass('carousel')) return
    var options = $.extend({}, $target.data(), $this.data())
    var slideIndex = $this.attr('data-slide-to')
    if (slideIndex) options.interval = false

    Plugin.call($target, options)

    if (slideIndex) {
      $target.data('bs.carousel').to(slideIndex)
    }

    e.preventDefault()
  })

  $(window).on('load', function () {
    $('[data-ride="carousel"]').each(function () {
      var $carousel = $(this)
      Plugin.call($carousel, $carousel.data())
    })
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: collapse.js v3.2.0
 * http://getbootstrap.com/javascript/#collapse
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // COLLAPSE PUBLIC CLASS DEFINITION
  // ================================

  var Collapse = function (element, options) {
    this.$element      = $(element)
    this.options       = $.extend({}, Collapse.DEFAULTS, options)
    this.transitioning = null

    if (this.options.parent) this.$parent = $(this.options.parent)
    if (this.options.toggle) this.toggle()
  }

  Collapse.VERSION  = '3.2.0'

  Collapse.TRANSITION_DURATION = 350

  Collapse.DEFAULTS = {
    toggle: true
  }

  Collapse.prototype.dimension = function () {
    var hasWidth = this.$element.hasClass('width')
    return hasWidth ? 'width' : 'height'
  }

  Collapse.prototype.show = function () {
    if (this.transitioning || this.$element.hasClass('in')) return

    var startEvent = $.Event('show.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    var actives = this.$parent && this.$parent.find('> .panel').children('.in, .collapsing')

    if (actives && actives.length) {
      var hasData = actives.data('bs.collapse')
      if (hasData && hasData.transitioning) return
      Plugin.call(actives, 'hide')
      hasData || actives.data('bs.collapse', null)
    }

    var dimension = this.dimension()

    this.$element
      .removeClass('collapse')
      .addClass('collapsing')[dimension](0)
      .attr('aria-expanded', true)

    this.transitioning = 1

    var complete = function () {
      this.$element
        .removeClass('collapsing')
        .addClass('collapse in')[dimension]('')
      this.transitioning = 0
      this.$element
        .trigger('shown.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    var scrollSize = $.camelCase(['scroll', dimension].join('-'))

    this.$element
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)[dimension](this.$element[0][scrollSize])
  }

  Collapse.prototype.hide = function () {
    if (this.transitioning || !this.$element.hasClass('in')) return

    var startEvent = $.Event('hide.bs.collapse')
    this.$element.trigger(startEvent)
    if (startEvent.isDefaultPrevented()) return

    var dimension = this.dimension()

    this.$element[dimension](this.$element[dimension]())[0].offsetHeight

    this.$element
      .addClass('collapsing')
      .removeClass('collapse in')
      .attr('aria-expanded', false)

    this.transitioning = 1

    var complete = function () {
      this.transitioning = 0
      this.$element
        .removeClass('collapsing')
        .addClass('collapse')
        .trigger('hidden.bs.collapse')
    }

    if (!$.support.transition) return complete.call(this)

    this.$element
      [dimension](0)
      .one('bsTransitionEnd', $.proxy(complete, this))
      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)
  }

  Collapse.prototype.toggle = function () {
    this[this.$element.hasClass('in') ? 'hide' : 'show']()
  }


  // COLLAPSE PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.collapse')
      var options = $.extend({}, Collapse.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data && options.toggle && option == 'show') options.toggle = false
      if (!data) $this.data('bs.collapse', (data = new Collapse(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.collapse

  $.fn.collapse             = Plugin
  $.fn.collapse.Constructor = Collapse


  // COLLAPSE NO CONFLICT
  // ====================

  $.fn.collapse.noConflict = function () {
    $.fn.collapse = old
    return this
  }


  // COLLAPSE DATA-API
  // =================

  $(document).on('click.bs.collapse.data-api', '[data-toggle="collapse"]', function (e) {
    var href
    var $this   = $(this)
    var target  = $this.attr('data-target')
        || e.preventDefault()
        || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') // strip for ie7
    var $target = $(target)
    var data    = $target.data('bs.collapse')
    var option  = data ? 'toggle' : $this.data()
    var parent  = $this.attr('data-parent')
    var $parent = parent && $(parent)

    if (!data || !data.transitioning) {
      if ($parent) $parent.find('[data-toggle="collapse"][data-parent="' + parent + '"]').not($this).addClass('collapsed').attr('aria-expanded', false)
      var isCollapsed = $target.hasClass('in')
      $this.toggleClass('collapsed', isCollapsed).attr('aria-expanded', !isCollapsed)
    }

    Plugin.call($target, option)
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: dropdown.js v3.2.0
 * http://getbootstrap.com/javascript/#dropdowns
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // DROPDOWN CLASS DEFINITION
  // =========================

  var backdrop = '.dropdown-backdrop'
  var toggle   = '[data-toggle="dropdown"]'
  var Dropdown = function (element) {
    $(element).on('click.bs.dropdown', this.toggle)
  }

  Dropdown.VERSION = '3.2.0'

  Dropdown.prototype.toggle = function (e) {
    var $this = $(this)

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    clearMenus()

    if (!isActive) {
      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
        // if mobile we use a backdrop because click events don't delegate
        $('<div class="dropdown-backdrop"/>').insertAfter($(this)).on('click', clearMenus)
      }

      var relatedTarget = { relatedTarget: this }
      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this
        .trigger('focus')
        .attr('aria-expanded', 'true')

      $parent
        .toggleClass('open')
        .trigger('shown.bs.dropdown', relatedTarget)
    }

    return false
  }

  Dropdown.prototype.keydown = function (e) {
    if (!/(38|40|27|32)/.test(e.which)) return

    var $this = $(this)

    e.preventDefault()
    e.stopPropagation()

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    if ((!isActive && e.which != 27) || (isActive && e.which == 27)) {
      if (e.which == 27) $parent.find(toggle).trigger('focus')
      return $this.trigger('click')
    }

    var desc = ' li:not(.divider):visible a'
    var $items = $parent.find('[role="menu"]' + desc + ', [role="listbox"]' + desc)

    if (!$items.length) return

    var index = $items.index($items.filter(':focus'))

    if (e.which == 38 && index > 0)                 index--                        // up
    if (e.which == 40 && index < $items.length - 1) index++                        // down
    if (!~index)                                      index = 0

    $items.eq(index).trigger('focus')
  }

  function clearMenus(e) {
    if (e && e.which === 3) return
    $(backdrop).remove()
    $(toggle).each(function () {
      var $this         = $(this)
      var $parent       = getParent($this)
      var relatedTarget = { relatedTarget: this }

      if (!$parent.hasClass('open')) return

      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $this.attr('aria-expanded', 'false')
      $parent.removeClass('open').trigger('hidden.bs.dropdown', relatedTarget)
    })
  }

  function getParent($this) {
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = selector && $(selector)

    return $parent && $parent.length ? $parent : $this.parent()
  }


  // DROPDOWN PLUGIN DEFINITION
  // ==========================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.dropdown')

      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  var old = $.fn.dropdown

  $.fn.dropdown             = Plugin
  $.fn.dropdown.Constructor = Dropdown


  // DROPDOWN NO CONFLICT
  // ====================

  $.fn.dropdown.noConflict = function () {
    $.fn.dropdown = old
    return this
  }


  // APPLY TO STANDARD DROPDOWN ELEMENTS
  // ===================================

  $(document)
    .on('click.bs.dropdown.data-api', clearMenus)
    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
    .on('click.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
    .on('keydown.bs.dropdown.data-api', toggle + ', [role="menu"], [role="listbox"]', Dropdown.prototype.keydown)

}(jQuery);

/* ========================================================================
 * Bootstrap: modal.js v3.2.0
 * http://getbootstrap.com/javascript/#modals
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // MODAL CLASS DEFINITION
  // ======================

  var Modal = function (element, options) {
    this.options        = options
    this.$body          = $(document.body)
    this.$element       = $(element)
    this.$backdrop      =
    this.isShown        = null
    this.scrollbarWidth = 0

    if (this.options.remote) {
      this.$element
        .find('.modal-content')
        .load(this.options.remote, $.proxy(function () {
          this.$element.trigger('loaded.bs.modal')
        }, this))
    }
  }

  Modal.VERSION  = '3.2.0'

  Modal.TRANSITION_DURATION = 300
  Modal.BACKDROP_TRANSITION_DURATION = 150

  Modal.DEFAULTS = {
    backdrop: true,
    keyboard: true,
    show: true
  }

  Modal.prototype.toggle = function (_relatedTarget) {
    return this.isShown ? this.hide() : this.show(_relatedTarget)
  }

  Modal.prototype.show = function (_relatedTarget) {
    var that = this
    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })

    this.$element.trigger(e)

    if (this.isShown || e.isDefaultPrevented()) return

    this.isShown = true

    this.checkScrollbar()
    this.$body.addClass('modal-open')

    this.setScrollbar()
    this.escape()

    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))

    this.backdrop(function () {
      var transition = $.support.transition && that.$element.hasClass('fade')

      if (!that.$element.parent().length) {
        that.$element.appendTo(that.$body) // don't move modals dom position
      }

      that.$element
        .show()
        .scrollTop(0)

      if (transition) {
        that.$element[0].offsetWidth // force reflow
      }

      that.$element
        .addClass('in')
        .attr('aria-hidden', false)

      that.enforceFocus()

      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })

      transition ?
        that.$element.find('.modal-dialog') // wait for modal to slide in
          .one('bsTransitionEnd', function () {
            that.$element.trigger('focus').trigger(e)
          })
          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
        that.$element.trigger('focus').trigger(e)
    })
  }

  Modal.prototype.hide = function (e) {
    if (e) e.preventDefault()

    e = $.Event('hide.bs.modal')

    this.$element.trigger(e)

    if (!this.isShown || e.isDefaultPrevented()) return

    this.isShown = false

    this.escape()

    $(document).off('focusin.bs.modal')

    this.$element
      .removeClass('in')
      .attr('aria-hidden', true)
      .off('click.dismiss.bs.modal')

    $.support.transition && this.$element.hasClass('fade') ?
      this.$element
        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
      this.hideModal()
  }

  Modal.prototype.enforceFocus = function () {
    $(document)
      .off('focusin.bs.modal') // guard against infinite focus loop
      .on('focusin.bs.modal', $.proxy(function (e) {
        if (this.$element[0] !== e.target && !this.$element.has(e.target).length) {
          this.$element.trigger('focus')
        }
      }, this))
  }

  Modal.prototype.escape = function () {
    if (this.isShown && this.options.keyboard) {
      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
        e.which == 27 && this.hide()
      }, this))
    } else if (!this.isShown) {
      this.$element.off('keydown.dismiss.bs.modal')
    }
  }

  Modal.prototype.hideModal = function () {
    var that = this
    this.$element.hide()
    this.backdrop(function () {
      that.$body.removeClass('modal-open')
      that.resetScrollbar()
      that.$element.trigger('hidden.bs.modal')
    })
  }

  Modal.prototype.removeBackdrop = function () {
    this.$backdrop && this.$backdrop.remove()
    this.$backdrop = null
  }

  Modal.prototype.backdrop = function (callback) {
    var that = this
    var animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
        .prependTo(this.$element)
        .on('click.dismiss.bs.modal', $.proxy(function (e) {
          if (e.target !== e.currentTarget) return
          this.options.backdrop == 'static'
            ? this.$element[0].focus.call(this.$element[0])
            : this.hide.call(this)
        }, this))

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      if (!callback) return

      doAnimate ?
        this.$backdrop
          .one('bsTransitionEnd', callback)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      var callbackRemove = function () {
        that.removeBackdrop()
        callback && callback()
      }
      $.support.transition && this.$element.hasClass('fade') ?
        this.$backdrop
          .one('bsTransitionEnd', callbackRemove)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callbackRemove()

    } else if (callback) {
      callback()
    }
  }

  Modal.prototype.checkScrollbar = function () {
    this.scrollbarWidth = this.measureScrollbar()
  }

  Modal.prototype.setScrollbar = function () {
    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
    if (this.scrollbarWidth) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
  }

  Modal.prototype.resetScrollbar = function () {
    this.$body.css('padding-right', '')
  }

  Modal.prototype.measureScrollbar = function () { // thx walsh
    if (document.body.clientWidth >= window.innerWidth) return 0
    var scrollDiv = document.createElement('div')
    scrollDiv.className = 'modal-scrollbar-measure'
    this.$body.append(scrollDiv)
    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
    this.$body[0].removeChild(scrollDiv)
    return scrollbarWidth
  }


  // MODAL PLUGIN DEFINITION
  // =======================

  function Plugin(option, _relatedTarget) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.modal')
      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option](_relatedTarget)
      else if (options.show) data.show(_relatedTarget)
    })
  }

  var old = $.fn.modal

  $.fn.modal             = Plugin
  $.fn.modal.Constructor = Modal


  // MODAL NO CONFLICT
  // =================

  $.fn.modal.noConflict = function () {
    $.fn.modal = old
    return this
  }


  // MODAL DATA-API
  // ==============

  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
    var $this   = $(this)
    var href    = $this.attr('href')
    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())

    if ($this.is('a')) e.preventDefault()

    $target.one('show.bs.modal', function (showEvent) {
      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
      $target.one('hidden.bs.modal', function () {
        $this.is(':visible') && $this.trigger('focus')
      })
    })
    Plugin.call($target, option, this)
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: tooltip.js v3.2.0
 * http://getbootstrap.com/javascript/#tooltip
 * Inspired by the original jQuery.tipsy by Jason Frame
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // TOOLTIP PUBLIC CLASS DEFINITION
  // ===============================

  var Tooltip = function (element, options) {
    this.type       =
    this.options    =
    this.enabled    =
    this.timeout    =
    this.hoverState =
    this.$element   = null

    this.init('tooltip', element, options)
  }

  Tooltip.VERSION  = '3.2.0'

  Tooltip.TRANSITION_DURATION = 150

  Tooltip.DEFAULTS = {
    animation: true,
    placement: 'top',
    selector: false,
    template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
    trigger: 'hover focus',
    title: '',
    delay: 0,
    html: false,
    container: false,
    viewport: {
      selector: 'body',
      padding: 0
    }
  }

  Tooltip.prototype.init = function (type, element, options) {
    this.enabled   = true
    this.type      = type
    this.$element  = $(element)
    this.options   = this.getOptions(options)
    this.$viewport = this.options.viewport && $(this.options.viewport.selector || this.options.viewport)

    var triggers = this.options.trigger.split(' ')

    for (var i = triggers.length; i--;) {
      var trigger = triggers[i]

      if (trigger == 'click') {
        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
      } else if (trigger != 'manual') {
        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focusin'
        var eventOut = trigger == 'hover' ? 'mouseleave' : 'focusout'

        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
      }
    }

    this.options.selector ?
      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
      this.fixTitle()
  }

  Tooltip.prototype.getDefaults = function () {
    return Tooltip.DEFAULTS
  }

  Tooltip.prototype.getOptions = function (options) {
    options = $.extend({}, this.getDefaults(), this.$element.data(), options)

    if (options.delay && typeof options.delay == 'number') {
      options.delay = {
        show: options.delay,
        hide: options.delay
      }
    }

    return options
  }

  Tooltip.prototype.getDelegateOptions = function () {
    var options  = {}
    var defaults = this.getDefaults()

    this._options && $.each(this._options, function (key, value) {
      if (defaults[key] != value) options[key] = value
    })

    return options
  }

  Tooltip.prototype.enter = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget).data('bs.' + this.type)

    if (self && self.$tip && self.$tip.is(':visible')) {
      self.hoverState = 'in'
      return
    }

    if (!self) {
      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
      $(obj.currentTarget).data('bs.' + this.type, self)
    }

    clearTimeout(self.timeout)

    self.hoverState = 'in'

    if (!self.options.delay || !self.options.delay.show) return self.show()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'in') self.show()
    }, self.options.delay.show)
  }

  Tooltip.prototype.leave = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget).data('bs.' + this.type)

    if (!self) {
      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
      $(obj.currentTarget).data('bs.' + this.type, self)
    }

    clearTimeout(self.timeout)

    self.hoverState = 'out'

    if (!self.options.delay || !self.options.delay.hide) return self.hide()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'out') self.hide()
    }, self.options.delay.hide)
  }

  Tooltip.prototype.show = function () {
    var e = $.Event('show.bs.' + this.type)

    if (this.hasContent() && this.enabled) {
      this.$element.trigger(e)

      var inDom = $.contains(this.$element[0].ownerDocument.documentElement, this.$element[0])
      if (e.isDefaultPrevented() || !inDom) return
      var that = this

      var $tip = this.tip()

      var tipId = this.getUID(this.type)

      this.setContent()
      $tip.attr('id', tipId)
      this.$element.attr('aria-describedby', tipId)

      if (this.options.animation) $tip.addClass('fade')

      var placement = typeof this.options.placement == 'function' ?
        this.options.placement.call(this, $tip[0], this.$element[0]) :
        this.options.placement

      var autoToken = /\s?auto?\s?/i
      var autoPlace = autoToken.test(placement)
      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'

      $tip
        .detach()
        .css({ top: 0, left: 0, display: 'block' })
        .addClass(placement)
        .data('bs.' + this.type, this)

      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)

      var pos          = this.getPosition()
      var actualWidth  = $tip[0].offsetWidth
      var actualHeight = $tip[0].offsetHeight

      if (autoPlace) {
        var orgPlacement = placement
        var $container   = this.options.container ? $(this.options.container) : this.$element.parent()
        var containerDim = this.getPosition($container)

        placement = placement == 'bottom' && pos.top   + pos.height          + actualHeight - containerDim.scroll > containerDim.height ? 'top'    :
                    placement == 'top'    && pos.top   - containerDim.scroll - actualHeight < containerDim.top                          ? 'bottom' :
                    placement == 'right'  && pos.right + actualWidth         > containerDim.width                                       ? 'left'   :
                    placement == 'left'   && pos.left  - actualWidth         < containerDim.left                                        ? 'right'  :
                    placement

        $tip
          .removeClass(orgPlacement)
          .addClass(placement)
      }

      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)

      this.applyPlacement(calculatedOffset, placement)

      var complete = function () {
        that.$element.trigger('shown.bs.' + that.type)
        that.hoverState = null
      }

      $.support.transition && this.$tip.hasClass('fade') ?
        $tip
          .one('bsTransitionEnd', complete)
          .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
        complete()
    }
  }

  Tooltip.prototype.applyPlacement = function (offset, placement) {
    var $tip   = this.tip()
    var width  = $tip[0].offsetWidth
    var height = $tip[0].offsetHeight

    // manually read margins because getBoundingClientRect includes difference
    var marginTop = parseInt($tip.css('margin-top'), 10)
    var marginLeft = parseInt($tip.css('margin-left'), 10)

    // we must check for NaN for ie 8/9
    if (isNaN(marginTop))  marginTop  = 0
    if (isNaN(marginLeft)) marginLeft = 0

    offset.top  = offset.top  + marginTop
    offset.left = offset.left + marginLeft

    // $.fn.offset doesn't round pixel values
    // so we use setOffset directly with our own function B-0
    $.offset.setOffset($tip[0], $.extend({
      using: function (props) {
        $tip.css({
          top: Math.round(props.top),
          left: Math.round(props.left)
        })
      }
    }, offset), 0)

    $tip.addClass('in')

    // check to see if placing tip in new offset caused the tip to resize itself
    var actualWidth  = $tip[0].offsetWidth
    var actualHeight = $tip[0].offsetHeight

    if (placement == 'top' && actualHeight != height) {
      offset.top = offset.top + height - actualHeight
    }

    var delta = this.getViewportAdjustedDelta(placement, offset, actualWidth, actualHeight)

    if (delta.left) offset.left += delta.left
    else offset.top += delta.top

    var isVertical          = /top|bottom/.test(placement)
    var arrowDelta          = isVertical ? delta.left * 2 - width + actualWidth : delta.top * 2 - height + actualHeight
    var arrowOffsetPosition = isVertical ? 'offsetWidth' : 'offsetHeight'

    $tip.offset(offset)
    this.replaceArrow(arrowDelta, $tip[0][arrowOffsetPosition], isVertical)
  }

  Tooltip.prototype.replaceArrow = function (delta, dimension, isHorizontal) {
    this.arrow()
      .css(isHorizontal ? 'left' : 'top', 50 * (1 - delta / dimension) + '%')
      .css(isHorizontal ? 'top' : 'left', '')
  }

  Tooltip.prototype.setContent = function () {
    var $tip  = this.tip()
    var title = this.getTitle()

    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
    $tip.removeClass('fade in top bottom left right')
  }

  Tooltip.prototype.hide = function (callback) {
    var that = this
    var $tip = this.tip()
    var e    = $.Event('hide.bs.' + this.type)

    function complete() {
      if (that.hoverState != 'in') $tip.detach()
      that.$element
        .removeAttr('aria-describedby')
        .trigger('hidden.bs.' + that.type)
      callback && callback()
    }

    this.$element.trigger(e)

    if (e.isDefaultPrevented()) return

    $tip.removeClass('in')

    $.support.transition && this.$tip.hasClass('fade') ?
      $tip
        .one('bsTransitionEnd', complete)
        .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
      complete()

    this.hoverState = null

    return this
  }

  Tooltip.prototype.fixTitle = function () {
    var $e = this.$element
    if ($e.attr('title') || typeof ($e.attr('data-original-title')) != 'string') {
      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
    }
  }

  Tooltip.prototype.hasContent = function () {
    return this.getTitle()
  }

  Tooltip.prototype.getPosition = function ($element) {
    $element   = $element || this.$element

    var el     = $element[0]
    var isBody = el.tagName == 'BODY'

    var elRect    = el.getBoundingClientRect()
    if (elRect.width == null) {
      // width and height are missing in IE8, so compute them manually; see https://github.com/twbs/bootstrap/issues/14093
      elRect = $.extend({}, elRect, { width: elRect.right - elRect.left, height: elRect.bottom - elRect.top })
    }
    var elOffset  = isBody ? { top: 0, left: 0 } : $element.offset()
    var scroll    = { scroll: isBody ? document.documentElement.scrollTop || document.body.scrollTop : $element.scrollTop() }
    var outerDims = isBody ? { width: $(window).width(), height: $(window).height() } : null

    return $.extend({}, elRect, scroll, outerDims, elOffset)
  }

  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width   }

  }

  Tooltip.prototype.getViewportAdjustedDelta = function (placement, pos, actualWidth, actualHeight) {
    var delta = { top: 0, left: 0 }
    if (!this.$viewport) return delta

    var viewportPadding = this.options.viewport && this.options.viewport.padding || 0
    var viewportDimensions = this.getPosition(this.$viewport)

    if (/right|left/.test(placement)) {
      var topEdgeOffset    = pos.top - viewportPadding - viewportDimensions.scroll
      var bottomEdgeOffset = pos.top + viewportPadding - viewportDimensions.scroll + actualHeight
      if (topEdgeOffset < viewportDimensions.top) { // top overflow
        delta.top = viewportDimensions.top - topEdgeOffset
      } else if (bottomEdgeOffset > viewportDimensions.top + viewportDimensions.height) { // bottom overflow
        delta.top = viewportDimensions.top + viewportDimensions.height - bottomEdgeOffset
      }
    } else {
      var leftEdgeOffset  = pos.left - viewportPadding
      var rightEdgeOffset = pos.left + viewportPadding + actualWidth
      if (leftEdgeOffset < viewportDimensions.left) { // left overflow
        delta.left = viewportDimensions.left - leftEdgeOffset
      } else if (rightEdgeOffset > viewportDimensions.width) { // right overflow
        delta.left = viewportDimensions.left + viewportDimensions.width - rightEdgeOffset
      }
    }

    return delta
  }

  Tooltip.prototype.getTitle = function () {
    var title
    var $e = this.$element
    var o  = this.options

    title = $e.attr('data-original-title')
      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

    return title
  }

  Tooltip.prototype.getUID = function (prefix) {
    do prefix += ~~(Math.random() * 1000000)
    while (document.getElementById(prefix))
    return prefix
  }

  Tooltip.prototype.tip = function () {
    return (this.$tip = this.$tip || $(this.options.template))
  }

  Tooltip.prototype.arrow = function () {
    return (this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow'))
  }

  Tooltip.prototype.enable = function () {
    this.enabled = true
  }

  Tooltip.prototype.disable = function () {
    this.enabled = false
  }

  Tooltip.prototype.toggleEnabled = function () {
    this.enabled = !this.enabled
  }

  Tooltip.prototype.toggle = function (e) {
    var self = this
    if (e) {
      self = $(e.currentTarget).data('bs.' + this.type)
      if (!self) {
        self = new this.constructor(e.currentTarget, this.getDelegateOptions())
        $(e.currentTarget).data('bs.' + this.type, self)
      }
    }

    self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
  }

  Tooltip.prototype.destroy = function () {
    var that = this
    clearTimeout(this.timeout)
    this.hide(function () {
      that.$element.off('.' + that.type).removeData('bs.' + that.type)
    })
  }


  // TOOLTIP PLUGIN DEFINITION
  // =========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.tooltip')
      var options = typeof option == 'object' && option

      if (!data && option == 'destroy') return
      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.tooltip

  $.fn.tooltip             = Plugin
  $.fn.tooltip.Constructor = Tooltip


  // TOOLTIP NO CONFLICT
  // ===================

  $.fn.tooltip.noConflict = function () {
    $.fn.tooltip = old
    return this
  }

}(jQuery);

/* ========================================================================
 * Bootstrap: popover.js v3.2.0
 * http://getbootstrap.com/javascript/#popovers
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // POPOVER PUBLIC CLASS DEFINITION
  // ===============================

  var Popover = function (element, options) {
    this.init('popover', element, options)
  }

  if (!$.fn.tooltip) throw new Error('Popover requires tooltip.js')

  Popover.VERSION  = '3.2.0'

  Popover.DEFAULTS = $.extend({}, $.fn.tooltip.Constructor.DEFAULTS, {
    placement: 'right',
    trigger: 'click',
    content: '',
    template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
  })


  // NOTE: POPOVER EXTENDS tooltip.js
  // ================================

  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype)

  Popover.prototype.constructor = Popover

  Popover.prototype.getDefaults = function () {
    return Popover.DEFAULTS
  }

  Popover.prototype.setContent = function () {
    var $tip    = this.tip()
    var title   = this.getTitle()
    var content = this.getContent()

    $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
    $tip.find('.popover-content').children().detach().end()[ // we use append for html objects to maintain js events
      this.options.html ? (typeof content == 'string' ? 'html' : 'append') : 'text'
    ](content)

    $tip.removeClass('fade top bottom left right in')

    // IE8 doesn't accept hiding via the `:empty` pseudo selector, we have to do
    // this manually by checking the contents.
    if (!$tip.find('.popover-title').html()) $tip.find('.popover-title').hide()
  }

  Popover.prototype.hasContent = function () {
    return this.getTitle() || this.getContent()
  }

  Popover.prototype.getContent = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-content')
      || (typeof o.content == 'function' ?
            o.content.call($e[0]) :
            o.content)
  }

  Popover.prototype.arrow = function () {
    return (this.$arrow = this.$arrow || this.tip().find('.arrow'))
  }

  Popover.prototype.tip = function () {
    if (!this.$tip) this.$tip = $(this.options.template)
    return this.$tip
  }


  // POPOVER PLUGIN DEFINITION
  // =========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.popover')
      var options = typeof option == 'object' && option

      if (!data && option == 'destroy') return
      if (!data) $this.data('bs.popover', (data = new Popover(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.popover

  $.fn.popover             = Plugin
  $.fn.popover.Constructor = Popover


  // POPOVER NO CONFLICT
  // ===================

  $.fn.popover.noConflict = function () {
    $.fn.popover = old
    return this
  }

}(jQuery);

/* ========================================================================
 * Bootstrap: scrollspy.js v3.2.0
 * http://getbootstrap.com/javascript/#scrollspy
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // SCROLLSPY CLASS DEFINITION
  // ==========================

  function ScrollSpy(element, options) {
    var process  = $.proxy(this.process, this)

    this.$body          = $('body')
    this.$scrollElement = $(element).is('body') ? $(window) : $(element)
    this.options        = $.extend({}, ScrollSpy.DEFAULTS, options)
    this.selector       = (this.options.target || '') + ' .nav li > a'
    this.offsets        = []
    this.targets        = []
    this.activeTarget   = null
    this.scrollHeight   = 0

    this.$scrollElement.on('scroll.bs.scrollspy', process)
    this.refresh()
    this.process()
  }

  ScrollSpy.VERSION  = '3.2.0'

  ScrollSpy.DEFAULTS = {
    offset: 10
  }

  ScrollSpy.prototype.getScrollHeight = function () {
    return this.$scrollElement[0].scrollHeight || Math.max(this.$body[0].scrollHeight, document.documentElement.scrollHeight)
  }

  ScrollSpy.prototype.refresh = function () {
    var offsetMethod = 'offset'
    var offsetBase   = 0

    if (!$.isWindow(this.$scrollElement[0])) {
      offsetMethod = 'position'
      offsetBase   = this.$scrollElement.scrollTop()
    }

    this.offsets = []
    this.targets = []
    this.scrollHeight = this.getScrollHeight()

    var self     = this

    this.$body
      .find(this.selector)
      .map(function () {
        var $el   = $(this)
        var href  = $el.data('target') || $el.attr('href')
        var $href = /^#./.test(href) && $(href)

        return ($href
          && $href.length
          && $href.is(':visible')
          && $el.is(':visible')
          && [[$href[offsetMethod]().top + offsetBase, href]]) || null
      })
      .sort(function (a, b) { return a[0] - b[0] })
      .each(function () {
        self.offsets.push(this[0])
        self.targets.push(this[1])
      })
  }

  ScrollSpy.prototype.process = function () {
    var scrollTop    = this.$scrollElement.scrollTop() + this.options.offset
    var scrollHeight = this.getScrollHeight()
    var maxScroll    = this.options.offset + scrollHeight - this.$scrollElement.height()
    var offsets      = this.offsets
    var targets      = this.targets
    var activeTarget = this.activeTarget
    var i

    if (this.scrollHeight != scrollHeight) {
      this.refresh()
    }

    if (scrollTop >= maxScroll) {
      return activeTarget != (i = targets[targets.length - 1]) && this.activate(i)
    }

    if (activeTarget && scrollTop <= offsets[0]) {
      return activeTarget != (i = targets[0]) && this.activate(i)
    }

    for (i = offsets.length; i--;) {
      activeTarget != targets[i]
        && scrollTop >= offsets[i]
        && (!offsets[i + 1] || scrollTop <= offsets[i + 1])
        && this.activate(targets[i])
    }
  }

  ScrollSpy.prototype.activate = function (target) {
    this.activeTarget = target

    $(this.selector)
      .parentsUntil(this.options.target, '.active')
      .removeClass('active')

    var selector = this.selector +
        '[data-target="' + target + '"],' +
        this.selector + '[href="' + target + '"]'

    var active = $(selector)
      .parents('li')
      .addClass('active')

    if (active.parent('.dropdown-menu').length) {
      active = active
        .closest('li.dropdown')
        .addClass('active')
    }

    active.trigger('activate.bs.scrollspy')
  }


  // SCROLLSPY PLUGIN DEFINITION
  // ===========================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.scrollspy')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.scrollspy', (data = new ScrollSpy(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.scrollspy

  $.fn.scrollspy             = Plugin
  $.fn.scrollspy.Constructor = ScrollSpy


  // SCROLLSPY NO CONFLICT
  // =====================

  $.fn.scrollspy.noConflict = function () {
    $.fn.scrollspy = old
    return this
  }


  // SCROLLSPY DATA-API
  // ==================

  $(window).on('load.bs.scrollspy.data-api', function () {
    $('[data-spy="scroll"]').each(function () {
      var $spy = $(this)
      Plugin.call($spy, $spy.data())
    })
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: tab.js v3.2.0
 * http://getbootstrap.com/javascript/#tabs
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // TAB CLASS DEFINITION
  // ====================

  var Tab = function (element) {
    this.element = $(element)
  }

  Tab.VERSION = '3.2.0'

  Tab.TRANSITION_DURATION = 150

  Tab.prototype.show = function () {
    var $this    = this.element
    var $ul      = $this.closest('ul:not(.dropdown-menu)')
    var selector = $this.data('target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    if ($this.parent('li').hasClass('active')) return

    var previous = $ul.find('.active:last a')[0]
    var e        = $.Event('show.bs.tab', {
      relatedTarget: previous
    })

    $this.trigger(e)

    if (e.isDefaultPrevented()) return

    var $target = $(selector)

    this.activate($this.closest('li'), $ul)
    this.activate($target, $target.parent(), function () {
      $this.trigger({
        type: 'shown.bs.tab',
        relatedTarget: previous
      })
    })
  }

  Tab.prototype.activate = function (element, container, callback) {
    var $active    = container.find('> .active')
    var transition = callback
      && $.support.transition
      && (($active.length && $active.hasClass('fade')) || !!container.find('> .fade').length)

    function next() {
      $active
        .removeClass('active')
        .find('> .dropdown-menu > .active')
        .removeClass('active')

      element.addClass('active')

      if (transition) {
        element[0].offsetWidth // reflow for transition
        element.addClass('in')
      } else {
        element.removeClass('fade')
      }

      if (element.parent('.dropdown-menu')) {
        element.closest('li.dropdown').addClass('active')
      }

      callback && callback()
    }

    $active.length && transition ?
      $active
        .one('bsTransitionEnd', next)
        .emulateTransitionEnd(Tab.TRANSITION_DURATION) :
      next()

    $active.removeClass('in')
  }


  // TAB PLUGIN DEFINITION
  // =====================

  function Plugin(option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.tab')

      if (!data) $this.data('bs.tab', (data = new Tab(this)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.tab

  $.fn.tab             = Plugin
  $.fn.tab.Constructor = Tab


  // TAB NO CONFLICT
  // ===============

  $.fn.tab.noConflict = function () {
    $.fn.tab = old
    return this
  }


  // TAB DATA-API
  // ============

  $(document).on('click.bs.tab.data-api', '[data-toggle="tab"], [data-toggle="pill"]', function (e) {
    e.preventDefault()
    Plugin.call($(this), 'show')
  })

}(jQuery);

/* ========================================================================
 * Bootstrap: affix.js v3.2.0
 * http://getbootstrap.com/javascript/#affix
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // AFFIX CLASS DEFINITION
  // ======================

  var Affix = function (element, options) {
    this.options = $.extend({}, Affix.DEFAULTS, options)

    this.$target = $(this.options.target)
      .on('scroll.bs.affix.data-api', $.proxy(this.checkPosition, this))
      .on('click.bs.affix.data-api',  $.proxy(this.checkPositionWithEventLoop, this))

    this.$element     = $(element)
    this.affixed      =
    this.unpin        =
    this.pinnedOffset = null

    this.checkPosition()
  }

  Affix.VERSION  = '3.2.0'

  Affix.RESET    = 'affix affix-top affix-bottom'

  Affix.DEFAULTS = {
    offset: 0,
    target: window
  }

  Affix.prototype.getState = function (scrollHeight, height, offsetTop, offsetBottom) {
    var scrollTop    = this.$target.scrollTop()
    var position     = this.$element.offset()
    var targetHeight = this.$target.height()

    if (offsetTop != null && this.affixed == 'top') return scrollTop < offsetTop ? 'top' : false

    if (this.affixed == 'bottom') {
      if (offsetTop != null) return (scrollTop + this.unpin <= position.top) ? false : 'bottom'
      return (scrollTop + targetHeight <= scrollHeight - offsetBottom) ? false : 'bottom'
    }

    var initializing   = this.affixed == null
    var colliderTop    = initializing ? scrollTop : position.top
    var colliderHeight = initializing ? targetHeight : height

    if (offsetTop != null && colliderTop <= offsetTop) return 'top'
    if (offsetBottom != null && (colliderTop + colliderHeight >= scrollHeight - offsetBottom)) return 'bottom'

    return false
  }

  Affix.prototype.getPinnedOffset = function () {
    if (this.pinnedOffset) return this.pinnedOffset
    this.$element.removeClass(Affix.RESET).addClass('affix')
    var scrollTop = this.$target.scrollTop()
    var position  = this.$element.offset()
    return (this.pinnedOffset = position.top - scrollTop)
  }

  Affix.prototype.checkPositionWithEventLoop = function () {
    setTimeout($.proxy(this.checkPosition, this), 1)
  }

  Affix.prototype.checkPosition = function () {
    if (!this.$element.is(':visible')) return

    var height       = this.$element.height()
    var offset       = this.options.offset
    var offsetTop    = offset.top
    var offsetBottom = offset.bottom
    var scrollHeight = $('body').height()

    if (typeof offset != 'object')         offsetBottom = offsetTop = offset
    if (typeof offsetTop == 'function')    offsetTop    = offset.top(this.$element)
    if (typeof offsetBottom == 'function') offsetBottom = offset.bottom(this.$element)

    var affix = this.getState(scrollHeight, height, offsetTop, offsetBottom)

    if (this.affixed != affix) {
      if (this.unpin != null) this.$element.css('top', '')

      var affixType = 'affix' + (affix ? '-' + affix : '')
      var e         = $.Event(affixType + '.bs.affix')

      this.$element.trigger(e)

      if (e.isDefaultPrevented()) return

      this.affixed = affix
      this.unpin = affix == 'bottom' ? this.getPinnedOffset() : null

      this.$element
        .removeClass(Affix.RESET)
        .addClass(affixType)
        .trigger(affixType.replace('affix', 'affixed') + '.bs.affix')
    }

    if (affix == 'bottom') {
      this.$element.offset({
        top: scrollHeight - height - offsetBottom
      })
    }
  }


  // AFFIX PLUGIN DEFINITION
  // =======================

  function Plugin(option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.affix')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.affix', (data = new Affix(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  var old = $.fn.affix

  $.fn.affix             = Plugin
  $.fn.affix.Constructor = Affix


  // AFFIX NO CONFLICT
  // =================

  $.fn.affix.noConflict = function () {
    $.fn.affix = old
    return this
  }


  // AFFIX DATA-API
  // ==============

  $(window).on('load', function () {
    $('[data-spy="affix"]').each(function () {
      var $spy = $(this)
      var data = $spy.data()

      data.offset = data.offset || {}

      if (data.offsetBottom != null) data.offset.bottom = data.offsetBottom
      if (data.offsetTop    != null) data.offset.top    = data.offsetTop

      Plugin.call($spy, data)
    })
  })

}(jQuery);

/**
 * jQuery.marquee - scrolling text like old marquee element
 * @author Aamir Afridi - aamirafridi(at)gmail(dot)com / http://aamirafridi.com/jquery/jquery-marquee-plugin
 */
;
(function ($) {
    $.fn.marquee = function (options) {
        return this.each(function () {
            // Extend the options if any provided
            var o = $.extend({}, $.fn.marquee.defaults, options),
                $this = $(this),
                $marqueeWrapper, containerWidth, animationCss, verticalDir, elWidth, loopCount = 3,
                playState = 'animation-play-state',
                css3AnimationIsSupported = false,

                //Private methods
                _prefixedEvent = function (element, type, callback) {
                    var pfx = ["webkit", "moz", "MS", "o", ""];
                    for (var p = 0; p < pfx.length; p++) {
                        if (!pfx[p]) type = type.toLowerCase();
                        element.addEventListener(pfx[p] + type, callback, false);
                    }
                },

                _objToString = function (obj) {
                    var tabjson = [];
                    for (var p in obj) {
                        if (obj.hasOwnProperty(p)) {
                            tabjson.push(p + ':' + obj[p]);
                        }
                    }
                    tabjson.push();
                    return '{' + tabjson.join(',') + '}';
                },

                _startAnimationWithDelay = function () {
                    $this.timer = setTimeout(animate, o.delayBeforeStart);
                },

                //Public methods
                methods = {
                    pause: function () {
                        if (css3AnimationIsSupported && o.allowCss3Support) {
                            $marqueeWrapper.css(playState, 'paused');
                        } else {
                            //pause using pause plugin
                            if ($.fn.pause) {
                                $marqueeWrapper.pause();
                            }
                        }
                        //save the status
                        $this.data('runningStatus', 'paused');
                        //fire event
                        $this.trigger('paused');
                    },

                    resume: function () {
                        //resume using css3
                        if (css3AnimationIsSupported && o.allowCss3Support) {
                            $marqueeWrapper.css(playState, 'running');
                        } else {
                            //resume using pause plugin
                            if ($.fn.resume) {
                                $marqueeWrapper.resume();
                            }
                        }
                        //save the status
                        $this.data('runningStatus', 'resumed');
                        //fire event
                        $this.trigger('resumed');
                    },

                    toggle: function () {
                        methods[$this.data('runningStatus') == 'resumed' ? 'pause' : 'resume']();
                    },

                    destroy: function () {
                        //Clear timer
                        clearTimeout($this.timer);
                        //Just unwrap the elements that has been added using this plugin
                        $this.css('visibility', 'hidden').html($this.find('.js-marquee:first'));
                        //This is to prevent the sudden blink
                        setTimeout(function () {
                            $this.css('visibility', 'visible');
                        }, 0);
                    }
                };

            //Check for methods
            if (typeof options === 'string') {
                if ($.isFunction(methods[options])) {
                    //Following two IF statements to support public methods
                    if (!$marqueeWrapper) {
                        $marqueeWrapper = $this.find('.js-marquee-wrapper');
                    }
                    if ($this.data('css3AnimationIsSupported') === true) {
                        css3AnimationIsSupported = true;
                    }
                    methods[options]();
                }
                return;
            }

/* Check if element has data attributes. They have top priority
               For details https://twitter.com/aamirafridi/status/403848044069679104 - Can't find a better solution :/
               jQuery 1.3.2 doesn't support $.data().KEY hence writting the following */
            var dataAttributes = {},
                attr;
            $.each(o, function (key, value) {
                //Check if element has this data attribute
                attr = $this.attr('data-' + key);
                if (typeof attr !== 'undefined') {
                    //Now check if value is boolean or not
                    switch (attr) {
                    case 'true':
                        attr = true;
                        break;
                    case 'false':
                        attr = false;
                        break;
                    }
                    o[key] = attr;
                }
            });

            //since speed option is changed to duration, to support speed for those who are already using it
            o.duration = o.speed || o.duration;

            //Shortcut to see if direction is upward or downward
            verticalDir = o.direction == 'up' || o.direction == 'down';

            //no gap if not duplicated
            o.gap = o.duplicated ? o.gap : 0;

            //wrap inner content into a div
            $this.wrapInner('<div class="js-marquee"></div>');

            //Make copy of the element
            var $el = $this.find('.js-marquee').css({
                'margin-right': o.gap,
                'float': 'left'
            });

            if (o.duplicated) {
                $el.clone(true).appendTo($this);
            }

            //wrap both inner elements into one div
            $this.wrapInner('<div style="width:100000px" class="js-marquee-wrapper"></div>');

            //Save the reference of the wrapper
            $marqueeWrapper = $this.find('.js-marquee-wrapper');

            //If direction is up or down, get the height of main element
            if (verticalDir) {
                var containerHeight = $this.height();
                $marqueeWrapper.removeAttr('style');
                $this.height(containerHeight);

                //Change the CSS for js-marquee element
                $this.find('.js-marquee').css({
                    'float': 'none',
                    'margin-bottom': o.gap,
                    'margin-right': 0
                });

                //Remove bottom margin from 2nd element if duplicated
                if (o.duplicated) $this.find('.js-marquee:last').css({
                    'margin-bottom': 0
                });

                var elHeight = $this.find('.js-marquee:first').height() + o.gap;

                // adjust the animation speed according to the text length
                // formula is to: (Height of the text node / Height of the main container) * speed;
                o.duration = ((parseInt(elHeight, 10) + parseInt(containerHeight, 10)) / parseInt(containerHeight, 10)) * o.duration;

            } else {
                //Save the width of the each element so we can use it in animation
                elWidth = $this.find('.js-marquee:first').width() + o.gap;

                //container width
                containerWidth = $this.width();

                // adjust the animation speed according to the text length
                // formula is to: (Width of the text node / Width of the main container) * speed;
                o.duration = ((parseInt(elWidth, 10) + parseInt(containerWidth, 10)) / parseInt(containerWidth, 10)) * o.duration;
            }

            //if duplicated than reduce the speed
            if (o.duplicated) {
                o.duration = o.duration / 2;
            }

            if (o.allowCss3Support) {
                var
                elm = document.body || document.createElement('div'),
                    animationName = 'marqueeAnimation-' + Math.floor(Math.random() * 10000000),
                    domPrefixes = 'Webkit Moz O ms Khtml'.split(' '),
                    animationString = 'animation',
                    animationCss3Str = '',
                    keyframeString = '';

                //Check css3 support
                if (elm.style.animation) {
                    keyframeString = '@keyframes ' + animationName + ' ';
                    css3AnimationIsSupported = true;
                }

                if (css3AnimationIsSupported === false) {
                    for (var i = 0; i < domPrefixes.length; i++) {
                        if (elm.style[domPrefixes[i] + 'AnimationName'] !== undefined) {
                            var prefix = '-' + domPrefixes[i].toLowerCase() + '-';
                            animationString = prefix + animationString;
                            playState = prefix + playState;
                            keyframeString = '@' + prefix + 'keyframes ' + animationName + ' ';
                            css3AnimationIsSupported = true;
                            break;
                        }
                    }
                }

                if (css3AnimationIsSupported) {
                    animationCss3Str = animationName + ' ' + o.duration / 1000 + 's ' + o.delayBeforeStart / 1000 + 's infinite ' + o.css3easing;
                    $this.data('css3AnimationIsSupported', true);
                }
            }

            var _rePositionVertically = function () {
                    $marqueeWrapper.css('margin-top', o.direction == 'up' ? containerHeight + 'px' : '-' + elHeight + 'px');
                },
                _rePositionHorizontally = function () {
                    $marqueeWrapper.css('margin-left', o.direction == 'left' ? containerWidth + 'px' : '-' + elWidth + 'px');
                };

            //if duplicated option is set to true than position the wrapper
            if (o.duplicated) {
                if (verticalDir) {
                    $marqueeWrapper.css('margin-top', o.direction == 'up' ? containerHeight : '-' + ((elHeight * 2) - o.gap) + 'px');
                } else {
                    $marqueeWrapper.css('margin-left', o.direction == 'left' ? containerWidth + 'px' : '-' + ((elWidth * 2) - o.gap) + 'px');
                }
                loopCount = 1;
            } else {
                if (verticalDir) {
                    _rePositionVertically();
                } else {
                    _rePositionHorizontally();
                }
            }

            //Animate recursive method
            var animate = function () {
                    if (o.duplicated) {
                        //When duplicated, the first loop will be scroll longer so double the duration
                        if (loopCount === 1) {
                            o._originalDuration = o.duration;
                            if (verticalDir) {
                                o.duration = o.direction == 'up' ? o.duration + (containerHeight / ((elHeight) / o.duration)) : o.duration * 2;
                            } else {
                                o.duration = o.direction == 'left' ? o.duration + (containerWidth / ((elWidth) / o.duration)) : o.duration * 2;
                            }
                            //Adjust the css3 animation as well
                            if (animationCss3Str) {
                                animationCss3Str = animationName + ' ' + o.duration / 1000 + 's ' + o.delayBeforeStart / 1000 + 's ' + o.css3easing;
                            }
                            loopCount++;
                        }
                        //On 2nd loop things back to normal, normal duration for the rest of animations
                        else if (loopCount === 2) {
                            o.duration = o._originalDuration;
                            //Adjust the css3 animation as well
                            if (animationCss3Str) {
                                animationName = animationName + '0';
                                keyframeString = $.trim(keyframeString) + '0 ';
                                animationCss3Str = animationName + ' ' + o.duration / 1000 + 's 0s infinite ' + o.css3easing;
                            }
                            loopCount++;
                        }
                    }

                    if (verticalDir) {
                        if (o.duplicated) {

                            //Adjust the starting point of animation only when first loops finishes
                            if (loopCount > 2) {
                                $marqueeWrapper.css('margin-top', o.direction == 'up' ? 0 : '-' + elHeight + 'px');
                            }

                            animationCss = {
                                'margin-top': o.direction == 'up' ? '-' + elHeight + 'px' : 0
                            };
                        } else {
                            _rePositionVertically();
                            animationCss = {
                                'margin-top': o.direction == 'up' ? '-' + ($marqueeWrapper.height()) + 'px' : containerHeight + 'px'
                            };
                        }
                    } else {
                        if (o.duplicated) {

                            //Adjust the starting point of animation only when first loops finishes
                            if (loopCount > 2) {
                                $marqueeWrapper.css('margin-left', o.direction == 'left' ? 0 : '-' + elWidth + 'px');
                            }

                            animationCss = {
                                'margin-left': o.direction == 'left' ? '-' + elWidth + 'px' : 0
                            };

                        } else {
                            _rePositionHorizontally();
                            animationCss = {
                                'margin-left': o.direction == 'left' ? '-' + elWidth + 'px' : containerWidth + 'px'
                            };
                        }
                    }

                    //fire event
                    $this.trigger('beforeStarting');

                    //If css3 support is available than do it with css3, otherwise use jQuery as fallback
                    if (css3AnimationIsSupported) {
                        //Add css3 animation to the element
                        $marqueeWrapper.css(animationString, animationCss3Str);
                        var keyframeCss = keyframeString + ' { 100%  ' + _objToString(animationCss) + '}',
                            $styles = $('style');

                        //Now add the keyframe animation to the head
                        if ($styles.length !== 0) {
                            //Bug fixed for jQuery 1.3.x - Instead of using .last(), use following
                            $styles.filter(":last").append(keyframeCss);
                        } else {
                            $('head').append('<style>' + keyframeCss + '</style>');
                        }

                        //Animation iteration event
                        _prefixedEvent($marqueeWrapper[0], "AnimationIteration", function () {
                            $this.trigger('finished');
                        });
                        //Animation stopped
                        _prefixedEvent($marqueeWrapper[0], "AnimationEnd", function () {
                            animate();
                            $this.trigger('finished');
                        });

                    } else {
                        //Start animating
                        $marqueeWrapper.animate(animationCss, o.duration, o.easing, function () {
                            //fire event
                            $this.trigger('finished');
                            //animate again
                            if (o.pauseOnCycle) {
                                _startAnimationWithDelay();
                            } else {
                                animate();
                            }
                        });
                    }
                    //save the status
                    $this.data('runningStatus', 'resumed');
                };

            //bind pause and resume events
            $this.bind('pause', methods.pause);
            $this.bind('resume', methods.resume);

            if (o.pauseOnHover) {
                $this.bind('mouseenter mouseleave', methods.toggle);
            }

            //If css3 animation is supported than call animate method at once
            if (css3AnimationIsSupported && o.allowCss3Support) {
                animate();
            } else {
                //Starts the recursive method
                _startAnimationWithDelay();
            }

        });
    }; //End of Plugin
    // Public: plugin defaults options
    $.fn.marquee.defaults = {
        //If you wish to always animate using jQuery
        allowCss3Support: true,
        //works when allowCss3Support is set to true - for full list see http://www.w3.org/TR/2013/WD-css3-transitions-20131119/#transition-timing-function
        css3easing: 'linear',
        //requires jQuery easing plugin. Default is 'linear'
        easing: 'linear',
        //pause time before the next animation turn in milliseconds
        delayBeforeStart: 1000,
        //'left', 'right', 'up' or 'down'
        direction: 'left',
        //true or false - should the marquee be duplicated to show an effect of continues flow
        duplicated: false,
        //speed in milliseconds of the marquee in milliseconds
        duration: 5000,
        //gap in pixels between the tickers
        gap: 20,
        //on cycle pause the marquee
        pauseOnCycle: false,
        //on hover pause the marquee - using jQuery plugin https://github.com/tobia/Pause
        pauseOnHover: false
    };
})(jQuery);

function MediumEditor(elements, options) {
    'use strict';
    return this.init(elements, options);
}

if (typeof module === 'object') {
    module.exports = MediumEditor;
}

(function (window, document) {
    'use strict';

    function extend(b, a) {
        var prop;
        if (b === undefined) {
            return a;
        }
        for (prop in a) {
            if (a.hasOwnProperty(prop) && b.hasOwnProperty(prop) === false) {
                b[prop] = a[prop];
            }
        }
        return b;
    }

    function isDescendant(parent, child) {
         var node = child.parentNode;
         while (node !== null) {
             if (node === parent) {
                 return true;
             }
             node = node.parentNode;
         }
         return false;
    }

    // http://stackoverflow.com/questions/5605401/insert-link-in-contenteditable-element
    // by Tim Down
    function saveSelection() {
        var i,
            len,
            ranges,
            sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            ranges = [];
            for (i = 0, len = sel.rangeCount; i < len; i += 1) {
                ranges.push(sel.getRangeAt(i));
            }
            return ranges;
        }
        return null;
    }

    function restoreSelection(savedSel) {
        var i,
            len,
            sel = window.getSelection();
        if (savedSel) {
            sel.removeAllRanges();
            for (i = 0, len = savedSel.length; i < len; i += 1) {
                sel.addRange(savedSel[i]);
            }
        }
    }

    // http://stackoverflow.com/questions/1197401/how-can-i-get-the-element-the-caret-is-in-with-javascript-when-using-contentedi
    // by You
    function getSelectionStart() {
        var node = document.getSelection().anchorNode,
            startNode = (node && node.nodeType === 3 ? node.parentNode : node);
        return startNode;
    }

    // http://stackoverflow.com/questions/4176923/html-of-selected-text
    // by Tim Down
    function getSelectionHtml() {
        var i,
            html = '',
            sel,
            len,
            container;
        if (window.getSelection !== undefined) {
            sel = window.getSelection();
            if (sel.rangeCount) {
                container = document.createElement('div');
                for (i = 0, len = sel.rangeCount; i < len; i += 1) {
                    container.appendChild(sel.getRangeAt(i).cloneContents());
                }
                html = container.innerHTML;
            }
        } else if (document.selection !== undefined) {
            if (document.selection.type === 'Text') {
                html = document.selection.createRange().htmlText;
            }
        }
        return html;
    }

    // https://github.com/jashkenas/underscore
    function isElement(obj) {
        return !!(obj && obj.nodeType === 1);
    }

    MediumEditor.prototype = {
        defaults: {
            allowMultiParagraphSelection: true,
            anchorInputPlaceholder: 'Paste or type a link',
            anchorPreviewHideDelay: 500,
            buttons: ['bold', 'italic', 'underline', 'anchor', 'header1', 'header2', 'quote'],
            buttonLabels: false,
            checkLinkFormat: false,
            cleanPastedHTML: false,
            delay: 0,
            diffLeft: 0,
            diffTop: -10,
            disableReturn: false,
            disableDoubleReturn: false,
            disableToolbar: false,
            disableEditing: false,
            elementsContainer: false,
            firstHeader: 'h3',
            forcePlainText: true,
            placeholder: 'Type your text',
            secondHeader: 'h4',
            targetBlank: false,
            anchorTarget: false,
            anchorButton: false,
            anchorButtonClass: 'btn',
            extensions: {},
            activeButtonClass: 'medium-editor-button-active',
            firstButtonClass: 'medium-editor-button-first',
            lastButtonClass: 'medium-editor-button-last'
        },

        // http://stackoverflow.com/questions/17907445/how-to-detect-ie11#comment30165888_17907562
        // by rg89
        isIE: ((navigator.appName === 'Microsoft Internet Explorer') || ((navigator.appName === 'Netscape') && (new RegExp('Trident/.*rv:([0-9]{1,}[.0-9]{0,})').exec(navigator.userAgent) !== null))),

        init: function (elements, options) {
            this.setElementSelection(elements);
            if (this.elements.length === 0) {
                return;
            }
            this.parentElements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre'];
            this.id = document.querySelectorAll('.medium-editor-toolbar').length + 1;
            this.options = extend(options, this.defaults);
            return this.setup();
        },

        setup: function () {
            this.isActive = true;
            this.initElements()
                .bindSelect()
                .bindPaste()
                .setPlaceholders()
                .bindWindowActions()
                .passInstance();
        },

        initElements: function () {
            this.updateElementList();
            var i,
                addToolbar = false;
            for (i = 0; i < this.elements.length; i += 1) {
                if (!this.options.disableEditing && !this.elements[i].getAttribute('data-disable-editing')) {
                    this.elements[i].setAttribute('contentEditable', true);
                }
                if (!this.elements[i].getAttribute('data-placeholder')) {
                    this.elements[i].setAttribute('data-placeholder', this.options.placeholder);
                }
                this.elements[i].setAttribute('data-medium-element', true);
                this.bindParagraphCreation(i).bindReturn(i).bindTab(i);
                if (!this.options.disableToolbar && !this.elements[i].getAttribute('data-disable-toolbar')) {
                    addToolbar = true;
                }
            }
            // Init toolbar
            if (addToolbar) {
                if (!this.options.elementsContainer) {
                    this.options.elementsContainer = document.body;
                }
                this.initToolbar()
                    .bindButtons()
                    .bindAnchorForm()
                    .bindAnchorPreview();
            }
            return this;
        },

        setElementSelection: function (selector) {
            this.elementSelection = selector;
            this.updateElementList();
        },

        updateElementList: function () {
            this.elements = typeof this.elementSelection === 'string' ? document.querySelectorAll(this.elementSelection) : this.elementSelection;
            if (this.elements.nodeType === 1) {
                this.elements = [this.elements];
            }
        },

        serialize: function () {
            var i,
                elementid,
                content = {};
            for (i = 0; i < this.elements.length; i += 1) {
                elementid = (this.elements[i].id !== '') ? this.elements[i].id : 'element-' + i;
                content[elementid] = {
                    value: this.elements[i].innerHTML.trim()
                };
            }
            return content;
        },

        /**
         * Helper function to call a method with a number of parameters on all registered extensions.
         * The function assures that the function exists before calling.
         *
         * @param {string} funcName name of the function to call
         * @param [args] arguments passed into funcName
         */
        callExtensions: function (funcName) {
            if (arguments.length < 1) {
                return;
            }

            var args = Array.prototype.slice.call(arguments, 1),
                ext,
                name;

            for (name in this.options.extensions) {
                if (this.options.extensions.hasOwnProperty(name)) {
                    ext = this.options.extensions[name];
                    if (ext[funcName] !== undefined) {
                        ext[funcName].apply(ext, args);
                    }
                }
            }
        },

        /**
         * Pass current Medium Editor instance to all extensions
         * if extension constructor has 'parent' attribute set to 'true'
         *
         */
        passInstance: function () {
            var self = this,
                ext,
                name;

            for (name in self.options.extensions) {
                if (self.options.extensions.hasOwnProperty(name)) {
                    ext = self.options.extensions[name];

                    if (ext.parent) {
                        ext.base = self;
                    }
                }
            }

            return self;
        },

        bindParagraphCreation: function (index) {
            var self = this;
            this.elements[index].addEventListener('keypress', function (e) {
                var node = getSelectionStart(),
                    tagName;
                if (e.which === 32) {
                    tagName = node.tagName.toLowerCase();
                    if (tagName === 'a') {
                        document.execCommand('unlink', false, null);
                    }
                }
            });

            this.elements[index].addEventListener('keyup', function (e) {
                var node = getSelectionStart(),
                    tagName;
                if (node && node.getAttribute('data-medium-element') && node.children.length === 0 && !(self.options.disableReturn || node.getAttribute('data-disable-return'))) {
                    document.execCommand('formatBlock', false, 'p');
                }
                if (e.which === 13) {
                    node = getSelectionStart();
                    tagName = node.tagName.toLowerCase();
                    if (!(self.options.disableReturn || this.getAttribute('data-disable-return')) &&
                        tagName !== 'li' && !self.isListItemChild(node)) {
                        if (!e.shiftKey) {
                            document.execCommand('formatBlock', false, 'p');
                        }
                        if (tagName === 'a') {
                            document.execCommand('unlink', false, null);
                        }
                    }
                }
            });
            return this;
        },

        isListItemChild: function (node) {
            var parentNode = node.parentNode,
                tagName = parentNode.tagName.toLowerCase();
            while (this.parentElements.indexOf(tagName) === -1 && tagName !== 'div') {
                if (tagName === 'li') {
                    return true;
                }
                parentNode = parentNode.parentNode;
                if (parentNode && parentNode.tagName) {
                    tagName = parentNode.tagName.toLowerCase();
                } else {
                    return false;
                }
            }
            return false;
        },

        bindReturn: function (index) {
            var self = this;
            this.elements[index].addEventListener('keypress', function (e) {
                if (e.which === 13) {
                    if (self.options.disableReturn || this.getAttribute('data-disable-return')) {
                        e.preventDefault();
                    } else if (self.options.disableDoubleReturn || this.getAttribute('data-disable-double-return')) {
                        var node = getSelectionStart();
                        if (node && node.innerText === '\n') {
                            e.preventDefault();
                        }
                    }
                }
            });
            return this;
        },

        bindTab: function (index) {
            this.elements[index].addEventListener('keydown', function (e) {
                if (e.which === 9) {
                    // Override tab only for pre nodes
                    var tag = getSelectionStart().tagName.toLowerCase();
                    if (tag === 'pre') {
                        e.preventDefault();
                        document.execCommand('insertHtml', null, '    ');
                    }

                    // Tab to indent list structures!
                    if (tag === 'li') {
                        e.preventDefault();

                        // If Shift is down, outdent, otherwise indent
                        if (e.shiftKey) {
                            document.execCommand('outdent', e);
                        } else {
                            document.execCommand('indent', e);
                        }
                    }
                }
            });
            return this;
        },

        buttonTemplate: function (btnType) {
            var buttonLabels = this.getButtonLabels(this.options.buttonLabels),
                buttonTemplates = {
                    'bold': '<button class="medium-editor-action medium-editor-action-bold" data-action="bold" data-element="b">' + buttonLabels.bold + '</button>',
                    'italic': '<button class="medium-editor-action medium-editor-action-italic" data-action="italic" data-element="i">' + buttonLabels.italic + '</button>',
                    'underline': '<button class="medium-editor-action medium-editor-action-underline" data-action="underline" data-element="u">' + buttonLabels.underline + '</button>',
                    'strikethrough': '<button class="medium-editor-action medium-editor-action-strikethrough" data-action="strikethrough" data-element="strike"><strike>A</strike></button>',
                    'superscript': '<button class="medium-editor-action medium-editor-action-superscript" data-action="superscript" data-element="sup">' + buttonLabels.superscript + '</button>',
                    'subscript': '<button class="medium-editor-action medium-editor-action-subscript" data-action="subscript" data-element="sub">' + buttonLabels.subscript + '</button>',
                    'anchor': '<button class="medium-editor-action medium-editor-action-anchor" data-action="anchor" data-element="a">' + buttonLabels.anchor + '</button>',
                    'image': '<button class="medium-editor-action medium-editor-action-image" data-action="image" data-element="img">' + buttonLabels.image + '</button>',
                    'header1': '<button class="medium-editor-action medium-editor-action-header1" data-action="append-' + this.options.firstHeader + '" data-element="' + this.options.firstHeader + '">' + buttonLabels.header1 + '</button>',
                    'header2': '<button class="medium-editor-action medium-editor-action-header2" data-action="append-' + this.options.secondHeader + '" data-element="' + this.options.secondHeader + '">' + buttonLabels.header2 + '</button>',
                    'quote': '<button class="medium-editor-action medium-editor-action-quote" data-action="append-blockquote" data-element="blockquote">' + buttonLabels.quote + '</button>',
                    'orderedlist': '<button class="medium-editor-action medium-editor-action-orderedlist" data-action="insertorderedlist" data-element="ol">' + buttonLabels.orderedlist + '</button>',
                    'unorderedlist': '<button class="medium-editor-action medium-editor-action-unorderedlist" data-action="insertunorderedlist" data-element="ul">' + buttonLabels.unorderedlist + '</button>',
                    'pre': '<button class="medium-editor-action medium-editor-action-pre" data-action="append-pre" data-element="pre">' + buttonLabels.pre + '</button>',
                    'indent': '<button class="medium-editor-action medium-editor-action-indent" data-action="indent" data-element="ul">' + buttonLabels.indent + '</button>',
                    'outdent': '<button class="medium-editor-action medium-editor-action-outdent" data-action="outdent" data-element="ul">' + buttonLabels.outdent + '</button>'
                };
            return buttonTemplates[btnType] || false;
        },

        // TODO: break method
        getButtonLabels: function (buttonLabelType) {
            var customButtonLabels,
                attrname,
                buttonLabels = {
                    'bold': '<b>B</b>',
                    'italic': '<b><i>I</i></b>',
                    'underline': '<b><u>U</u></b>',
                    'superscript': '<b>x<sup>1</sup></b>',
                    'subscript': '<b>x<sub>1</sub></b>',
                    'anchor': '<b>#</b>',
                    'image': '<b>image</b>',
                    'header1': '<b>H1</b>',
                    'header2': '<b>H2</b>',
                    'quote': '<b>&ldquo;</b>',
                    'orderedlist': '<b>1.</b>',
                    'unorderedlist': '<b>&bull;</b>',
                    'pre': '<b>0101</b>',
                    'indent': '<b>&rarr;</b>',
                    'outdent': '<b>&larr;</b>'
                };
            if (buttonLabelType === 'fontawesome') {
                customButtonLabels = {
                    'bold': '<i class="fa fa-bold"></i>',
                    'italic': '<i class="fa fa-italic"></i>',
                    'underline': '<i class="fa fa-underline"></i>',
                    'superscript': '<i class="fa fa-superscript"></i>',
                    'subscript': '<i class="fa fa-subscript"></i>',
                    'anchor': '<i class="fa fa-link"></i>',
                    'image': '<i class="fa fa-picture-o"></i>',
                    'quote': '<i class="fa fa-quote-right"></i>',
                    'orderedlist': '<i class="fa fa-list-ol"></i>',
                    'unorderedlist': '<i class="fa fa-list-ul"></i>',
                    'pre': '<i class="fa fa-code fa-lg"></i>',
                    'indent': '<i class="fa fa-indent"></i>',
                    'outdent': '<i class="fa fa-outdent"></i>'
                };
            } else if (typeof buttonLabelType === 'object') {
                customButtonLabels = buttonLabelType;
            }
            if (typeof customButtonLabels === 'object') {
                for (attrname in customButtonLabels) {
                    if (customButtonLabels.hasOwnProperty(attrname)) {
                        buttonLabels[attrname] = customButtonLabels[attrname];
                    }
                }
            }
            return buttonLabels;
        },

        initToolbar: function () {
            if (this.toolbar) {
                return this;
            }
            this.toolbar = this.createToolbar();
            this.keepToolbarAlive = false;
            this.anchorForm = this.toolbar.querySelector('.medium-editor-toolbar-form-anchor');
            this.anchorInput = this.anchorForm.querySelector('input.medium-editor-toolbar-anchor-input');
            this.anchorTarget = this.anchorForm.querySelector('input.medium-editor-toolbar-anchor-target');
            this.anchorButton = this.anchorForm.querySelector('input.medium-editor-toolbar-anchor-button');
            this.toolbarActions = this.toolbar.querySelector('.medium-editor-toolbar-actions');
            this.anchorPreview = this.createAnchorPreview();

            return this;
        },

        createToolbar: function () {
            var toolbar = document.createElement('div');
            toolbar.id = 'medium-editor-toolbar-' + this.id;
            toolbar.className = 'medium-editor-toolbar';
            toolbar.appendChild(this.toolbarButtons());
            toolbar.appendChild(this.toolbarFormAnchor());
            this.options.elementsContainer.appendChild(toolbar);
            return toolbar;
        },

        //TODO: actionTemplate
        toolbarButtons: function () {
            var btns = this.options.buttons,
                ul = document.createElement('ul'),
                li,
                i,
                btn,
                ext;

            ul.id = 'medium-editor-toolbar-actions';
            ul.className = 'medium-editor-toolbar-actions clearfix';

            for (i = 0; i < btns.length; i += 1) {
                if (this.options.extensions.hasOwnProperty(btns[i])) {
                    ext = this.options.extensions[btns[i]];
                    btn = ext.getButton !== undefined ? ext.getButton() : null;
                } else {
                    btn = this.buttonTemplate(btns[i]);
                }

                if (btn) {
                    li = document.createElement('li');
                    if (isElement(btn)) {
                        li.appendChild(btn);
                    } else {
                        li.innerHTML = btn;
                    }
                    ul.appendChild(li);
                }
            }

            return ul;
        },

        toolbarFormAnchor: function () {
            var anchor = document.createElement('div'),
                input = document.createElement('input'),
                target_label = document.createElement('label'),
                target = document.createElement('input'),
                button_label = document.createElement('label'),
                button = document.createElement('input'),
                close = document.createElement('a'),
                save = document.createElement('a');

            close.setAttribute('href', '#');
            close.className = 'medium-editor-toobar-anchor-close';
            close.innerHTML = '&times;';

            save.setAttribute('href', '#');
            save.className = 'medium-editor-toobar-anchor-save';
            save.innerHTML = '&#10003;';

            input.setAttribute('type', 'text');
            input.className = 'medium-editor-toolbar-anchor-input';
            input.setAttribute('placeholder', this.options.anchorInputPlaceholder);


            target.setAttribute('type', 'checkbox');
            target.className = 'medium-editor-toolbar-anchor-target';
            target_label.innerHTML = "Open in New Window?";
            target_label.insertBefore(target, target_label.firstChild);

            button.setAttribute('type', 'checkbox');
            button.className = 'medium-editor-toolbar-anchor-button';
            button_label.innerHTML = "Button";
            button_label.insertBefore(button, button_label.firstChild);


            anchor.className = 'medium-editor-toolbar-form-anchor';
            anchor.id = 'medium-editor-toolbar-form-anchor';
            anchor.appendChild(input);

            anchor.appendChild(save);
            anchor.appendChild(close);

            if (this.options.anchorTarget) {
                anchor.appendChild(target_label);
            }

            if (this.options.anchorButton) {
                anchor.appendChild(button_label);
            }

            return anchor;
        },

        bindSelect: function () {
            var self = this,
                timer = '',
                i;

            this.checkSelectionWrapper = function (e) {

                // Do not close the toolbar when bluring the editable area and clicking into the anchor form
                if (e && self.clickingIntoArchorForm(e)) {
                    return false;
                }

                clearTimeout(timer);
                timer = setTimeout(function () {
                    self.checkSelection();
                }, self.options.delay);
            };

            document.documentElement.addEventListener('mouseup', this.checkSelectionWrapper);

            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].addEventListener('keyup', this.checkSelectionWrapper);
                this.elements[i].addEventListener('blur', this.checkSelectionWrapper);
            }
            return this;
        },

        checkSelection: function () {
            var newSelection,
                selectionElement;

            if (this.keepToolbarAlive !== true && !this.options.disableToolbar) {

                newSelection = window.getSelection();
                if (newSelection.toString().trim() === '' ||
                    (this.options.allowMultiParagraphSelection === false && this.hasMultiParagraphs()) ||
                    this.selectionInContentEditableFalse()) {
                    this.hideToolbarActions();
                } else {
                    selectionElement = this.getSelectionElement();
                    if (!selectionElement || selectionElement.getAttribute('data-disable-toolbar')) {
                        this.hideToolbarActions();
                    } else {
                        this.checkSelectionElement(newSelection, selectionElement);
                    }
                }
            }
            return this;
        },

        clickingIntoArchorForm: function (e) {
            var self = this;

            if (e.type && e.type.toLowerCase() === 'blur' && e.relatedTarget && e.relatedTarget === self.anchorInput) {
                return true;
            }

            return false;
        },

        hasMultiParagraphs: function () {
            var selectionHtml = getSelectionHtml().replace(/<[\S]+><\/[\S]+>/gim, ''),
                hasMultiParagraphs = selectionHtml.match(/<(p|h[0-6]|blockquote)>([\s\S]*?)<\/(p|h[0-6]|blockquote)>/g);

            return (hasMultiParagraphs ? hasMultiParagraphs.length : 0);
        },

        checkSelectionElement: function (newSelection, selectionElement) {
            var i;
            this.selection = newSelection;
            this.selectionRange = this.selection.getRangeAt(0);
            for (i = 0; i < this.elements.length; i += 1) {
                if (this.elements[i] === selectionElement) {
                    this.setToolbarButtonStates()
                        .setToolbarPosition()
                        .showToolbarActions();
                    return;
                }
            }
            this.hideToolbarActions();
        },

        findMatchingSelectionParent: function(testElementFunction) {
            var selection = window.getSelection(),
                range, current, parent,
                result,
                getElement = function (e) {
                    var localParent = e;
                    try {
                        while (!testElementFunction(localParent)) {
                            localParent = localParent.parentNode;
                        }
                    } catch (errb) {
                        return false;
                    }
                    return localParent;
                };
            // First try on current node
            try {
                range = selection.getRangeAt(0);
                current = range.commonAncestorContainer;
                parent = current.parentNode;

                if (testElementFunction(current)) {
                    result = current;
                } else {
                    result = getElement(parent);
                }
                // If not search in the parent nodes.
            } catch (err) {
                result = getElement(parent);
            }
            return result;
        },

        getSelectionElement: function () {
            return this.findMatchingSelectionParent(function(el) {
                return el.getAttribute('data-medium-element');
            });
        },

        selectionInContentEditableFalse: function () {
            return this.findMatchingSelectionParent(function(el) {
                return (el && el.nodeName !== '#text' && el.getAttribute('contenteditable') === 'false');
            });
        },

        setToolbarPosition: function () {
            var buttonHeight = 50,
                selection = window.getSelection(),
                range = selection.getRangeAt(0),
                boundary = range.getBoundingClientRect(),
                defaultLeft = (this.options.diffLeft) - (this.toolbar.offsetWidth / 2),
                middleBoundary = (boundary.left + boundary.right) / 2,
                halfOffsetWidth = this.toolbar.offsetWidth / 2;
            if (boundary.top < buttonHeight) {
                this.toolbar.classList.add('medium-toolbar-arrow-over');
                this.toolbar.classList.remove('medium-toolbar-arrow-under');
                this.toolbar.style.top = buttonHeight + boundary.bottom - this.options.diffTop + window.pageYOffset - this.toolbar.offsetHeight + 'px';
            } else {
                this.toolbar.classList.add('medium-toolbar-arrow-under');
                this.toolbar.classList.remove('medium-toolbar-arrow-over');
                this.toolbar.style.top = boundary.top + this.options.diffTop + window.pageYOffset - this.toolbar.offsetHeight + 'px';
            }
            if (middleBoundary < halfOffsetWidth) {
                this.toolbar.style.left = defaultLeft + halfOffsetWidth + 'px';
            } else if ((window.innerWidth - middleBoundary) < halfOffsetWidth) {
                this.toolbar.style.left = window.innerWidth + defaultLeft - halfOffsetWidth + 'px';
            } else {
                this.toolbar.style.left = defaultLeft + middleBoundary + 'px';
            }

            this.hideAnchorPreview();

            return this;
        },

        setToolbarButtonStates: function () {
            var buttons = this.toolbarActions.querySelectorAll('button'),
                i;
            for (i = 0; i < buttons.length; i += 1) {
                buttons[i].classList.remove(this.options.activeButtonClass);
            }
            this.checkActiveButtons();
            return this;
        },

        checkActiveButtons: function () {
            var elements = Array.prototype.slice.call(this.elements),
                parentNode = this.getSelectedParentElement();
            while (parentNode.tagName !== undefined && this.parentElements.indexOf(parentNode.tagName.toLowerCase) === -1) {
                this.activateButton(parentNode.tagName.toLowerCase());
                this.callExtensions('checkState', parentNode);

                // we can abort the search upwards if we leave the contentEditable element
                if (elements.indexOf(parentNode) !== -1) {
                    break;
                }
                parentNode = parentNode.parentNode;
            }
        },

        activateButton: function (tag) {
            var el = this.toolbar.querySelector('[data-element="' + tag + '"]');
            if (el !== null && el.className.indexOf(this.options.activeButtonClass) === -1) {
                el.className += ' ' + this.options.activeButtonClass;
            }
        },

        bindButtons: function () {
            var buttons = this.toolbar.querySelectorAll('button'),
                i,
                self = this,
                triggerAction = function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    if (self.selection === undefined) {
                        self.checkSelection();
                    }
                    if (this.className.indexOf(self.options.activeButtonClass) > -1) {
                        this.classList.remove(self.options.activeButtonClass);
                    } else {
                        this.className += ' ' + self.options.activeButtonClass;
                    }
                    if (this.hasAttribute('data-action')) {
                        self.execAction(this.getAttribute('data-action'), e);
                    }
                };
            for (i = 0; i < buttons.length; i += 1) {
                buttons[i].addEventListener('click', triggerAction);
            }
            this.setFirstAndLastItems(buttons);
            return this;
        },

        setFirstAndLastItems: function (buttons) {
            if (buttons.length > 0) {
                buttons[0].className += ' ' + this.options.firstButtonClass;
                buttons[buttons.length - 1].className += ' ' + this.options.lastButtonClass;
            }
            return this;
        },

        execAction: function (action, e) {
            if (action.indexOf('append-') > -1) {
                this.execFormatBlock(action.replace('append-', ''));
                this.setToolbarPosition();
                this.setToolbarButtonStates();
            } else if (action === 'anchor') {
                this.triggerAnchorAction(e);
            } else if (action === 'image') {
                document.execCommand('insertImage', false, window.getSelection());
            } else {
                document.execCommand(action, false, null);
                this.setToolbarPosition();
            }
        },

        // http://stackoverflow.com/questions/15867542/range-object-get-selection-parent-node-chrome-vs-firefox
        rangeSelectsSingleNode: function (range) {
            var startNode = range.startContainer;
            return startNode === range.endContainer &&
                startNode.hasChildNodes() &&
                range.endOffset === range.startOffset + 1;
        },

        getSelectedParentElement: function () {
            var selectedParentElement = null,
                range = this.selectionRange;
            if (this.rangeSelectsSingleNode(range)) {
                selectedParentElement = range.startContainer.childNodes[range.startOffset];
            } else if (range.startContainer.nodeType === 3) {
                selectedParentElement = range.startContainer.parentNode;
            } else {
                selectedParentElement = range.startContainer;
            }
            return selectedParentElement;
        },

        triggerAnchorAction: function () {
            var selectedParentElement = this.getSelectedParentElement();
            if (selectedParentElement.tagName &&
                    selectedParentElement.tagName.toLowerCase() === 'a') {
                document.execCommand('unlink', false, null);
            } else {
                if (this.anchorForm.style.display === 'block') {
                    this.showToolbarActions();
                } else {
                    this.showAnchorForm();
                }
            }
            return this;
        },

        execFormatBlock: function (el) {
            var selectionData = this.getSelectionData(this.selection.anchorNode);
            // FF handles blockquote differently on formatBlock
            // allowing nesting, we need to use outdent
            // https://developer.mozilla.org/en-US/docs/Rich-Text_Editing_in_Mozilla
            if (el === 'blockquote' && selectionData.el &&
                selectionData.el.parentNode.tagName.toLowerCase() === 'blockquote') {
                return document.execCommand('outdent', false, null);
            }
            if (selectionData.tagName === el) {
                el = 'p';
            }
            // When IE we need to add <> to heading elements and
            //  blockquote needs to be called as indent
            // http://stackoverflow.com/questions/10741831/execcommand-formatblock-headings-in-ie
            // http://stackoverflow.com/questions/1816223/rich-text-editor-with-blockquote-function/1821777#1821777
            if (this.isIE) {
                if (el === 'blockquote') {
                    return document.execCommand('indent', false, el);
                }
                el = '<' + el + '>';
            }
            return document.execCommand('formatBlock', false, el);
        },

        getSelectionData: function (el) {
            var tagName;

            if (el && el.tagName) {
                tagName = el.tagName.toLowerCase();
            }

            while (el && this.parentElements.indexOf(tagName) === -1) {
                el = el.parentNode;
                if (el && el.tagName) {
                    tagName = el.tagName.toLowerCase();
                }
            }

            return {
                el: el,
                tagName: tagName
            };
        },

        getFirstChild: function (el) {
            var firstChild = el.firstChild;
            while (firstChild !== null && firstChild.nodeType !== 1) {
                firstChild = firstChild.nextSibling;
            }
            return firstChild;
        },

        hideToolbarActions: function () {
            this.keepToolbarAlive = false;
            if (this.toolbar !== undefined) {
                this.toolbar.classList.remove('medium-editor-toolbar-active');
            }
        },

        showToolbarActions: function () {
            var self = this,
                timer;
            this.anchorForm.style.display = 'none';
            this.toolbarActions.style.display = 'block';
            this.keepToolbarAlive = false;
            clearTimeout(timer);
            timer = setTimeout(function () {
                if (self.toolbar && !self.toolbar.classList.contains('medium-editor-toolbar-active')) {
                    self.toolbar.classList.add('medium-editor-toolbar-active');
                }
            }, 100);
        },

        saveSelection: function() {
            this.savedSelection = saveSelection();
        },

        restoreSelection: function() {
            restoreSelection(this.savedSelection);
        },

        showAnchorForm: function (link_value) {
            this.toolbarActions.style.display = 'none';
            this.saveSelection();
            this.anchorForm.style.display = 'block';
            this.setToolbarPosition();
            this.keepToolbarAlive = true;
            this.anchorInput.focus();
            this.anchorInput.value = link_value || '';
        },

        bindAnchorForm: function () {
            var linkCancel = this.anchorForm.querySelector('a.medium-editor-toobar-anchor-close'),
                linkSave = this.anchorForm.querySelector('a.medium-editor-toobar-anchor-save'),
                self = this;

            this.anchorForm.addEventListener('click', function (e) {
                e.stopPropagation();
                self.keepToolbarAlive = true;
            });

            this.anchorInput.addEventListener('keyup', function (e) {
                var button = null,
                    target;

                if (e.keyCode === 13) {
                    e.preventDefault();
                    if (self.options.anchorTarget && self.anchorTarget.checked) {
                        target = "_blank";
                    }
                    else {
                        target = "_self";
                    }

                    if (self.options.anchorButton && self.anchorButton.checked) {
                        button = self.options.anchorButtonClass;
                    }

                    self.createLink(this, target, button);
                }
            });

            linkSave.addEventListener('click', function(e) {
                var button = null,
                    target;
                e.preventDefault();
                if ( self.options.anchorTarget && self.anchorTarget.checked) {
                    target = "_blank";
                }
                else {
                    target = "_self";
                }

                if (self.options.anchorButton && self.anchorButton.checked) {
                    button = self.options.anchorButtonClass;
                }

                self.createLink(self.anchorInput, target, button);
            }, true);

            this.anchorInput.addEventListener('click', function (e) {
                // make sure not to hide form when cliking into the input
                e.stopPropagation();
                self.keepToolbarAlive = true;
            });

            // Hide the anchor form when focusing outside of it.
            document.body.addEventListener('click', function (e) {
                if (e.target !== self.anchorForm && !isDescendant(self.anchorForm, e.target) && !isDescendant(self.toolbarActions, e.target)) {
                    self.keepToolbarAlive = false;
                    self.checkSelection();
                }
            }, true);
            document.body.addEventListener('focus', function (e) {
                if (e.target !== self.anchorForm && !isDescendant(self.anchorForm, e.target) && !isDescendant(self.toolbarActions, e.target)) {
                    self.keepToolbarAlive = false;
                    self.checkSelection();
                }
            }, true);

            linkCancel.addEventListener('click', function (e) {
                e.preventDefault();
                self.showToolbarActions();
                restoreSelection(self.savedSelection);
            });
            return this;
        },


        hideAnchorPreview: function () {
            this.anchorPreview.classList.remove('medium-editor-anchor-preview-active');
        },

        // TODO: break method
        showAnchorPreview: function (anchorEl) {
            if (this.anchorPreview.classList.contains('medium-editor-anchor-preview-active')
                || anchorEl.getAttribute('data-disable-preview')) {
                return true;
            }

            var self = this,
                buttonHeight = 40,
                boundary = anchorEl.getBoundingClientRect(),
                middleBoundary = (boundary.left + boundary.right) / 2,
                halfOffsetWidth,
                defaultLeft,
                timer;

            self.anchorPreview.querySelector('i').textContent = anchorEl.href;
            halfOffsetWidth = self.anchorPreview.offsetWidth / 2;
            defaultLeft = self.options.diffLeft - halfOffsetWidth;

            clearTimeout(timer);
            timer = setTimeout(function () {
                if (self.anchorPreview && !self.anchorPreview.classList.contains('medium-editor-anchor-preview-active')) {
                    self.anchorPreview.classList.add('medium-editor-anchor-preview-active');
                }
            }, 100);

            self.observeAnchorPreview(anchorEl);

            self.anchorPreview.classList.add('medium-toolbar-arrow-over');
            self.anchorPreview.classList.remove('medium-toolbar-arrow-under');
            self.anchorPreview.style.top = Math.round(buttonHeight + boundary.bottom - self.options.diffTop + window.pageYOffset - self.anchorPreview.offsetHeight) + 'px';
            if (middleBoundary < halfOffsetWidth) {
                self.anchorPreview.style.left = defaultLeft + halfOffsetWidth + 'px';
            } else if ((window.innerWidth - middleBoundary) < halfOffsetWidth) {
                self.anchorPreview.style.left = window.innerWidth + defaultLeft - halfOffsetWidth + 'px';
            } else {
                self.anchorPreview.style.left = defaultLeft + middleBoundary + 'px';
            }

            return this;
        },

        // TODO: break method
        observeAnchorPreview: function (anchorEl) {
            var self = this,
                lastOver = (new Date()).getTime(),
                over = true,
                stamp = function () {
                    lastOver = (new Date()).getTime();
                    over = true;
                },
                unstamp = function (e) {
                    if (!e.relatedTarget || !/anchor-preview/.test(e.relatedTarget.className)) {
                        over = false;
                    }
                },
                interval_timer = setInterval(function () {
                    if (over) {
                        return true;
                    }
                    var durr = (new Date()).getTime() - lastOver;
                    if (durr > self.options.anchorPreviewHideDelay) {
                        // hide the preview 1/2 second after mouse leaves the link
                        self.hideAnchorPreview();

                        // cleanup
                        clearInterval(interval_timer);
                        self.anchorPreview.removeEventListener('mouseover', stamp);
                        self.anchorPreview.removeEventListener('mouseout', unstamp);
                        anchorEl.removeEventListener('mouseover', stamp);
                        anchorEl.removeEventListener('mouseout', unstamp);

                    }
                }, 200);

            self.anchorPreview.addEventListener('mouseover', stamp);
            self.anchorPreview.addEventListener('mouseout', unstamp);
            anchorEl.addEventListener('mouseover', stamp);
            anchorEl.addEventListener('mouseout', unstamp);
        },

        createAnchorPreview: function () {
            var self = this,
                anchorPreview = document.createElement('div');

            anchorPreview.id = 'medium-editor-anchor-preview-' + this.id;
            anchorPreview.className = 'medium-editor-anchor-preview';
            anchorPreview.innerHTML = this.anchorPreviewTemplate();
            this.options.elementsContainer.appendChild(anchorPreview);

            anchorPreview.addEventListener('click', function () {
                self.anchorPreviewClickHandler();
            });

            return anchorPreview;
        },

        anchorPreviewTemplate: function () {
            return '<div class="medium-editor-toolbar-anchor-preview" id="medium-editor-toolbar-anchor-preview">' +
                '    <i class="medium-editor-toolbar-anchor-preview-inner"></i>' +
                '</div>';
        },

        anchorPreviewClickHandler: function (e) {
            if (this.activeAnchor) {

                var self = this,
                    range = document.createRange(),
                    sel = window.getSelection();

                range.selectNodeContents(self.activeAnchor);
                sel.removeAllRanges();
                sel.addRange(range);
                setTimeout(function () {
                    if (self.activeAnchor) {
                        self.showAnchorForm(self.activeAnchor.href);
                    }
                    self.keepToolbarAlive = false;
                }, 100 + self.options.delay);

            }

            this.hideAnchorPreview();
        },

        editorAnchorObserver: function (e) {
            var self = this,
                overAnchor = true,
                leaveAnchor = function () {
                    // mark the anchor as no longer hovered, and stop listening
                    overAnchor = false;
                    self.activeAnchor.removeEventListener('mouseout', leaveAnchor);
                };

            if (e.target && e.target.tagName.toLowerCase() === 'a') {

                // Detect empty href attributes
                // The browser will make href="" or href="#top"
                // into absolute urls when accessed as e.targed.href, so check the html
                if (!/href=["']\S+["']/.test(e.target.outerHTML) || /href=["']#\S+["']/.test(e.target.outerHTML)) {
                    return true;
                }

                // only show when hovering on anchors
                if (this.toolbar.classList.contains('medium-editor-toolbar-active')) {
                    // only show when toolbar is not present
                    return true;
                }
                this.activeAnchor = e.target;
                this.activeAnchor.addEventListener('mouseout', leaveAnchor);
                // show the anchor preview according to the configured delay
                // if the mouse has not left the anchor tag in that time
                setTimeout(function () {
                    if (overAnchor) {
                        self.showAnchorPreview(e.target);
                    }
                }, self.options.delay);


            }
        },

        bindAnchorPreview: function (index) {
            var i, self = this;
            this.editorAnchorObserverWrapper = function (e) {
                self.editorAnchorObserver(e);
            };
            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].addEventListener('mouseover', this.editorAnchorObserverWrapper);
            }
            return this;
        },

        checkLinkFormat: function (value) {
            var re = /^(https?|ftps?|rtmpt?):\/\/|mailto:/;
            return (re.test(value) ? '' : 'http://') + value;
        },

        setTargetBlank: function () {
            var el = getSelectionStart(),
                i;
            if (el.tagName.toLowerCase() === 'a') {
                el.target = '_blank';
            } else {
                el = el.getElementsByTagName('a');
                for (i = 0; i < el.length; i += 1) {
                    el[i].target = '_blank';
                }
            }
        },

        setButtonClass: function (buttonClass) {
            var el = getSelectionStart(),
                classes = buttonClass.split(' '),
                i, j;
            if (el.tagName.toLowerCase() === 'a') {
                for (j = 0; j < classes.length; j += 1) {
                    el.classList.add(classes[j]);
                }
            } else {
                el = el.getElementsByTagName('a');
                for (i = 0; i < el.length; i += 1) {
                    for (j = 0; j < classes.length; j += 1) {
                        el[i].classList.add(classes[j]);
                    }
                }
            }
        },

        createLink: function (input, target, buttonClass) {
            var i, event;

            if (input.value.trim().length === 0) {
                this.hideToolbarActions();
                return;
            }

            restoreSelection(this.savedSelection);

            if (this.options.checkLinkFormat) {
                input.value = this.checkLinkFormat(input.value);
            }

            document.execCommand('createLink', false, input.value);

            if (this.options.targetBlank || target === "_blank") {
                this.setTargetBlank();
            }

            if (buttonClass) {
                this.setButtonClass(buttonClass);
            }

            if (this.options.targetBlank || target === "_blank" || buttonClass) {
                event = document.createEvent("HTMLEvents");
                event.initEvent("input", true, true, window);
                for (i = 0; i < this.elements.length; i += 1) {
                    this.elements[i].dispatchEvent(event);
                }
            }

            this.checkSelection();
            this.showToolbarActions();
            input.value = '';
        },

        bindWindowActions: function () {
            var timerResize,
                self = this;
            this.windowResizeHandler = function () {
                clearTimeout(timerResize);
                timerResize = setTimeout(function () {
                    if (self.toolbar && self.toolbar.classList.contains('medium-editor-toolbar-active')) {
                        self.setToolbarPosition();
                    }
                }, 100);
            };
            window.addEventListener('resize', this.windowResizeHandler);
            return this;
        },

        activate: function () {
            if (this.isActive) {
                return;
            }

            this.setup();
        },

        // TODO: break method
        deactivate: function () {
            var i;
            if (!this.isActive) {
                return;
            }
            this.isActive = false;

            if (this.toolbar !== undefined) {
                this.options.elementsContainer.removeChild(this.anchorPreview);
                this.options.elementsContainer.removeChild(this.toolbar);
                delete this.toolbar;
                delete this.anchorPreview;
            }

            document.documentElement.removeEventListener('mouseup', this.checkSelectionWrapper);
            window.removeEventListener('resize', this.windowResizeHandler);

            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].removeEventListener('mouseover', this.editorAnchorObserverWrapper);
                this.elements[i].removeEventListener('keyup', this.checkSelectionWrapper);
                this.elements[i].removeEventListener('blur', this.checkSelectionWrapper);
                this.elements[i].removeEventListener('paste', this.pasteWrapper);
                this.elements[i].removeAttribute('contentEditable');
                this.elements[i].removeAttribute('data-medium-element');
            }

        },

        htmlEntities: function (str) {
            // converts special characters (like <) into their escaped/encoded values (like &lt;).
            // This allows you to show to display the string without the browser reading it as HTML.
            return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
        },

        bindPaste: function () {
            var i, self = this;
            this.pasteWrapper = function (e) {
                var paragraphs,
                    html = '',
                    p;

                this.classList.remove('medium-editor-placeholder');
                if (!self.options.forcePlainText && !self.options.cleanPastedHTML) {
                    return this;
                }

                if (e.clipboardData && e.clipboardData.getData && !e.defaultPrevented) {
                    e.preventDefault();

                    if (self.options.cleanPastedHTML && e.clipboardData.getData('text/html')) {
                        return self.cleanPaste(e.clipboardData.getData('text/html'));
                    }
                    if (!(self.options.disableReturn || this.getAttribute('data-disable-return'))) {
                        paragraphs = e.clipboardData.getData('text/plain').split(/[\r\n]/g);
                        for (p = 0; p < paragraphs.length; p += 1) {
                            if (paragraphs[p] !== '') {
                                if (navigator.userAgent.match(/firefox/i) && p === 0) {
                                    html += self.htmlEntities(paragraphs[p]);
                                } else {
                                    html += '<p>' + self.htmlEntities(paragraphs[p]) + '</p>';
                                }
                            }
                        }
                        document.execCommand('insertHTML', false, html);
                    } else {
                        document.execCommand('insertHTML', false, e.clipboardData.getData('text/plain'));
                    }
                }
            };
            for (i = 0; i < this.elements.length; i += 1) {
                this.elements[i].addEventListener('paste', this.pasteWrapper);
            }
            return this;
        },

        setPlaceholders: function () {
            var i,
                activatePlaceholder = function (el) {
                    if (!(el.querySelector('img')) &&
                            !(el.querySelector('blockquote')) &&
                            el.textContent.replace(/^\s+|\s+$/g, '') === '') {
                        el.classList.add('medium-editor-placeholder');
                    }
                },
                placeholderWrapper = function (e) {
                    this.classList.remove('medium-editor-placeholder');
                    if (e.type !== 'keypress') {
                        activatePlaceholder(this);
                    }
                };
            for (i = 0; i < this.elements.length; i += 1) {
                activatePlaceholder(this.elements[i]);
                this.elements[i].addEventListener('blur', placeholderWrapper);
                this.elements[i].addEventListener('keypress', placeholderWrapper);
            }
            return this;
        },

        cleanPaste: function (text) {

            /*jslint regexp: true*/
            /*
                jslint does not allow character negation, because the negation
                will not match any unicode characters. In the regexes in this
                block, negation is used specifically to match the end of an html
                tag, and in fact unicode characters *should* be allowed.
            */
            var i, elList, workEl,
                el = this.getSelectionElement(),
                multiline = /<p|<br|<div/.test(text),
                replacements = [

                    // replace two bogus tags that begin pastes from google docs
                    [new RegExp(/<[^>]*docs-internal-guid[^>]*>/gi), ""],
                    [new RegExp(/<\/b>(<br[^>]*>)?$/gi), ""],

                     // un-html spaces and newlines inserted by OS X
                    [new RegExp(/<span class="Apple-converted-space">\s+<\/span>/g), ' '],
                    [new RegExp(/<br class="Apple-interchange-newline">/g), '<br>'],

                    // replace google docs italics+bold with a span to be replaced once the html is inserted
                    [new RegExp(/<span[^>]*(font-style:italic;font-weight:bold|font-weight:bold;font-style:italic)[^>]*>/gi), '<span class="replace-with italic bold">'],

                    // replace google docs italics with a span to be replaced once the html is inserted
                    [new RegExp(/<span[^>]*font-style:italic[^>]*>/gi), '<span class="replace-with italic">'],

                    //[replace google docs bolds with a span to be replaced once the html is inserted
                    [new RegExp(/<span[^>]*font-weight:bold[^>]*>/gi), '<span class="replace-with bold">'],

                     // replace manually entered b/i/a tags with real ones
                    [new RegExp(/&lt;(\/?)(i|b|a)&gt;/gi), '<$1$2>'],

                     // replace manually a tags with real ones, converting smart-quotes from google docs
                    [new RegExp(/&lt;a\s+href=(&quot;|&rdquo;|&ldquo;|“|”)([^&]+)(&quot;|&rdquo;|&ldquo;|“|”)&gt;/gi), '<a href="$2">']

                ];
            /*jslint regexp: false*/

            for (i = 0; i < replacements.length; i += 1) {
                text = text.replace(replacements[i][0], replacements[i][1]);
            }

            if (multiline) {

                // double br's aren't converted to p tags, but we want paragraphs.
                elList = text.split('<br><br>');

                this.pasteHTML('<p>' + elList.join('</p><p>') + '</p>');
                document.execCommand('insertText', false, "\n");

                // block element cleanup
                elList = el.querySelectorAll('p,div,br');
                for (i = 0; i < elList.length; i += 1) {

                    workEl = elList[i];

                    switch (workEl.tagName.toLowerCase()) {
                    case 'p':
                    case 'div':
                        this.filterCommonBlocks(workEl);
                        break;
                    case 'br':
                        this.filterLineBreak(workEl);
                        break;
                    }

                }


            } else {

                this.pasteHTML(text);

            }

        },

        pasteHTML: function (html) {
            var elList, workEl, i, fragmentBody, pasteBlock = document.createDocumentFragment();

            pasteBlock.appendChild(document.createElement('body'));

            fragmentBody = pasteBlock.querySelector('body');
            fragmentBody.innerHTML = html;

            this.cleanupSpans(fragmentBody);

            elList = fragmentBody.querySelectorAll('*');
            for (i = 0; i < elList.length; i += 1) {

                workEl = elList[i];

                // delete ugly attributes
                workEl.removeAttribute('class');
                workEl.removeAttribute('style');
                workEl.removeAttribute('dir');

                if (workEl.tagName.toLowerCase() === 'meta') {
                    workEl.parentNode.removeChild(workEl);
                }

            }
            document.execCommand('insertHTML', false, fragmentBody.innerHTML.replace(/&nbsp;/g, ' '));
        },
        isCommonBlock: function (el) {
            return (el && (el.tagName.toLowerCase() === 'p' || el.tagName.toLowerCase() === 'div'));
        },
        filterCommonBlocks: function (el) {
            if (/^\s*$/.test(el.innerText)) {
                el.parentNode.removeChild(el);
            }
        },
        filterLineBreak: function (el) {
            if (this.isCommonBlock(el.previousElementSibling)) {

                // remove stray br's following common block elements
                el.parentNode.removeChild(el);

            } else if (this.isCommonBlock(el.parentNode) && (el.parentNode.firstChild === el || el.parentNode.lastChild === el)) {

                // remove br's just inside open or close tags of a div/p
                el.parentNode.removeChild(el);

            } else if (el.parentNode.childElementCount === 1) {

                // and br's that are the only child of a div/p
                this.removeWithParent(el);

            }

        },

        // remove an element, including its parent, if it is the only element within its parent
        removeWithParent: function (el) {
            if (el && el.parentNode) {
                if (el.parentNode.parentNode && el.parentNode.childElementCount === 1) {
                    el.parentNode.parentNode.removeChild(el.parentNode);
                } else {
                    el.parentNode.removeChild(el.parentNode);
                }
            }
        },

        cleanupSpans: function (container_el) {

            var i,
                el,
                new_el,
                spans = container_el.querySelectorAll('.replace-with');

            for (i = 0; i < spans.length; i += 1) {

                el = spans[i];
                new_el = document.createElement(el.classList.contains('bold') ? 'b' : 'i');

                if (el.classList.contains('bold') && el.classList.contains('italic')) {

                    // add an i tag as well if this has both italics and bold
                    new_el.innerHTML = '<i>' + el.innerHTML + '</i>';

                } else {

                    new_el.innerHTML = el.innerHTML;

                }
                el.parentNode.replaceChild(new_el, el);

            }

            spans = container_el.querySelectorAll('span');
            for (i = 0; i < spans.length; i += 1) {

                el = spans[i];

                // remove empty spans, replace others with their contents
                if (/^\s*$/.test()) {
                    el.parentNode.removeChild(el);
                } else {
                    el.parentNode.replaceChild(document.createTextNode(el.innerText), el);
                }

            }

        }

    };

}(window, document));

/*!
 * headroom.js v0.6.0 - Give your page some headroom. Hide your header until you need it
 * Copyright (c) 2014 Nick Williams - http://wicky.nillia.ms/headroom.js
 * License: MIT
 */

(function(window, document) {

  'use strict';

  /* exported features */
  
  var features = {
    bind : !!(function(){}.bind),
    classList : 'classList' in document.documentElement,
    rAF : !!(window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame)
  };
  window.requestAnimationFrame = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame;
  
  /**
   * Handles debouncing of events via requestAnimationFrame
   * @see http://www.html5rocks.com/en/tutorials/speed/animations/
   * @param {Function} callback The callback to handle whichever event
   */
  function Debouncer (callback) {
    this.callback = callback;
    this.ticking = false;
  }
  Debouncer.prototype = {
    constructor : Debouncer,
  
    /**
     * dispatches the event to the supplied callback
     * @private
     */
    update : function() {
      this.callback && this.callback();
      this.ticking = false;
    },
  
    /**
     * ensures events don't get stacked
     * @private
     */
    requestTick : function() {
      if(!this.ticking) {
        requestAnimationFrame(this.rafCallback || (this.rafCallback = this.update.bind(this)));
        this.ticking = true;
      }
    },
  
    /**
     * Attach this as the event listeners
     */
    handleEvent : function() {
      this.requestTick();
    }
  };
  /**
   * Helper function for extending objects
   */
  function extend (object /*, objectN ... */) {
    if(arguments.length <= 0) {
      throw new Error('Missing arguments in extend function');
    }
  
    var result = object || {},
        key,
        i;
  
    for (i = 1; i < arguments.length; i++) {
      var replacement = arguments[i] || {};
  
      for (key in replacement) {
        if(typeof result[key] === 'object') {
          result[key] = extend(result[key], replacement[key]);
        }
        else {
          result[key] = result[key] || replacement[key];
        }
      }
    }
  
    return result;
  }
  
  /**
   * Helper function for normalizing tolerance option to object format
   */
  function normalizeTolerance (t) {
    return t === Object(t) ? t : { down : t, up : t };
  }
  
  /**
   * UI enhancement for fixed headers.
   * Hides header when scrolling down
   * Shows header when scrolling up
   * @constructor
   * @param {DOMElement} elem the header element
   * @param {Object} options options for the widget
   */
  function Headroom (elem, options) {
    options = extend(options, Headroom.options);
  
    this.lastKnownScrollY = 0;
    this.elem             = elem;
    this.debouncer        = new Debouncer(this.update.bind(this));
    this.tolerance        = normalizeTolerance(options.tolerance);
    this.classes          = options.classes;
    this.offset           = options.offset;
    this.initialised      = false;
    this.onPin            = options.onPin;
    this.onUnpin          = options.onUnpin;
    this.onTop            = options.onTop;
    this.onNotTop         = options.onNotTop;
  }
  Headroom.prototype = {
    constructor : Headroom,
  
    /**
     * Initialises the widget
     */
    init : function() {
      if(!Headroom.cutsTheMustard) {
        return;
      }
  
      this.elem.classList.add(this.classes.initial);
  
      // defer event registration to handle browser 
      // potentially restoring previous scroll position
      setTimeout(this.attachEvent.bind(this), 100);
  
      return this;
    },
  
    /**
     * Unattaches events and removes any classes that were added
     */
    destroy : function() {
      var classes = this.classes;
  
      this.initialised = false;
      window.removeEventListener('scroll', this.debouncer, false);
      this.elem.classList.remove(classes.unpinned, classes.pinned, classes.top, classes.initial);
    },
  
    /**
     * Attaches the scroll event
     * @private
     */
    attachEvent : function() {
      if(!this.initialised){
        this.lastKnownScrollY = this.getScrollY();
        this.initialised = true;
        window.addEventListener('scroll', this.debouncer, false);
  
        this.debouncer.handleEvent();
      }
    },
    
    /**
     * Unpins the header if it's currently pinned
     */
    unpin : function() {
      var classList = this.elem.classList,
        classes = this.classes;
      
      if(classList.contains(classes.pinned) || !classList.contains(classes.unpinned)) {
        classList.add(classes.unpinned);
        classList.remove(classes.pinned);
        this.onUnpin && this.onUnpin.call(this);
      }
    },
  
    /**
     * Pins the header if it's currently unpinned
     */
    pin : function() {
      var classList = this.elem.classList,
        classes = this.classes;
      
      if(classList.contains(classes.unpinned)) {
        classList.remove(classes.unpinned);
        classList.add(classes.pinned);
        this.onPin && this.onPin.call(this);
      }
    },
  
    /**
     * Handles the top states
     */
    top : function() {
      var classList = this.elem.classList,
        classes = this.classes;
      
      if(!classList.contains(classes.top)) {
        classList.add(classes.top);
        classList.remove(classes.notTop);
        this.onTop && this.onTop.call(this);
      }
    },
  
    /**
     * Handles the not top state
     */
    notTop : function() {
      var classList = this.elem.classList,
        classes = this.classes;
      
      if(!classList.contains(classes.notTop)) {
        classList.add(classes.notTop);
        classList.remove(classes.top);
        this.onNotTop && this.onNotTop.call(this);
      }
    },
  
    /**
     * Gets the Y scroll position
     * @see https://developer.mozilla.org/en-US/docs/Web/API/Window.scrollY
     * @return {Number} pixels the page has scrolled along the Y-axis
     */
    getScrollY : function() {
      return (window.pageYOffset !== undefined)
        ? window.pageYOffset
        : (document.documentElement || document.body.parentNode || document.body).scrollTop;
    },
  
    /**
     * Gets the height of the viewport
     * @see http://andylangton.co.uk/blog/development/get-viewport-size-width-and-height-javascript
     * @return {int} the height of the viewport in pixels
     */
    getViewportHeight : function () {
      return window.innerHeight
        || document.documentElement.clientHeight
        || document.body.clientHeight;
    },
  
    /**
     * Gets the height of the document
     * @see http://james.padolsey.com/javascript/get-document-height-cross-browser/
     * @return {int} the height of the document in pixels
     */
    getDocumentHeight : function () {
      var body = document.body,
        documentElement = document.documentElement;
  
      return Math.max(
          body.scrollHeight, documentElement.scrollHeight,
          body.offsetHeight, documentElement.offsetHeight,
          body.clientHeight, documentElement.clientHeight
      );
    },
  
    /**
     * determines if the scroll position is outside of document boundaries
     * @param  {int}  currentScrollY the current y scroll position
     * @return {bool} true if out of bounds, false otherwise
     */
    isOutOfBounds : function (currentScrollY) {
      var pastTop  = currentScrollY < 0,
        pastBottom = currentScrollY + this.getViewportHeight() > this.getDocumentHeight();
      
      return pastTop || pastBottom;
    },
  
    /**
     * determines if the tolerance has been exceeded
     * @param  {int} currentScrollY the current scroll y position
     * @return {bool} true if tolerance exceeded, false otherwise
     */
    toleranceExceeded : function (currentScrollY, direction) {
      return Math.abs(currentScrollY-this.lastKnownScrollY) >= this.tolerance[direction];
    },
  
    /**
     * determine if it is appropriate to unpin
     * @param  {int} currentScrollY the current y scroll position
     * @param  {bool} toleranceExceeded has the tolerance been exceeded?
     * @return {bool} true if should unpin, false otherwise
     */
    shouldUnpin : function (currentScrollY, toleranceExceeded) {
      var scrollingDown = currentScrollY > this.lastKnownScrollY,
        pastOffset = currentScrollY >= this.offset;
  
      return scrollingDown && pastOffset && toleranceExceeded;
    },
  
    /**
     * determine if it is appropriate to pin
     * @param  {int} currentScrollY the current y scroll position
     * @param  {bool} toleranceExceeded has the tolerance been exceeded?
     * @return {bool} true if should pin, false otherwise
     */
    shouldPin : function (currentScrollY, toleranceExceeded) {
      var scrollingUp  = currentScrollY < this.lastKnownScrollY,
        pastOffset = currentScrollY <= this.offset;
  
      return (scrollingUp && toleranceExceeded) || pastOffset;
    },
  
    /**
     * Handles updating the state of the widget
     */
    update : function() {
      var currentScrollY  = this.getScrollY(),
        scrollDirection = currentScrollY > this.lastKnownScrollY ? 'down' : 'up',
        toleranceExceeded = this.toleranceExceeded(currentScrollY, scrollDirection);
  
      if(this.isOutOfBounds(currentScrollY)) { // Ignore bouncy scrolling in OSX
        return;
      }
  
      if (currentScrollY <= this.offset ) {
        this.top();
      } else {
        this.notTop();
      }
  
      if(this.shouldUnpin(currentScrollY, toleranceExceeded)) {
        this.unpin();
      }
      else if(this.shouldPin(currentScrollY, toleranceExceeded)) {
        this.pin();
      }
  
      this.lastKnownScrollY = currentScrollY;
    }
  };
  /**
   * Default options
   * @type {Object}
   */
  Headroom.options = {
    tolerance : {
      up : 0,
      down : 0
    },
    offset : 0,
    classes : {
      pinned : 'headroom--pinned',
      unpinned : 'headroom--unpinned',
      top : 'headroom--top',
      notTop : 'headroom--not-top',
      initial : 'headroom'
    }
  };
  Headroom.cutsTheMustard = typeof features !== 'undefined' && features.rAF && features.bind && features.classList;

  window.Headroom = Headroom;

}(window, document));
/*!
 * headroom.js v0.6.0 - Give your page some headroom. Hide your header until you need it
 * Copyright (c) 2014 Nick Williams - http://wicky.nillia.ms/headroom.js
 * License: MIT
 */

(function($) {

  if(!$) {
    return;
  }

  ////////////
  // Plugin //
  ////////////

  $.fn.headroom = function(option) {
    return this.each(function() {
      var $this   = $(this),
        data      = $this.data('headroom'),
        options   = typeof option === 'object' && option;

      options = $.extend(true, {}, Headroom.options, options);

      if (!data) {
        data = new Headroom(this, options);
        data.init();
        $this.data('headroom', data);
      }
      if (typeof option === 'string') {
        data[option]();
      }
    });
  };

  //////////////
  // Data API //
  //////////////

  $('[data-headroom]').each(function() {
    var $this = $(this);
    $this.headroom($this.data());
  });

}(window.Zepto || window.jQuery));
'use strict';
(function ($) {
    $(document).ready(function () {
        if ($('body').hasClass('lt-ie7')) {
            return;
        }
        if ($('.bs-docs-top').length > 0) {
            setTimeout(function () {
                $('.bs-docs-top').affix();
            }, 100);
        }
        $('#app-toolbar').headroom();
        $('.marquee').marquee({ speed: 5000 });
        var $ajaxContainer = $('#appui-container');
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
        $('div[data-appui="eventbox"]').each(function () {
            var $sourceUrl = $(this).data('source'), $targetEl = $(this);
            $.getJSON($sourceUrl, function (data) {
                var divData = '';
                $.each(data.items, function (i, item) {
                    divData += '<a class="app-box-item" href="' + item.url + '">';
                    divData += '<time class="app-box-date h5">' + item.date + '</time>';
                    divData += '<span>' + item.title + '</span>';
                    divData += '<span class="app-box-item-more text-right"><i class="icon-double-angle-right"></i></span>';
                    divData += '</a>';
                });
                $targetEl.html(divData);
            });
        });
        // Medium editor
        var $editor = new MediumEditor('.editable', {
            anchorInputPlaceholder: 'Type a link',
            buttons: ['bold', 'italic', 'anchor', 'header1', 'header2', 'quote', 'unorderedlist']
        });
        $('form[data-appui="content-editable-form"]').on('submit', function (e) {
            e.preventDefault();
            var $contentObj = $editor.serialize();
            $("#content-editable-form-body").val($contentObj['element-0'].value);
            this.submit();
        });
        $('a[data-appui="content-editable-save"]').on('click', function (e) {
            e.preventDefault();
            var $targetURL = $(this).data('appui-target-url');
            $.ajax({
                url: $targetURL,
                data: $editor.serialize(),
                success: function (res) {
                    if (res.result === 'ok') {
                        $console.text('Data saved');
                    } else {
                        $console.text('Save error');
                    }
                }
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
    });
}(jQuery));