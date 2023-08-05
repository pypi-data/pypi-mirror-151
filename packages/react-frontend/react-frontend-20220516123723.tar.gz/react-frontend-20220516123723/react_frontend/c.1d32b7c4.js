import{_ as t,s as i,e as s,t as e,$ as n,ar as o,n as c}from"./main-ac83c92b.js";import{U as a}from"./c.027db416.js";import{aH as r,aJ as h}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([c("hui-lock-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return r(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return n``;const t=this.hass.states[this._config.entity];return t?n`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        <mwc-button
          @click=${this._callService}
          .disabled=${a.includes(t.state)}
          class="text-content"
        >
          ${"locked"===t.state?this.hass.localize("ui.card.lock.unlock"):this.hass.localize("ui.card.lock.lock")}
        </mwc-button>
      </hui-generic-entity-row>
    `:n`
        <hui-warning>
          ${h(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      mwc-button {
        margin-right: -0.57em;
      }
    `}},{kind:"method",key:"_callService",value:function(t){t.stopPropagation();const i=this.hass.states[this._config.entity];this.hass.callService("lock","locked"===i.state?"unlock":"lock",{entity_id:i.entity_id})}}]}}),i);
