import{_ as e,s as a,e as t,t as i,$ as o,f as c,n as s}from"./main-ac83c92b.js";import"./c.1fca9ca6.js";import{X as r,Y as n,Z as l,_ as d,a0 as m}from"./c.3e14cfd3.js";import{b as h}from"./c.461e571b.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.027db416.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.8cbd7110.js";const u=r(h,n({title:l(d()),content:d(),theme:l(d())})),f=[{name:"title",selector:{text:{}}},{name:"content",required:!0,selector:{text:{multiline:!0}}},{name:"theme",selector:{theme:{}}}];let p=e([s("hui-markdown-card-editor")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){m(e,u),this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?o`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${f}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:o``}},{kind:"method",key:"_valueChanged",value:function(e){c(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||this.hass.localize(`ui.panel.lovelace.editor.card.markdown.${e.name}`)}}]}}),a);export{p as HuiMarkdownCardEditor};
