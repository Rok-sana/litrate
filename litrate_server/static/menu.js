 function padding_page(){
    var h_hght = 22.9; // высота шапки
    var h_mrg = 0;    // отступ когда шапка уже не видна

    $(function(){
        var elem = $('#top_nav');
        var top = $(this).scrollTop();
        var h_px = document.body.clientWidth * 0.01 * h_hght + document.body.clientWidth * 0.0035;
        if(top > h_px){
            elem.css('top', h_mrg);
        }
        $(window).scroll(function(){
            top = $(this).scrollTop();
            if (top+h_mrg < h_px) {
                elem.css('top', (h_px-top));
            } else {
                elem.css('top', h_mrg);
            }
        });
    });

    }
    //setInterval(padding_page, 1000);





    /*
    *
    * Credits to https://css-tricks.com/long-dropdowns-solution/
    *
    */
    function menu_height(){
    var maxHeight = 400;

    $(function(){

        $(".dropdown > li").hover(function() {

             var $container = $(this),
                 $list = $container.find("ul"),
                 $anchor = $container.find("a"),
                 height = $list.height() * 1.1,       // make sure there is enough room at the bottom
                 multiplier = height / maxHeight;     // needs to move faster if list is taller

            // need to save height here so it can revert on mouseout
            $container.data("origHeight", $container.height());

            // so it can retain it's rollover color all the while the dropdown is open
            $anchor.addClass("hover");

            // make sure dropdown appears directly below parent list item
            $list
                .show()
                .css({
                    paddingTop: $container.data("origHeight")
                });

            // don't do any animation if list shorter than max
            if (multiplier > 1) {
                $container
                    .css({
                        height: maxHeight,
                        overflow: "hidden"
                    })
                    .mousemove(function(e) {
                        var offset = $container.offset();
                        var relativeY = ((e.pageY - offset.top) * multiplier) - ($container.data("origHeight") * multiplier);
                        if (relativeY > $container.data("origHeight")) {
                            $list.css("top", -relativeY + $container.data("origHeight"));
                        };
                    });
            }

        }, function() {

            var $el = $(this);

            // put things back to normal
            $el
                .height($(this).data("origHeight"))
                .find("ul")
                .css({ top: 0 })
                .hide()
                .end()
                .find("a")
                .removeClass("hover");

        });

    });
    }
