import{_ as t,s as e,e as i,t as a,$ as s,ar as n,n as r}from"./main-ac83c92b.js";import{c as o,x as h,U as d}from"./c.027db416.js";import{s as c}from"./c.279ecd1c.js";import{aH as u,aJ as l}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([r("hui-input-text-entity-row")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return u(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return s``;const t=this.hass.states[this._config.entity];return t?s`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        hideName
      >
        <ha-textfield
          .label=${this._config.name||o(t)}
          .disabled=${t.state===h}
          .value=${t.state}
          .minlength=${t.attributes.min}
          .maxlength=${t.attributes.max}
          .autoValidate=${t.attributes.pattern}
          .pattern=${t.attributes.pattern}
          .type=${t.attributes.mode}
          @change=${this._selectedValueChanged}
          placeholder="(empty value)"
        ></ha-textfield>
      </hui-generic-entity-row>
    `:s`
        <hui-warning>
          ${l(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"method",key:"_selectedValueChanged",value:function(t){const e=this.hass.states[this._config.entity],i=t.target.value;i&&d.includes(i)?t.target.value=e.state:(i!==e.state&&c(this.hass,e.entity_id,i),t.target.blur())}},{kind:"field",static:!0,key:"styles",value:()=>n`
    hui-generic-entity-row {
      display: flex;
      align-items: center;
    }
    ha-textfield {
      width: 100%;
    }
  `}]}}),e);
