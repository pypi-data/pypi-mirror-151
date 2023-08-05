import{_ as t,s as i,e,t as s,$ as n,ar as a,n as r}from"./main-ac83c92b.js";import{aH as o,aJ as h}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";t([r("hui-climate-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return o(this,t)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return n``;const t=this.hass.states[this._config.entity];return t?n`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        <ha-climate-state .hass=${this.hass} .stateObj=${t}>
        </ha-climate-state>
      </hui-generic-entity-row>
    `:n`
        <hui-warning>
          ${h(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      ha-climate-state {
        text-align: right;
      }
    `}}]}}),i);
