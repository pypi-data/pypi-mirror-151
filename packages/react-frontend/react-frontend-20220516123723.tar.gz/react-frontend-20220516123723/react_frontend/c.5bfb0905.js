import{_ as t,s as e,e as a,ap as i,$ as s,dL as r,dd as n,f as l,ar as o,n as d,aq as u,g as c,i as h}from"./main-ac83c92b.js";import{z as m,e as _,s as g}from"./c.027db416.js";import{c as v,b as p,e as b,g as $,h as f,i as k,j as y,k as w,l as x}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([d("ha-climate-control")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"value",value:void 0},{kind:"field",decorators:[a()],key:"unit",value:()=>""},{kind:"field",decorators:[a()],key:"min",value:void 0},{kind:"field",decorators:[a()],key:"max",value:void 0},{kind:"field",decorators:[a()],key:"step",value:()=>1},{kind:"field",key:"_lastChanged",value:void 0},{kind:"field",decorators:[i("#target_temperature")],key:"_targetTemperature",value:void 0},{kind:"method",key:"render",value:function(){return s`
      <div id="target_temperature">${this.value} ${this.unit}</div>
      <div class="control-buttons">
        <div>
          <ha-icon-button
            .path=${r}
            .label=${this.hass.localize("ui.components.climate-control.temperature_up")}
            @click=${this._incrementValue}
          >
          </ha-icon-button>
        </div>
        <div>
          <ha-icon-button
            .path=${n}
            .label=${this.hass.localize("ui.components.climate-control.temperature_down")}
            @click=${this._decrementValue}
          >
          </ha-icon-button>
        </div>
      </div>
    `}},{kind:"method",key:"updated",value:function(t){t.has("value")&&this._valueChanged()}},{kind:"method",key:"_temperatureStateInFlux",value:function(t){this._targetTemperature.classList.toggle("in-flux",t)}},{kind:"method",key:"_round",value:function(t){const e=this.step.toString().split(".");return e[1]?parseFloat(t.toFixed(e[1].length)):Math.round(t)}},{kind:"method",key:"_incrementValue",value:function(){const t=this._round(this.value+this.step);this._processNewValue(t)}},{kind:"method",key:"_decrementValue",value:function(){const t=this._round(this.value-this.step);this._processNewValue(t)}},{kind:"method",key:"_processNewValue",value:function(t){const e=v(t,this.min,this.max);this.value!==e&&(this.value=e,this._lastChanged=Date.now(),this._temperatureStateInFlux(!0))}},{kind:"method",key:"_valueChanged",value:function(){this._lastChanged&&window.setTimeout((()=>{Date.now()-this._lastChanged>=2e3&&(l(this,"change"),this._temperatureStateInFlux(!1),this._lastChanged=void 0)}),2010)}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: flex;
        justify-content: space-between;
      }
      .in-flux {
        color: var(--error-color);
      }
      #target_temperature {
        align-self: center;
        font-size: 28px;
        direction: ltr;
      }
      .control-buttons {
        font-size: 24px;
        text-align: right;
      }
      ha-icon-button {
        --mdc-icon-size: 32px;
      }
    `}}]}}),e);let j=t(null,(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"stateObj",value:void 0},{kind:"field",key:"_resizeDebounce",value:void 0},{kind:"method",key:"render",value:function(){if(!this.stateObj)return s``;const t=this.hass,e=this.stateObj,a=m(e,p),i=m(e,b),r=m(e,$),n=m(e,f),l=m(e,k),o=m(e,y),d=m(e,w),c=e.attributes.target_temp_step||(-1===t.config.unit_system.temperature.indexOf("F")?.5:1),h=_(t);return s`
      <div
        class=${u({"has-current_temperature":"current_temperature"in e.attributes,"has-current_humidity":"current_humidity"in e.attributes,"has-target_temperature":a,"has-target_temperature_range":i,"has-target_humidity":r,"has-fan_mode":n,"has-swing_mode":o,"has-aux_heat":d,"has-preset_mode":l})}
      >
        <div class="container-temperature">
          <div class=${e.state}>
            ${a||i?s`
                  <div>
                    ${t.localize("ui.card.climate.target_temperature")}
                  </div>
                `:""}
            ${void 0!==e.attributes.temperature&&null!==e.attributes.temperature?s`
                  <ha-climate-control
                    .hass=${this.hass}
                    .value=${e.attributes.temperature}
                    .unit=${t.config.unit_system.temperature}
                    .step=${c}
                    .min=${e.attributes.min_temp}
                    .max=${e.attributes.max_temp}
                    @change=${this._targetTemperatureChanged}
                  ></ha-climate-control>
                `:""}
            ${void 0!==e.attributes.target_temp_low&&null!==e.attributes.target_temp_low||void 0!==e.attributes.target_temp_high&&null!==e.attributes.target_temp_high?s`
                  <ha-climate-control
                    .hass=${this.hass}
                    .value=${e.attributes.target_temp_low}
                    .unit=${t.config.unit_system.temperature}
                    .step=${c}
                    .min=${e.attributes.min_temp}
                    .max=${e.attributes.target_temp_high}
                    class="range-control-left"
                    @change=${this._targetTemperatureLowChanged}
                  ></ha-climate-control>
                  <ha-climate-control
                    .hass=${this.hass}
                    .value=${e.attributes.target_temp_high}
                    .unit=${t.config.unit_system.temperature}
                    .step=${c}
                    .min=${e.attributes.target_temp_low}
                    .max=${e.attributes.max_temp}
                    class="range-control-right"
                    @change=${this._targetTemperatureHighChanged}
                  ></ha-climate-control>
                `:""}
          </div>
        </div>

        ${r?s`
              <div class="container-humidity">
                <div>${t.localize("ui.card.climate.target_humidity")}</div>
                <div class="single-row">
                  <div class="target-humidity">
                    ${e.attributes.humidity} %
                  </div>
                  <ha-slider
                    step="1"
                    pin
                    ignore-bar-touch
                    dir=${h}
                    .min=${e.attributes.min_humidity}
                    .max=${e.attributes.max_humidity}
                    .value=${e.attributes.humidity}
                    @change=${this._targetHumiditySliderChanged}
                  >
                  </ha-slider>
                </div>
              </div>
            `:""}

        <div class="container-hvac_modes">
          <div class="controls">
            <ha-select
              .label=${t.localize("ui.card.climate.operation")}
              .value=${e.state}
              fixedMenuPosition
              naturalMenuWidth
              @selected=${this._handleOperationmodeChanged}
              @closed=${g}
            >
              ${e.attributes.hvac_modes.concat().sort(x).map((e=>s`
                    <mwc-list-item .value=${e}>
                      ${t.localize(`component.climate.state._.${e}`)}
                    </mwc-list-item>
                  `))}
            </ha-select>
          </div>
        </div>

        ${l&&e.attributes.preset_modes?s`
              <div class="container-preset_modes">
                <ha-select
                  .label=${t.localize("ui.card.climate.preset_mode")}
                  .value=${e.attributes.preset_mode}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${this._handlePresetmodeChanged}
                  @closed=${g}
                >
                  ${e.attributes.preset_modes.map((e=>s`
                      <mwc-list-item .value=${e}>
                        ${t.localize(`state_attributes.climate.preset_mode.${e}`)||e}
                      </mwc-list-item>
                    `))}
                </ha-select>
              </div>
            `:""}
        ${n&&e.attributes.fan_modes?s`
              <div class="container-fan_list">
                <ha-select
                  .label=${t.localize("ui.card.climate.fan_mode")}
                  .value=${e.attributes.fan_mode}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${this._handleFanmodeChanged}
                  @closed=${g}
                >
                  ${e.attributes.fan_modes.map((e=>s`
                      <mwc-list-item .value=${e}>
                        ${t.localize(`state_attributes.climate.fan_mode.${e}`)||e}
                      </mwc-list-item>
                    `))}
                </ha-select>
              </div>
            `:""}
        ${o&&e.attributes.swing_modes?s`
              <div class="container-swing_list">
                <ha-select
                  .label=${t.localize("ui.card.climate.swing_mode")}
                  .value=${e.attributes.swing_mode}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${this._handleSwingmodeChanged}
                  @closed=${g}
                >
                  ${e.attributes.swing_modes.map((t=>s`
                      <mwc-list-item .value=${t}>${t}</mwc-list-item>
                    `))}
                </ha-select>
              </div>
            `:""}
        ${d?s`
              <div class="container-aux_heat">
                <div class="center horizontal layout single-row">
                  <div class="flex">
                    ${t.localize("ui.card.climate.aux_heat")}
                  </div>
                  <ha-switch
                    .checked=${"on"===e.attributes.aux_heat}
                    @change=${this._auxToggleChanged}
                  ></ha-switch>
                </div>
              </div>
            `:""}
      </div>
    `}},{kind:"method",key:"updated",value:function(t){c(h(i.prototype),"updated",this).call(this,t),t.has("stateObj")&&this.stateObj&&(this._resizeDebounce&&clearTimeout(this._resizeDebounce),this._resizeDebounce=window.setTimeout((()=>{l(this,"iron-resize"),this._resizeDebounce=void 0}),500))}},{kind:"method",key:"_targetTemperatureChanged",value:function(t){const e=t.target.value;this._callServiceHelper(this.stateObj.attributes.temperature,e,"set_temperature",{temperature:e})}},{kind:"method",key:"_targetTemperatureLowChanged",value:function(t){const e=t.currentTarget.value;this._callServiceHelper(this.stateObj.attributes.target_temp_low,e,"set_temperature",{target_temp_low:e,target_temp_high:this.stateObj.attributes.target_temp_high})}},{kind:"method",key:"_targetTemperatureHighChanged",value:function(t){const e=t.currentTarget.value;this._callServiceHelper(this.stateObj.attributes.target_temp_high,e,"set_temperature",{target_temp_low:this.stateObj.attributes.target_temp_low,target_temp_high:e})}},{kind:"method",key:"_targetHumiditySliderChanged",value:function(t){const e=t.target.value;this._callServiceHelper(this.stateObj.attributes.humidity,e,"set_humidity",{humidity:e})}},{kind:"method",key:"_auxToggleChanged",value:function(t){const e=t.target.checked;this._callServiceHelper("on"===this.stateObj.attributes.aux_heat,e,"set_aux_heat",{aux_heat:e})}},{kind:"method",key:"_handleFanmodeChanged",value:function(t){const e=t.target.value;this._callServiceHelper(this.stateObj.attributes.fan_mode,e,"set_fan_mode",{fan_mode:e})}},{kind:"method",key:"_handleOperationmodeChanged",value:function(t){const e=t.target.value;this._callServiceHelper(this.stateObj.state,e,"set_hvac_mode",{hvac_mode:e})}},{kind:"method",key:"_handleSwingmodeChanged",value:function(t){const e=t.target.value;this._callServiceHelper(this.stateObj.attributes.swing_mode,e,"set_swing_mode",{swing_mode:e})}},{kind:"method",key:"_handlePresetmodeChanged",value:function(t){const e=t.target.value||null;this._callServiceHelper(this.stateObj.attributes.preset_mode,e,"set_preset_mode",{preset_mode:e})}},{kind:"method",key:"_callServiceHelper",value:async function(t,e,a,i){if(t===e)return;i.entity_id=this.stateObj.entity_id;const s=this.stateObj;await this.hass.callService("climate",a,i),await new Promise((t=>setTimeout(t,2e3))),this.stateObj===s&&(this.stateObj=void 0,await this.updateComplete,void 0===this.stateObj&&(this.stateObj=s))}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        color: var(--primary-text-color);
      }

      ha-select {
        width: 100%;
        margin-top: 8px;
      }

      ha-slider {
        width: 100%;
      }

      .container-humidity .single-row {
        display: flex;
        height: 50px;
      }

      .target-humidity {
        width: 90px;
        font-size: 200%;
        margin: auto;
        direction: ltr;
      }

      ha-climate-control.range-control-left,
      ha-climate-control.range-control-right {
        float: left;
        width: 46%;
      }
      ha-climate-control.range-control-left {
        margin-right: 4%;
      }
      ha-climate-control.range-control-right {
        margin-left: 4%;
      }

      .single-row {
        padding: 8px 0;
      }
    `}}]}}),e);customElements.define("more-info-climate",j);
