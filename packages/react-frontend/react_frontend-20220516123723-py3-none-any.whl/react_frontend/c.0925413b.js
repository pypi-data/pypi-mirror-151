import{_ as t,s as i,e as s,t as o,$ as e,ar as n,n as r}from"./main-ac83c92b.js";import{aH as a,aJ as c,m as h}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";t([r("hui-cover-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return a(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return e``;const t=this.hass.states[this._config.entity];return t?e`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        ${h(t)?e`
              <ha-cover-tilt-controls
                .hass=${this.hass}
                .stateObj=${t}
              ></ha-cover-tilt-controls>
            `:e`
              <ha-cover-controls
                .hass=${this.hass}
                .stateObj=${t}
              ></ha-cover-controls>
            `}
      </hui-generic-entity-row>
    `:e`
        <hui-warning>
          ${c(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      ha-cover-controls,
      ha-cover-tilt-controls {
        margin-right: -0.57em;
      }
    `}}]}}),i);
