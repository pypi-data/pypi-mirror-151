import{_ as e,s as i,e as t,t as a,$ as o,f as s,ar as n,n as c}from"./main-ac83c92b.js";import{i as l}from"./c.027db416.js";import{X as r,Y as h,Z as d,_ as u,a0 as f}from"./c.3e14cfd3.js";import"./c.86ce6bc8.js";import{b as g}from"./c.461e571b.js";import"./c.8cbd7110.js";const v=r(g,h({title:d(u()),theme:d(u())}));let _=e([c("hui-shopping-list-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){f(e,v),this._config=e}},{kind:"get",key:"_title",value:function(){return this._config.title||""}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?o`
      <div class="card-config">
        ${l(this.hass,"shopping_list")?"":o`
              <div class="error">
                ${this.hass.localize("ui.panel.lovelace.editor.card.shopping-list.integration_not_loaded")}
              </div>
            `}
        <ha-textfield
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.title")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value=${this._title}
          .configValue=${"title"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-theme-picker
          .hass=${this.hass}
          .value=${this._theme}
          .configValue=${"theme"}
          .label=${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`}
          @value-changed=${this._valueChanged}
        ></ha-theme-picker>
      </div>
    `:o``}},{kind:"method",key:"_valueChanged",value:function(e){if(!this._config||!this.hass)return;const i=e.target;this[`_${i.configValue}`]!==i.value&&(i.configValue&&(""===i.value?(this._config={...this._config},delete this._config[i.configValue]):this._config={...this._config,[i.configValue]:i.value}),s(this,"config-changed",{config:this._config}))}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      .error {
        color: var(--error-color);
      }
    `}}]}}),i);export{_ as HuiShoppingListEditor};
