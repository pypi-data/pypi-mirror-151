var jcropapi;function setupJcrop(t,i,o,a){t.Jcrop({trueSize:[i.width,i.height],bgColor:"rgb(192, 192, 192)",onSelect:function(t){var i=Math.floor((t.x+t.x2)/2),o=Math.floor((t.y+t.y2)/2),h=Math.floor(t.w),e=Math.floor(t.h);a.x.val(i),a.y.val(o),a.width.val(h),a.height.val(e)},onRelease:function(){a.x.val(o.x),a.y.val(o.y),a.width.val(o.width),a.height.val(o.height)}},(function(){jcropapi=this,$("img",jcropapi.ui.holder).attr("alt","")}))}$((function(){var t=$("div.focal-point-chooser"),i=$(".current-focal-point-indicator",t),o=$("img",t),a={width:o.data("originalWidth"),height:o.data("originalHeight")},h={x:t.data("focalPointX"),y:t.data("focalPointY"),width:t.data("focalPointWidth"),height:t.data("focalPointHeight")},e={x:$("input.focal_point_x"),y:$("input.focal_point_y"),width:$("input.focal_point_width"),height:$("input.focal_point_height")},r=h.x-h.width/2,c=h.y-h.height/2,l=h.width,n=h.height;i.css("left",100*r/a.width+"%"),i.css("top",100*c/a.height+"%"),i.css("width",100*l/a.width+"%"),i.css("height",100*n/a.height+"%");var p=[o,a,h,e];setupJcrop.apply(this,p),$(window).on("resize",$.debounce(300,(function(){jcropapi.destroy(),o.removeAttr("style"),$(".jcrop-holder").remove(),setupJcrop.apply(this,p)}))),$(".remove-focal-point").on("click",(function(){jcropapi.destroy(),o.removeAttr("style"),$(".jcrop-holder").remove(),$(".current-focal-point-indicator").remove(),e.x.val(""),e.y.val(""),e.width.val(""),e.height.val(""),setupJcrop.apply(this,p)}))}));