define({

    handleClickOutside: function(element, marker) {
        const outsideClickListener = event => {
            if (!element.contains(event.target)) { // or use: event.target.closest(selector) === null
                if (element.classList.contains(marker)) {
                    // element.style.display = 'none'
                    console.log('Remove open marker');
                    element.classList.remove(marker);
                    removeClickListener()
                }
            }
        };
        const removeClickListener = () => {
            document.removeEventListener('click', outsideClickListener)
        };
        document.addEventListener('click', outsideClickListener);

        // document.addEventListener('click', function(event) {
        //     var isClickInside = element.contains(event.target);
        //     if (isClickInside) {
        //         console.log('You clicked inside');
        //     }
        //     else {
        //         console.log('You clicked outside')
        //         element.classList.remove(marker);
        //         console.log(element);
        //     }
        // });
    },

    extendDefaultOptions: function(){
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
});
