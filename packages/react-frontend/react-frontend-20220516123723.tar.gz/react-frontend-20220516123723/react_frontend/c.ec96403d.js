import{_ as e,s as t,e as i,t as s,g as a,i as n,$ as d,ar as r,n as o}from"./main-ac83c92b.js";import{aH as h,aJ as l,aK as u,O as c}from"./c.3e14cfd3.js";import{U as f,e as m,d as v}from"./c.027db416.js";import{s as b}from"./c.279ecd1c.js";import"./c.8cbd7110.js";e([o("hui-input-number-entity-row")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",key:"_loaded",value:void 0},{kind:"field",key:"_updated",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"setConfig",value:function(e){if(!e)throw new Error("Invalid configuration");this._config=e}},{kind:"method",key:"connectedCallback",value:function(){a(n(o.prototype),"connectedCallback",this).call(this),this._updated&&!this._loaded&&this._initialLoad(),this._attachObserver()}},{kind:"method",key:"disconnectedCallback",value:function(){var e;null===(e=this._resizeObserver)||void 0===e||e.disconnect()}},{kind:"method",key:"firstUpdated",value:function(){this._updated=!0,this.isConnected&&!this._loaded&&this._initialLoad(),this._attachObserver()}},{kind:"method",key:"shouldUpdate",value:function(e){return h(this,e)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return d``;const e=this.hass.states[this._config.entity];return e?d`
      <hui-generic-entity-row .hass=${this.hass} .config=${this._config}>
        ${"slider"===e.attributes.mode?d`
              <div class="flex">
                <ha-slider
                  .disabled=${f.includes(e.state)}
                  .dir=${m(this.hass)}
                  .step=${Number(e.attributes.step)}
                  .min=${Number(e.attributes.min)}
                  .max=${Number(e.attributes.max)}
                  .value=${e.state}
                  pin
                  @change=${this._selectedValueChanged}
                  ignore-bar-touch
                ></ha-slider>
                <span class="state">
                  ${u(this.hass.localize,e,this.hass.locale,e.state)}
                </span>
              </div>
            `:d`
              <div class="flex state">
                <ha-textfield
                  .disabled=${f.includes(e.state)}
                  pattern="[0-9]+([\\.][0-9]+)?"
                  .step=${Number(e.attributes.step)}
                  .min=${Number(e.attributes.min)}
                  .max=${Number(e.attributes.max)}
                  .value=${e.state}
                  .suffix=${e.attributes.unit_of_measurement}
                  type="number"
                  @change=${this._selectedValueChanged}
                >
                </ha-textfield>
              </div>
            `}
      </hui-generic-entity-row>
    `:d`
        <hui-warning>
          ${l(this.hass,this._config.entity)}
        </hui-warning>
      `}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      :host {
        display: block;
      }
      .flex {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        flex-grow: 2;
      }
      .state {
        min-width: 45px;
        text-align: end;
      }
      ha-textfield {
        text-align: end;
      }
      ha-slider {
        width: 100%;
        max-width: 200px;
      }
    `}},{kind:"method",key:"_initialLoad",value:async function(){this._loaded=!0,await this.updateComplete,this._measureCard()}},{kind:"method",key:"_measureCard",value:function(){if(!this.isConnected)return;const e=this.shadowRoot.querySelector(".state");e&&(e.hidden=this.clientWidth<=300)}},{kind:"method",key:"_attachObserver",value:async function(){this._resizeObserver||(await c(),this._resizeObserver=new ResizeObserver(v((()=>this._measureCard()),250,!1))),this.isConnected&&this._resizeObserver.observe(this)}},{kind:"method",key:"_selectedValueChanged",value:function(e){const t=this.hass.states[this._config.entity];e.target.value!==t.state&&b(this.hass,t.entity_id,e.target.value)}}]}}),t);
