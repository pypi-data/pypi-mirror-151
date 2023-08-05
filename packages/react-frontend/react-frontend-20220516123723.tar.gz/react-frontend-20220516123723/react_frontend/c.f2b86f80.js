import{_ as t,s as i,e as s,t as e,$ as n,n as o}from"./main-ac83c92b.js";import{h as a,$ as r}from"./c.027db416.js";import{aH as h,aJ as c,aK as u}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([o("hui-group-entity-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"_config",value:void 0},{kind:"method",key:"_computeCanToggle",value:function(t,i){return i.some((i=>{const s=a(i);var e;return"group"===s?this._computeCanToggle(t,null===(e=this.hass)||void 0===e?void 0:e.states[i].attributes.entity_id):r.has(s)}))}},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return h(this,t)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return n``;const t=this.hass.states[this._config.entity];return t?n`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        ${this._computeCanToggle(this.hass,t.attributes.entity_id)?n`
              <ha-entity-toggle
                .hass=${this.hass}
                .stateObj=${t}
              ></ha-entity-toggle>
            `:n`
              <div class="text-content">
                ${u(this.hass.localize,t,this.hass.locale)}
              </div>
            `}
      </hui-generic-entity-row>
    `:n`
        <hui-warning>
          ${c(this.hass,this._config.entity)}
        </hui-warning>
      `}}]}}),i);
