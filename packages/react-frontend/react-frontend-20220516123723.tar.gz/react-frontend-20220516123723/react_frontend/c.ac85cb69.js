import{_ as e,s as i,e as t,t as a,$ as n,f as c,n as s}from"./main-ac83c92b.js";import{X as o,Y as h,Z as l,_ as r,a0 as d}from"./c.3e14cfd3.js";import"./c.53212acc.js";import"./c.86ce6bc8.js";import{b as u}from"./c.461e571b.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.cfa85e17.js";import"./c.0e001851.js";const f=o(u,h({entity:l(r()),theme:l(r())})),g=["media_player"];let m=e([s("hui-media-control-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){d(e,f),this._config=e}},{kind:"get",key:"_entity",value:function(){return this._config.entity||""}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?n`
      <div class="card-config">
        <ha-entity-picker
          .label=${this.hass.localize("ui.panel.lovelace.editor.card.generic.entity")}
          .hass=${this.hass}
          .value=${this._entity}
          .configValue=${"entity"}
          .includeDomains=${g}
          .required=${!0}
          @change=${this._valueChanged}
          allow-custom-entity
        ></ha-entity-picker>
        <ha-theme-picker
          .label=${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`}
          .hass=${this.hass}
          .value=${this._theme}
          .configValue=${"theme"}
          @value-changed=${this._valueChanged}
        ></ha-theme-picker>
      </div>
    `:n``}},{kind:"method",key:"_valueChanged",value:function(e){if(!this._config||!this.hass)return;const i=e.target;this[`_${i.configValue}`]!==i.value&&(i.configValue&&(""===i.value?(this._config={...this._config},delete this._config[i.configValue]):this._config={...this._config,[i.configValue]:i.value}),c(this,"config-changed",{config:this._config}))}}]}}),i);export{m as HuiMediaControlCardEditor};
