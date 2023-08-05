import{_ as t,s as e,e as a,t as s,$ as i,aq as o,m as r,ez as n,eA as d,eh as c,eB as l,eg as h,eC as u,ar as p,n as g}from"./main-ac83c92b.js";import{P as m,Q as f,b7 as y}from"./c.3e14cfd3.js";import{s as k,a as _,g as b,b as v}from"./c.9e1e758b.js";import{c as j}from"./c.027db416.js";import{S as x}from"./c.02ed471c.js";import{i as $}from"./c.b466e318.js";import{d as S,c as z}from"./c.d4761680.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";let C=t([g("hui-energy-gas-graph-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",decorators:[s()],key:"_chartData",value:()=>({datasets:[]})},{kind:"field",decorators:[s()],key:"_start",value:()=>k()},{kind:"field",decorators:[s()],key:"_end",value:()=>_()},{kind:"field",decorators:[s()],key:"_unit",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var t;return[b(this.hass,{key:null===(t=this._config)||void 0===t?void 0:t.collection_key}).subscribe((t=>this._getStatistics(t)))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){this._config=t}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?i`
      <ha-card>
        ${this._config.title?i`<h1 class="card-header">${this._config.title}</h1>`:""}
        <div
          class="content ${o({"has-header":!!this._config.title})}"
        >
          <ha-chart-base
            .data=${this._chartData}
            .options=${this._createOptions(this._start,this._end,this.hass.locale,this._unit)}
            chart-type="bar"
          ></ha-chart-base>
          ${this._chartData.datasets.length?"":i`<div class="no-data">
                ${$(this._start)?this.hass.localize("ui.panel.lovelace.cards.energy.no_data"):this.hass.localize("ui.panel.lovelace.cards.energy.no_data_period")}
              </div>`}
        </div>
      </ha-card>
    `:i``}},{kind:"field",key:"_createOptions",value:()=>r(((t,e,a,s)=>{const i=S(e,t);return{parsing:!1,animation:!1,scales:{x:{type:"time",suggestedMin:t.getTime(),suggestedMax:e.getTime(),adapters:{date:{locale:a}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:t=>t.tick&&t.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:i>35?"monthyear":i>7?"date":i>2?"weekday":i>0?"datetime":"hour",minUnit:i>35?"month":i>2?"day":"hour"},offset:!0},y:{stacked:!0,type:"linear",title:{display:!0,text:s},ticks:{beginAtZero:!0}}},plugins:{tooltip:{mode:"nearest",callbacks:{title:t=>{if(i>0)return t[0].label;const e=new Date(t[0].parsed.x);return`${m(e,a)} – ${m(z(e,1),a)}`},label:t=>`${t.dataset.label}: ${f(t.parsed.y,a)} ${s}`}},filler:{propagate:!1},legend:{display:!1,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{bar:{borderWidth:1.5,borderRadius:4},point:{hitRadius:5}},locale:y(a)}}))},{kind:"method",key:"_getStatistics",value:async function(t){const e=t.prefs.energy_sources.filter((t=>"gas"===t.type));this._unit=v(this.hass,t.prefs)||"m³";const a=[],s=getComputedStyle(this).getPropertyValue("--energy-gas-color").trim();e.forEach(((e,i)=>{const o=[],r=this.hass.states[e.stat_energy_from],p=i>0?this.hass.themes.darkMode?n(d(c(s)),i):l(d(c(s)),i):void 0,g=p?h(u(p)):s;let m=null,f=null;const y=[];if(e.stat_energy_from in t.stats){const a=t.stats[e.stat_energy_from];for(const t of a){if(null===t.sum)continue;if(null===m){m=t.sum;continue}if(f===t.start)continue;const e=t.sum-m,a=new Date(t.start);y.push({x:a.getTime(),y:e}),f=t.start,m=t.sum}}y.length&&o.push({label:r?j(r):e.stat_energy_from,borderColor:g,backgroundColor:g+"7F",data:y,stack:"gas"}),Array.prototype.push.apply(a,o)})),this._start=t.start,this._end=t.end||_(),this._chartData={datasets:a}}},{kind:"get",static:!0,key:"styles",value:function(){return p`
      ha-card {
        height: 100%;
      }
      .card-header {
        padding-bottom: 0;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
      .no-data {
        position: absolute;
        height: 100%;
        top: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20%;
        margin-left: 32px;
        box-sizing: border-box;
      }
    `}}]}}),x(e));export{C as HuiEnergyGasGraphCard};
