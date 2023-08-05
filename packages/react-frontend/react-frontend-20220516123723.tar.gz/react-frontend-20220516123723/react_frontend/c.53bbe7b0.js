import{_ as t,s as i,e as n,t as s,$ as e,ar as o,n as r}from"./main-ac83c92b.js";import{x as a}from"./c.027db416.js";import{aH as c,aJ as u}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([r("hui-input-button-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[n({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return c(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return e``;const t=this.hass.states[this._config.entity];return t?e`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        <mwc-button
          @click=${this._pressButton}
          .disabled=${t.state===a}
        >
          ${this.hass.localize("ui.card.button.press")}
        </mwc-button>
      </hui-generic-entity-row>
    `:e`
        <hui-warning>
          ${u(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      mwc-button:last-child {
        margin-right: -0.57em;
      }
    `}},{kind:"method",key:"_pressButton",value:function(t){t.stopPropagation(),this.hass.callService("input_button","press",{entity_id:this._config.entity})}}]}}),i);
