import{_ as i,s as e,e as t,t as a,$ as c,f as o,ar as s,n}from"./main-ac83c92b.js";import{X as r,Y as l,Z as d,_ as h,a0 as u}from"./c.3e14cfd3.js";import"./c.11a6fda3.js";import"./c.86ce6bc8.js";import{a as m}from"./c.1430be7b.js";import{b as p}from"./c.461e571b.js";import{c as f}from"./c.ad12eed4.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.958cb46c.js";import"./c.57c0073c.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.4e93087d.js";import"./c.cfa85e17.js";import"./c.c018532e.js";import"./c.e9aa747b.js";import"./c.53212acc.js";import"./c.0e001851.js";import"./c.8d0ef0b0.js";import"./c.1fca9ca6.js";import"./c.8eddd911.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.d6711a1d.js";import"./c.622dfac1.js";import"./c.8786ad90.js";import"./c.be47aa9a.js";import"./c.39da0aeb.js";import"./c.02ed471c.js";import"./c.9e7e5aa1.js";import"./c.3eb3ee48.js";import"./c.6999bfff.js";import"./c.2541228c.js";import"./c.0225555d.js";import"./c.6e13c00f.js";import"./c.40d6516d.js";import"./c.4860f91b.js";import"./c.550b6e59.js";import"./c.3fc42334.js";import"./c.e38196bb.js";import"./c.5756eeee.js";const g=r(p,l({image:d(h()),tap_action:d(m),hold_action:d(m),theme:d(h())}));let j=i([n("hui-picture-card-editor")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(i){u(i,g),this._config=i}},{kind:"get",key:"_image",value:function(){return this._config.image||""}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"none"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"none"}}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return c``;const i=["navigate","url","call-service","none"];return c`
      <div class="card-config">
        <ha-textfield
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.image")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
          .value=${this._image}
          .configValue=${"image"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-theme-picker
          .hass=${this.hass}
          .value=${this._theme}
          .label=${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`}
          .configValue=${"theme"}
          @value-changed=${this._valueChanged}
        ></ha-theme-picker>
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._tap_action}
          .actions=${i}
          .configValue=${"tap_action"}
          @value-changed=${this._valueChanged}
        ></hui-action-editor>
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._hold_action}
          .actions=${i}
          .configValue=${"hold_action"}
          @value-changed=${this._valueChanged}
        ></hui-action-editor>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(i){var e,t;if(!this._config||!this.hass)return;const a=i.target,c=null!==(e=null===(t=i.detail)||void 0===t?void 0:t.value)&&void 0!==e?e:a.value;this[`_${a.configValue}`]!==c&&(a.configValue&&(!1===c||c?this._config={...this._config,[a.configValue]:c}:(this._config={...this._config},delete this._config[a.configValue])),o(this,"config-changed",{config:this._config}))}},{kind:"get",static:!0,key:"styles",value:function(){return[f,s`
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),e);export{j as HuiPictureCardEditor};
