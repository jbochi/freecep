/*globals $, Raphael, Math, console, document, parseInt */

var trainer = {};


trainer.img_name = "22631-002.bmp";
trainer.img_width = 570;
trainer.img_height = 120;

trainer.img_name = img.path;
trainer.img_width = img.width;
trainer.img_height = img.height;

trainer.active_symbol = false;
trainer.link_symbol = false;
trainer.symbols = [];
trainer.symbol = function (x, y, width, height, symbol) {
    var that = {};
    
    that.symbol = symbol;
    that.x = x;
    that.y = y;
    that.width = width;
    that.height = height;
    that.draw = function () {
        if (that.rect) {
            // updates existing rectangle
            that.rect.attr("x", that.x);
            that.rect.attr("y", that.y);
            that.rect.attr("width", that.width);
            that.rect.attr("height", that.height);                        
        } else {
            // create a new rectangle
            that.rect = trainer.paper.rect(that.x, that.y, that.width, that.height);
            that.rect.attr("stroke", "red");
            that.rect.attr("stroke-width", 0.5);
            that.rect.attr('fill', 'rgba(0, 0, 0, 0)');
            $(that.rect.node).click(function (event) {
                that.link();
            });
            $(that.rect.node).mousedown(function (event) {    
                event.stopPropagation();
            });
        }
        trainer.dump();
        trainer.paper.safari(); //chrome work around 
    };
    
    that.dump = function () {
        var output = [that.symbol,
                      that.x,
                      trainer.img_height - that.height - that.y,
                      that.width + that.x,
                      trainer.img_height - that.y,
                      0];
        return output.join(' ');
    };
    
    that.link = function () {
        if (trainer.link_symbol) {
            trainer.link_symbol.rect.attr('stroke', 'red');
        }
        that.rect.attr('stroke', 'purple');
        $("#symbol_form [name=symbol]").val(that.symbol);
        $("#symbol_form [name=x]").val(that.x);
        $("#symbol_form [name=y]").val(that.y);
        $("#symbol_form [name=width]").val(that.width);
        $("#symbol_form [name=height]").val(that.height);
        trainer.link_symbol = that;
    };
    
    that.remove = function () {
        that.rect.remove();
    };
    
    trainer.symbols.push(that);
    return that;
};


trainer.load = function () {
    var input, values;
    
    input = $('#dump_area').val().split('\n');
    
    
    trainer.clear();
    $.each(input, function (index, value) {
        values = value.split(' ');
        if (values.length === 5 || values.length === 6) {
            trainer.symbol(parseInt(values[1], 10),  // X
                           parseInt(trainer.img_height - values[4], 10),  // Y
                           parseInt(values[3] - values[1], 10),  // Width
                           parseInt(values[4] - values[2], 10),  // Height
                           values[0]);
        } 
    });
    trainer.draw();
    
    
};

trainer.clear = function () {
    $.each(trainer.symbols, function (index, value) {
        value.remove();
    });
    
    trainer.active_symbol = false;
    trainer.link_symbol = false;
    trainer.symbols = [];
};

trainer.dump = function () {
    var output = [];
    $.each(trainer.symbols, function (index, value) {
        output.push(value.dump());
    });
    $('#dump_area').val(output.join('\n'));
};

trainer.start = function () {
    var image, screen = document.getElementById("screen");
    trainer.paper = new Raphael(screen, trainer.img_width, trainer.img_height);
    image = trainer.paper.image(trainer.img_name, 0, 0, trainer.img_width, trainer.img_height);
    $(screen).mousedown(function (event) {
        trainer.active_symbol = trainer.symbol(event.offsetX, event.offsetY, 0, 0);
        trainer.draw();
        trainer.active_symbol.link();
    });
    $(screen).mousemove(function (event) {
        var symbol = trainer.active_symbol;
        if (symbol) {
            symbol.width = Math.max(event.offsetX - symbol.x, 0);
            symbol.height = Math.max(event.offsetY - symbol.y, 0);
            //symbol.x = Math.min(event.offsetX, symbol.x);
            //symbol.y = Math.min(event.offsetY, symbol.y);
            symbol.draw();
            trainer.active_symbol.link();
        }
    });
    $(screen).mouseup(function (event) {
        trainer.active_symbol = false;
    });
    trainer.draw();
   
    $("#symbol_form input[name=symbol]").change(function (event) {
        if (trainer.link_symbol) {
            trainer.link_symbol.symbol = $(this).val();
        }
    });    

    $("#symbol_form input.integer").spinner().bind('spinchange', function (event, ui) {
        if (trainer.link_symbol) {
            switch (event.target.name) {
            case 'x': 
                trainer.link_symbol.x = $(this).val();  
                break;
            case 'y':
                trainer.link_symbol.y = $(this).val();  
                break;
            case 'width':
                trainer.link_symbol.width = $(this).val();  
                break;
            case 'height':
                trainer.link_symbol.height = $(this).val();
                break;
            }
            trainer.link_symbol.draw();            
            trainer.dump();
        }
    });          
    
    /*
    $("#symbol_form [name=x]").val(that.x);
    $("#symbol_form [name=y]").val(that.y);
    $("#symbol_form [name=width]").val(that.width);
    $("#symbol_form [name=height]").val(that.height);
    */
    
};

trainer.draw = function () {
    $.each(trainer.symbols, function (index, value) {

        value.draw();
    });
};


$(document).ready(trainer.start);
