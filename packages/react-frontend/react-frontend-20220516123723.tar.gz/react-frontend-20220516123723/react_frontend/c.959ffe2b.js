import{_ as e,s as a,e as t,t as i,$ as o,et as s,aA as n,ar as r,n as c}from"./main-ac83c92b.js";import"./c.027db416.js";import{aJ as d,b1 as l,b2 as h}from"./c.3e14cfd3.js";import"./c.9fa7d7aa.js";import{g as u,e as p}from"./c.9e1e758b.js";import{S as g}from"./c.02ed471c.js";import{severityMap as m}from"./c.90220dc5.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";import"./c.d4761680.js";e([c("hui-energy-carbon-consumed-gauge-card")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"field",decorators:[i()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"hassSubscribe",value:function(){var e;return[u(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return o``;if(!this._data)return o`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;if(!this._data.co2SignalEntity)return o``;if(!this.hass.states[this._data.co2SignalEntity])return o`<hui-warning>
        ${d(this.hass,this._data.co2SignalEntity)}
      </hui-warning>`;const e=this._data.prefs,a=p(e),t=l(this._data.stats,a.grid[0].flow_from.map((e=>e.stat_energy_from)));let i;if(0===t&&(i=100),this._data.fossilEnergyConsumption&&t){const e=this._data.fossilEnergyConsumption?Object.values(this._data.fossilEnergyConsumption).reduce(((e,a)=>e+a),0):0,o=a.solar&&l(this._data.stats,a.solar.map((e=>e.stat_energy_from)))||0,s=l(this._data.stats,a.grid[0].flow_to.map((e=>e.stat_energy_to)))||0,n=t+Math.max(0,o-s);i=h(100*(1-e/n))}return o`
      <ha-card>
        ${void 0!==i?o`
              <ha-svg-icon id="info" .path=${s}></ha-svg-icon>
              <paper-tooltip animation-delay="0" for="info" position="left">
                <span>
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.card_indicates_energy_used")}
                </span>
              </paper-tooltip>
              <ha-gauge
                min="0"
                max="100"
                .value=${i}
                .locale=${this.hass.locale}
                label="%"
                style=${n({"--gauge-color":this._computeSeverity(i)})}
              ></ha-gauge>
              <div class="name">
                ${this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.non_fossil_energy_consumed")}
              </div>
            `:o`${this.hass.localize("ui.panel.lovelace.cards.energy.carbon_consumed_gauge.non_fossil_energy_not_calculated")}`}
      </ha-card>
    `}},{kind:"method",key:"_computeSeverity",value:function(e){return e<10?m.red:e<30?m.yellow:e>75?m.green:m.normal}},{kind:"get",static:!0,key:"styles",value:function(){return r`
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
    `}}]}}),g(a));
