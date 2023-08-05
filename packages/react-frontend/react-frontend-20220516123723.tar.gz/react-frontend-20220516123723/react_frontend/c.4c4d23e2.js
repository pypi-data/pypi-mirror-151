import{_ as e,s as t,e as a,t as i,$ as s,f as c,n as o}from"./main-ac83c92b.js";import"./c.1fca9ca6.js";import{X as r,Y as d,Z as n,_ as l,a0 as m}from"./c.3e14cfd3.js";import{b as u}from"./c.461e571b.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.027db416.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.8cbd7110.js";const h=r(u,d({title:n(l()),url:n(l()),aspect_ratio:n(l())})),f=[{name:"title",selector:{text:{}}},{name:"",type:"grid",schema:[{name:"url",required:!0,selector:{text:{}}},{name:"aspect_ratio",selector:{text:{}}}]}];let p=e([o("hui-iframe-card-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){m(e,h),this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?s`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${f}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `:s``}},{kind:"method",key:"_valueChanged",value:function(e){c(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}}]}}),t);export{p as HuiIframeCardEditor};
