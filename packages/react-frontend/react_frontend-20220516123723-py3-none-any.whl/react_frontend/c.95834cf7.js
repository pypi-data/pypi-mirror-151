import{_ as t,s as i,e,t as a,$ as s,ar as n,n as o}from"./main-ac83c92b.js";import"./c.550b6e59.js";import{c as h,U as r,w as d}from"./c.027db416.js";import{s as u,a as c}from"./c.fe74db75.js";import{aH as l,aJ as f}from"./c.3e14cfd3.js";import"./c.25e73c3c.js";import"./c.8cbd7110.js";t([o("hui-input-datetime-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return l(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return s``;const t=this.hass.states[this._config.entity];if(!t)return s`
        <hui-warning>
          ${f(this.hass,this._config.entity)}
        </hui-warning>
      `;const i=this._config.name||h(t);return s`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        .hideName=${t.attributes.has_date&&t.attributes.has_time}
      >
        ${t.attributes.has_date?s`
              <ha-date-input
                .label=${t.attributes.has_time?i:void 0}
                .locale=${this.hass.locale}
                .disabled=${r.includes(t.state)}
                .value=${u(t)}
                @value-changed=${this._dateChanged}
              >
              </ha-date-input>
            `:""}
        ${t.attributes.has_time?s`
              <ha-time-input
                .value=${t.state===d?"":t.attributes.has_date?t.state.split(" ")[1]:t.state}
                .locale=${this.hass.locale}
                .disabled=${r.includes(t.state)}
                @value-changed=${this._timeChanged}
                @click=${this._stopEventPropagation}
              ></ha-time-input>
            `:""}
      </hui-generic-entity-row>
    `}},{kind:"method",key:"_stopEventPropagation",value:function(t){t.stopPropagation()}},{kind:"method",key:"_timeChanged",value:function(t){const i=this.hass.states[this._config.entity];c(this.hass,i.entity_id,t.detail.value,i.attributes.has_date?i.state.split(" ")[0]:void 0),t.target.blur()}},{kind:"method",key:"_dateChanged",value:function(t){const i=this.hass.states[this._config.entity];c(this.hass,i.entity_id,i.attributes.has_time?i.state.split(" ")[1]:void 0,t.detail.value),t.target.blur()}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      ha-date-input + ha-time-input {
        margin-left: 4px;
      }
    `}}]}}),i);
