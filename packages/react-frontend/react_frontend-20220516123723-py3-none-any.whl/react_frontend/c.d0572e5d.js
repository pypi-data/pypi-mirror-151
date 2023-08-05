import{_ as e,s as i,e as a,t,$ as r,et as o,ar as s,n}from"./main-ac83c92b.js";import"./c.027db416.js";import{b1 as l,Q as c}from"./c.3e14cfd3.js";import"./c.9fa7d7aa.js";import{g as d}from"./c.9e1e758b.js";import{S as u}from"./c.02ed471c.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";import"./c.d4761680.js";const g=[{level:-1,stroke:"var(--energy-grid-consumption-color)"},{level:0,stroke:"var(--energy-grid-return-color)"}];e([n("hui-energy-grid-neutrality-gauge-card")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"_config",value:void 0},{kind:"field",decorators:[t()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var e;return[d(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return r``;if(!this._data)return r`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;const e=this._data.prefs.energy_sources.find((e=>"grid"===e.type));let i;if(!e)return r``;const a=l(this._data.stats,e.flow_from.map((e=>e.stat_energy_from))),t=l(this._data.stats,e.flow_to.map((e=>e.stat_energy_to)));return null!==a&&null!==t&&(i=t>a?1-a/t:t<a?-1*(1-t/a):0),r`
      <ha-card>
        ${void 0!==i?r`
              <ha-svg-icon id="info" .path=${o}></ha-svg-icon>
              <paper-tooltip animation-delay="0" for="info" position="left">
                <span>
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.grid_neutrality_gauge.energy_dependency")}
                  <br /><br />
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.grid_neutrality_gauge.color_explain")}
                </span>
              </paper-tooltip>

              <ha-gauge
                min="-1"
                max="1"
                .value=${i}
                .valueText=${c(Math.abs(t-a),this.hass.locale,{maximumFractionDigits:2})}
                .locale=${this.hass.locale}
                .levels=${g}
                label="kWh"
                needle
              ></ha-gauge>
              <div class="name">
                ${t>=a?this.hass.localize("ui.panel.lovelace.cards.energy.grid_neutrality_gauge.net_returned_grid"):this.hass.localize("ui.panel.lovelace.cards.energy.grid_neutrality_gauge.net_consumed_grid")}
              </div>
            `:this.hass.localize("ui.panel.lovelace.cards.energy.grid_neutrality_gauge.grid_neutrality_not_calculated")}
      </ha-card>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return s`
      ha-card {
        height: 100%;
        overflow: hidden;
        padding: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-sizing: border-box;
      }

      ha-gauge {
        width: 100%;
        max-width: 250px;
      }

      .name {
        text-align: center;
        line-height: initial;
        color: var(--primary-text-color);
        width: 100%;
        font-size: 15px;
        margin-top: 8px;
      }

      ha-svg-icon {
        position: absolute;
        right: 4px;
        top: 4px;
        color: var(--secondary-text-color);
      }
      paper-tooltip > span {
        font-size: 12px;
        line-height: 12px;
      }
      paper-tooltip {
        width: 80%;
        max-width: 250px;
        top: 8px !important;
      }
    `}}]}}),u(i));
