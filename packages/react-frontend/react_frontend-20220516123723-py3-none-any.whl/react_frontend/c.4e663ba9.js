import{_ as e,s as t,e as i,$ as s,aq as a,g as d,i as r,f as o,ar as n}from"./main-ac83c92b.js";import{z as u,e as l,s as h}from"./c.027db416.js";import"./c.3e14cfd3.js";import"./c.8cbd7110.js";let c=e(null,(function(e,t){class c extends t{constructor(...t){super(...t),e(this)}}return{F:c,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"stateObj",value:void 0},{kind:"field",key:"_resizeDebounce",value:void 0},{kind:"method",key:"render",value:function(){if(!this.stateObj)return s``;const e=this.hass,t=this.stateObj,i=u(t,1),d=l(e);return s`
      <div
        class=${a({"has-modes":i})}
      >
        <div class="container-humidity">
          <div>${e.localize("ui.card.humidifier.humidity")}</div>
          <div class="single-row">
            <div class="target-humidity">${t.attributes.humidity} %</div>
            <ha-slider
              step="1"
              pin
              ignore-bar-touch
              dir=${d}
              .min=${t.attributes.min_humidity}
              .max=${t.attributes.max_humidity}
              .value=${t.attributes.humidity}
              @change=${this._targetHumiditySliderChanged}
            >
            </ha-slider>
          </div>
        </div>

        ${i?s`
              <ha-select
                .label=${e.localize("ui.card.humidifier.mode")}
                .value=${t.attributes.mode}
                fixedMenuPosition
                naturalMenuWidth
                @selected=${this._handleModeChanged}
                @closed=${h}
              >
                ${t.attributes.available_modes.map((t=>s`
                    <mwc-list-item .value=${t}>
                      ${e.localize(`state_attributes.humidifier.mode.${t}`)||t}
                    </mwc-list-item>
                  `))}
              </ha-select>
            `:""}
      </div>
    `}},{kind:"method",key:"updated",value:function(e){d(r(c.prototype),"updated",this).call(this,e),e.has("stateObj")&&this.stateObj&&(this._resizeDebounce&&clearTimeout(this._resizeDebounce),this._resizeDebounce=window.setTimeout((()=>{o(this,"iron-resize"),this._resizeDebounce=void 0}),500))}},{kind:"method",key:"_targetHumiditySliderChanged",value:function(e){const t=e.target.value;this._callServiceHelper(this.stateObj.attributes.humidity,t,"set_humidity",{humidity:t})}},{kind:"method",key:"_handleModeChanged",value:function(e){const t=e.target.value||null;this._callServiceHelper(this.stateObj.attributes.mode,t,"set_mode",{mode:t})}},{kind:"method",key:"_callServiceHelper",value:async function(e,t,i,s){if(e===t)return;s.entity_id=this.stateObj.entity_id;const a=this.stateObj;await this.hass.callService("humidifier",i,s),await new Promise((e=>setTimeout(e,2e3))),this.stateObj===a&&(this.stateObj=void 0,await this.updateComplete,void 0===this.stateObj&&(this.stateObj=a))}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      :host {
        color: var(--primary-text-color);
      }

      ha-select {
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

      .single-row {
        padding: 8px 0;
      }
    `}}]}}),t);customElements.define("more-info-humidifier",c);
