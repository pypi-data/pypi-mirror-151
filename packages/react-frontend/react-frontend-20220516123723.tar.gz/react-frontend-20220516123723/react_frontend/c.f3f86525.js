import{_ as t,s as e,e as s,t as i,$ as a,ar as n,n as c}from"./main-ac83c92b.js";import{c as o,x as h,s as r,Z as l}from"./c.027db416.js";import{aH as d,aJ as u,aM as f}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([c("hui-select-entity-row")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return d(this,t)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return a``;const t=this.hass.states[this._config.entity];return t?a`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        hideName
      >
        <ha-select
          .label=${this._config.name||o(t)}
          .value=${t.state}
          .disabled=${t.state===h}
          naturalMenuWidth
          @selected=${this._selectedChanged}
          @click=${r}
          @closed=${r}
        >
          ${t.attributes.options?t.attributes.options.map((e=>a`
                    <mwc-list-item .value=${e}
                      >${t.attributes.device_class&&this.hass.localize(`component.select.state.${t.attributes.device_class}.${e}`)||this.hass.localize(`component.select.state._.${e}`)||e}
                    </mwc-list-item>
                  `)):""}
        </ha-select>
      </hui-generic-entity-row>
    `:a`
        <hui-warning>
          ${u(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      hui-generic-entity-row {
        display: flex;
        align-items: center;
      }
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_selectedChanged",value:function(t){const e=this.hass.states[this._config.entity],s=t.target.value;s!==e.state&&e.attributes.options.includes(s)&&(l("light"),f(this.hass,e.entity_id,s))}}]}}),e);
