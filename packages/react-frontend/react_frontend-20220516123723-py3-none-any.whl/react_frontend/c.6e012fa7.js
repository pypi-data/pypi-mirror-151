import{_ as t,s,e as i,$ as a,a2 as e,ah as h,ac as r,dy as o,W as l,ar as n,n as c,c7 as d,a3 as u,dg as v,dz as b,e1 as m,e2 as p,e3 as $,e4 as g,e5 as w,dA as f,e6 as y,e7 as j,e8 as x,e9 as O}from"./main-ac83c92b.js";import{R as _,Q as k,T as V,U as z,V as D,W as U}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";const W={"clear-night":d,cloudy:u,exceptional:v,fog:b,hail:m,lightning:p,"lightning-rainy":$,partlycloudy:g,pouring:w,rainy:f,snowy:y,"snowy-rainy":j,sunny:x,windy:o,"windy-variant":O};t([c("more-info-weather")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"stateObj",value:void 0},{kind:"method",key:"shouldUpdate",value:function(t){if(t.has("stateObj"))return!0;const s=t.get("hass");return!s||s.locale!==this.hass.locale||s.config.unit_system!==this.hass.config.unit_system}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return a``;const t=_(this.stateObj.attributes.forecast);return a`
      <div class="flex">
        <ha-svg-icon .path=${e}></ha-svg-icon>
        <div class="main">
          ${this.hass.localize("ui.card.weather.attributes.temperature")}
        </div>
        <div>
          ${k(this.stateObj.attributes.temperature,this.hass.locale)}
          ${V(this.hass,"temperature")}
        </div>
      </div>
      ${this._showValue(this.stateObj.attributes.pressure)?a`
            <div class="flex">
              <ha-svg-icon .path=${h}></ha-svg-icon>
              <div class="main">
                ${this.hass.localize("ui.card.weather.attributes.air_pressure")}
              </div>
              <div>
                ${k(this.stateObj.attributes.pressure,this.hass.locale)}
                ${V(this.hass,"pressure")}
              </div>
            </div>
          `:""}
      ${this._showValue(this.stateObj.attributes.humidity)?a`
            <div class="flex">
              <ha-svg-icon .path=${r}></ha-svg-icon>
              <div class="main">
                ${this.hass.localize("ui.card.weather.attributes.humidity")}
              </div>
              <div>
                ${k(this.stateObj.attributes.humidity,this.hass.locale)}
                %
              </div>
            </div>
          `:""}
      ${this._showValue(this.stateObj.attributes.wind_speed)?a`
            <div class="flex">
              <ha-svg-icon .path=${o}></ha-svg-icon>
              <div class="main">
                ${this.hass.localize("ui.card.weather.attributes.wind_speed")}
              </div>
              <div>
                ${z(this.hass,this.stateObj.attributes.wind_speed,this.stateObj.attributes.wind_bearing)}
              </div>
            </div>
          `:""}
      ${this._showValue(this.stateObj.attributes.visibility)?a`
            <div class="flex">
              <ha-svg-icon .path=${l}></ha-svg-icon>
              <div class="main">
                ${this.hass.localize("ui.card.weather.attributes.visibility")}
              </div>
              <div>
                ${k(this.stateObj.attributes.visibility,this.hass.locale)}
                ${V(this.hass,"length")}
              </div>
            </div>
          `:""}
      ${this.stateObj.attributes.forecast?a`
            <div class="section">
              ${this.hass.localize("ui.card.weather.forecast")}:
            </div>
            ${this.stateObj.attributes.forecast.map((s=>this._showValue(s.templow)||this._showValue(s.temperature)?a`<div class="flex">
                    ${s.condition?a`
                          <ha-svg-icon
                            .path=${W[s.condition]}
                          ></ha-svg-icon>
                        `:""}
                    ${t?a`
                          <div class="main">
                            ${D(new Date(s.datetime),this.hass.locale)}
                          </div>
                        `:a`
                          <div class="main">
                            ${U(new Date(s.datetime),this.hass.locale)}
                          </div>
                        `}
                    <div class="templow">
                      ${this._showValue(s.templow)?`${k(s.templow,this.hass.locale)}\n                          ${V(this.hass,"temperature")}`:t?"":"—"}
                    </div>
                    <div class="temp">
                      ${this._showValue(s.temperature)?`${k(s.temperature,this.hass.locale)}\n                        ${V(this.hass,"temperature")}`:"—"}
                    </div>
                  </div>`:""))}
          `:""}
      ${this.stateObj.attributes.attribution?a`
            <div class="attribution">
              ${this.stateObj.attributes.attribution}
            </div>
          `:""}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      ha-svg-icon {
        color: var(--paper-item-icon-color);
      }
      .section {
        margin: 16px 0 8px 0;
        font-size: 1.2em;
      }

      .flex {
        display: flex;
        height: 32px;
        align-items: center;
      }

      .main {
        flex: 1;
        margin-left: 24px;
      }

      .temp,
      .templow {
        min-width: 48px;
        text-align: right;
      }

      .templow {
        margin: 0 16px;
        color: var(--secondary-text-color);
      }

      .attribution {
        color: var(--secondary-text-color);
        text-align: center;
      }
    `}},{kind:"method",key:"_showValue",value:function(t){return null!=t}}]}}),s);
