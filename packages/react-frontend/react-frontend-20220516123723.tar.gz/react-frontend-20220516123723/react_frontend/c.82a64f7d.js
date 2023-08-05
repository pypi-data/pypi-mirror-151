import{_ as t,s as i,e,$ as s,n}from"./main-ac83c92b.js";import"./c.027db416.js";import{aH as o,aJ as r}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([n("hui-humidifier-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[e()],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return o(this,t)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return s``;const t=this.hass.states[this._config.entity];return t?s`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        .secondaryText=${t.attributes.humidity?`${this.hass.localize("ui.card.humidifier.humidity")}:\n            ${t.attributes.humidity} %${t.attributes.mode?` (${this.hass.localize(`state_attributes.humidifier.mode.${t.attributes.mode}`)||t.attributes.mode})`:""}`:""}
      >
        <ha-entity-toggle
          .hass=${this.hass}
          .stateObj=${t}
        ></ha-entity-toggle>
      </hui-generic-entity-row>
    `:s`
        <hui-warning>
          ${r(this.hass,this._config.entity)}
        </hui-warning>
      `}}]}}),i);
