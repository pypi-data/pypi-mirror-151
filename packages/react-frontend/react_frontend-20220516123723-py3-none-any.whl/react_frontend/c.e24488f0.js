import{_ as e,s as a,e as o,t as i,$ as t,et as s,aA as r,ar as n,n as l}from"./main-ac83c92b.js";import"./c.027db416.js";import{b1 as c}from"./c.3e14cfd3.js";import"./c.9fa7d7aa.js";import{g as d,e as u}from"./c.9e1e758b.js";import{S as h}from"./c.02ed471c.js";import{severityMap as p}from"./c.90220dc5.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";import"./c.d4761680.js";e([l("hui-energy-solar-consumed-gauge-card")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[o({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"field",decorators:[i()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var e;return[d(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 4}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return t``;if(!this._data)return t`${this.hass.localize("ui.panel.lovelace.cards.energy.loading")}`;const e=this._data.prefs,a=u(e);if(!a.solar)return t``;const o=c(this._data.stats,a.solar.map((e=>e.stat_energy_from))),i=c(this._data.stats,a.grid[0].flow_to.map((e=>e.stat_energy_to)));let n;if(null!==i&&o){n=Math.max(0,o-i)/o*100}return t`
      <ha-card>
        ${void 0!==n?t`
              <ha-svg-icon id="info" .path=${s}></ha-svg-icon>
              <paper-tooltip animation-delay="0" for="info" position="left">
                <span>
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.solar_consumed_gauge.card_indicates_solar_energy_used")}
                  <br /><br />
                  ${this.hass.localize("ui.panel.lovelace.cards.energy.solar_consumed_gauge.card_indicates_solar_energy_used_charge_home_bat")}
                </span>
              </paper-tooltip>
              <ha-gauge
                min="0"
                max="100"
                .value=${n}
                .locale=${this.hass.locale}
                label="%"
                style=${r({"--gauge-color":this._computeSeverity(n)})}
              ></ha-gauge>
              <div class="name">
                ${this.hass.localize("ui.panel.lovelace.cards.energy.solar_consumed_gauge.self_consumed_solar_energy")}
              </div>
            `:0===o?this.hass.localize("ui.panel.lovelace.cards.energy.solar_consumed_gauge.not_produced_solar_energy"):this.hass.localize("ui.panel.lovelace.cards.energy.solar_consumed_gauge.self_consumed_solar_could_not_calc")}
      </ha-card>
    `}},{kind:"method",key:"_computeSeverity",value:function(e){return e>75?p.green:e<50?p.yellow:p.normal}},{kind:"get",static:!0,key:"styles",value:function(){return n`
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
    `}}]}}),h(a));
