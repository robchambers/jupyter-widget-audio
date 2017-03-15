var widgets = require('jupyter-js-widgets');
var _ = require('underscore');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var AudioModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
        _model_name : 'AudioModel',
        _view_name : 'AudioView',
        _model_module : 'jupyter-widget-audio',
        _view_module : 'jupyter-widget-audio',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        // value : 'Audio World'
        src:'',
        // type:'',

    })
});


// Custom View. Renders the widget model.
var AudioView = widgets.DOMWidgetView.extend({
    render: function() {

        console.log('render');
        this.el.setAttribute('controls', 'controls');
        this.el.setAttribute('src', this.model.get('src'));//'http://www.kozco.com/tech/piano2.wav');

        // this._color_container = document.createElement('div');
        // this._color_container.className = 'widget-inline-hbox widget-colorpicker-input';
        // this.el.appendChild(this._color_container);
        //
        // this._textbox = document.createElement('input');
        // this._textbox.setAttribute('type', 'text');
        //
        // this._color_container.appendChild(this._textbox);
        // this._textbox.value = this.model.get('value');
        //
        // this._colorpicker = document.createElement('input');
        // this._colorpicker.setAttribute('type', 'color');
        // this._color_container.appendChild(this._colorpicker);

        // this.listenTo(this.model, 'change:value', this._update_value);
        // this.listenTo(this.model, 'change:concise', this._update_concise);

        // this._update_concise();
        // this._update_value();
    // }
    //
    //
        this.value_changed();
        // this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        // this.el.textContent = this.model.get('value');
    },



    get tagName() {
        // We can't make this an attribute with a default value
        // since it would be set after it is needed in the
        // constructor.
        return 'audio';
    }

});


module.exports = {
    AudioModel : AudioModel,
    AudioView : AudioView
};
