import{_ as e,s as i,e as t,t as a,$ as s,f as o,n as c}from"./main-ac83c92b.js";import"./c.1fca9ca6.js";import{X as n,Y as r,Z as l,a2 as h,_ as d,a7 as m,a0 as u}from"./c.3e14cfd3.js";import"./c.3fc42334.js";import{b as f}from"./c.461e571b.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.027db416.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.8cbd7110.js";import"./c.53212acc.js";import"./c.cfa85e17.js";import"./c.0e001851.js";const p=n(f,r({entities:l(h(d())),title:l(d()),hours_to_show:l(m()),theme:l(d())})),g=[{name:"title",selector:{text:{}}},{name:"",type:"grid",schema:[{name:"theme",selector:{theme:{}}},{name:"hours_to_show",selector:{number:{mode:"box",min:1}}}]}];let v=e([c("hui-logbook-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){u(e,p),this._config=e}},{kind:"get",key:"_entities",value:function(){return this._config.entities||[]}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?s`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${g}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <h3>
        ${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})`}
      </h3>
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this._entities}
        @value-changed=${this._entitiesChanged}
      >
      </ha-entities-picker>
    `:s``}},{kind:"method",key:"_entitiesChanged",value:function(e){this._config={...this._config,entities:e.detail.value},o(this,"config-changed",{config:this._config})}},{kind:"method",key:"_valueChanged",value:function(e){o(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||this.hass.localize(`ui.panel.lovelace.editor.card.logbook.${e.name}`)}}]}}),i);export{v as HuiLogbookCardEditor};
