import{_ as e,s as t,e as a,t as s,$ as r,aq as i,m as o,ez as n,eA as l,eh as c,eB as d,eg as h,eC as u,ar as p,n as f}from"./main-ac83c92b.js";import{P as g,Q as m,b7 as y}from"./c.3e14cfd3.js";import{c as _}from"./c.027db416.js";import{s as b,a as k,g as v,c as j}from"./c.9e1e758b.js";import{S as x}from"./c.02ed471c.js";import{i as $}from"./c.b466e318.js";import{d as D,c as S}from"./c.d4761680.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";let w=e([f("hui-energy-solar-graph-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",decorators:[s()],key:"_chartData",value:()=>({datasets:[]})},{kind:"field",decorators:[s()],key:"_start",value:()=>b()},{kind:"field",decorators:[s()],key:"_end",value:()=>k()},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var e;return[v(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>this._getStatistics(e)))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?r`
      <ha-card>
        ${this._config.title?r`<h1 class="card-header">${this._config.title}</h1>`:""}
        <div
          class="content ${i({"has-header":!!this._config.title})}"
        >
          <ha-chart-base
            .data=${this._chartData}
            .options=${this._createOptions(this._start,this._end,this.hass.locale)}
            chart-type="bar"
          ></ha-chart-base>
          ${this._chartData.datasets.length?"":r`<div class="no-data">
                ${$(this._start)?this.hass.localize("ui.panel.lovelace.cards.energy.no_data"):this.hass.localize("ui.panel.lovelace.cards.energy.no_data_period")}
              </div>`}
        </div>
      </ha-card>
    `:r``}},{kind:"field",key:"_createOptions",value:()=>o(((e,t,a)=>{const s=D(t,e);return{parsing:!1,animation:!1,scales:{x:{type:"time",suggestedMin:e.getTime(),suggestedMax:t.getTime(),adapters:{date:{locale:a}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:e=>e.tick&&e.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:s>35?"monthyear":s>7?"date":s>2?"weekday":s>0?"datetime":"hour",minUnit:s>35?"month":s>2?"day":"hour"},offset:!0},y:{stacked:!0,type:"linear",title:{display:!0,text:"kWh"},ticks:{beginAtZero:!0}}},plugins:{tooltip:{mode:"nearest",callbacks:{title:e=>{if(s>0)return e[0].label;const t=new Date(e[0].parsed.x);return`${g(t,a)} – ${g(S(t,1),a)}`},label:e=>`${e.dataset.label}: ${m(e.parsed.y,a)} kWh`}},filler:{propagate:!1},legend:{display:!1,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{line:{tension:.3,borderWidth:1.5},bar:{borderWidth:1.5,borderRadius:4},point:{hitRadius:5}},locale:y(a)}}))},{kind:"method",key:"_getStatistics",value:async function(e){const t=e.prefs.energy_sources.filter((e=>"solar"===e.type));let a;if(t.some((e=>{var t;return null===(t=e.config_entry_solar_forecast)||void 0===t?void 0:t.length})))try{a=await j(this.hass)}catch(e){}const s=[],r=getComputedStyle(this),i=r.getPropertyValue("--energy-solar-color").trim(),o=D(e.end||new Date,e.start);t.forEach(((t,p)=>{const f=[],g=this.hass.states[t.stat_energy_from],m=p>0?this.hass.themes.darkMode?n(l(c(i)),p):d(l(c(i)),p):void 0,y=m?h(u(m)):i;let b=null,k=null;const v=[];if(t.stat_energy_from in e.stats){const a=e.stats[t.stat_energy_from];for(const e of a){if(null===e.sum)continue;if(null===b){b=e.sum;continue}if(k===e.start)continue;const t=e.sum-b,a=new Date(e.start);v.push({x:a.getTime(),y:t}),k=e.start,b=e.sum}}if(v.length&&f.push({label:this.hass.localize("ui.panel.lovelace.cards.energy.energy_solar_graph.production",{name:g?_(g):t.stat_energy_from}),borderColor:y,backgroundColor:y+"7F",data:v,stack:"solar"}),a&&t.config_entry_solar_forecast){const s={};if(t.config_entry_solar_forecast.forEach((t=>{a[t]&&Object.entries(a[t].wh_hours).forEach((([t,a])=>{const r=new Date(t);if(r<e.start||e.end&&r>e.end)return;o>35&&r.setDate(1),o>2?r.setHours(0,0,0,0):r.setMinutes(0,0,0);const i=r.getTime();i in s?s[i]+=a:s[i]=a}))})),s){const e=[];for(const[t,a]of Object.entries(s))e.push({x:Number(t),y:a/1e3});e.length&&f.push({type:"line",label:this.hass.localize("ui.panel.lovelace.cards.energy.energy_solar_graph.forecast",{name:g?_(g):t.stat_energy_from}),fill:!1,stepped:!1,borderColor:r.getPropertyValue("--primary-text-color"),borderDash:[7,5],pointRadius:0,data:e})}}Array.prototype.push.apply(s,f)})),this._start=e.start,this._end=e.end||k(),this._chartData={datasets:s}}},{kind:"get",static:!0,key:"styles",value:function(){return p`
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
    `}}]}}),x(t));export{w as HuiEnergySolarGraphCard};
