import{_ as e,s as t,e as r,t as a,$ as o,aq as s,m as i,ez as n,eA as d,eh as l,eB as c,eg as u,eC as _,ar as g,n as f}from"./main-ac83c92b.js";import{Q as h,P as y,b7 as m}from"./c.3e14cfd3.js";import{c as p}from"./c.027db416.js";import{s as b,a as k,g as v}from"./c.9e1e758b.js";import{S as j}from"./c.02ed471c.js";import{i as x}from"./c.b466e318.js";import{d as O,c as z}from"./c.d4761680.js";import"./c.8cbd7110.js";import"./c.85c615ca.js";import"./c.40d6516d.js";let S=e([f("hui-energy-usage-graph-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[r({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"field",decorators:[a()],key:"_chartData",value:()=>({datasets:[]})},{kind:"field",decorators:[a()],key:"_start",value:()=>b()},{kind:"field",decorators:[a()],key:"_end",value:()=>k()},{kind:"field",key:"hassSubscribeRequiredHostProps",value:()=>["_config"]},{kind:"method",key:"hassSubscribe",value:function(){var e;return[v(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>this._getStatistics(e)))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?o`
      <ha-card>
        ${this._config.title?o`<h1 class="card-header">${this._config.title}</h1>`:""}
        <div
          class="content ${s({"has-header":!!this._config.title})}"
        >
          <ha-chart-base
            .data=${this._chartData}
            .options=${this._createOptions(this._start,this._end,this.hass.locale)}
            chart-type="bar"
          ></ha-chart-base>
          ${this._chartData.datasets.some((e=>e.data.length))?"":o`<div class="no-data">
                ${x(this._start)?this.hass.localize("ui.panel.lovelace.cards.energy.no_data"):this.hass.localize("ui.panel.lovelace.cards.energy.no_data_period")}
              </div>`}
        </div>
      </ha-card>
    `:o``}},{kind:"field",key:"_createOptions",value(){return i(((e,t,r)=>{const a=O(t,e);return{parsing:!1,animation:!1,scales:{x:{type:"time",suggestedMin:e.getTime(),suggestedMax:t.getTime(),adapters:{date:{locale:r}},ticks:{maxRotation:0,sampleSize:5,autoSkipPadding:20,major:{enabled:!0},font:e=>e.tick&&e.tick.major?{weight:"bold"}:{}},time:{tooltipFormat:a>35?"monthyear":a>7?"date":a>2?"weekday":a>0?"datetime":"hour",minUnit:a>35?"month":a>2?"day":"hour"},offset:!0},y:{stacked:!0,type:"linear",title:{display:!0,text:"kWh"},ticks:{beginAtZero:!0,callback:e=>h(Math.abs(e),r)}}},plugins:{tooltip:{mode:"x",intersect:!0,position:"nearest",filter:e=>"0"!==e.formattedValue,callbacks:{title:e=>{if(a>0)return e[0].label;const t=new Date(e[0].parsed.x);return`${y(t,r)} – ${y(z(t,1),r)}`},label:e=>`${e.dataset.label}: ${h(Math.abs(e.parsed.y),r)} kWh`,footer:e=>{let t=0,a=0;for(const r of e){const e=r.dataset.data[r.dataIndex].y;e>0?t+=e:a+=Math.abs(e)}return[t?this.hass.localize("ui.panel.lovelace.cards.energy.energy_usage_graph.total_consumed",{num:h(t,r)}):"",a?this.hass.localize("ui.panel.lovelace.cards.energyenergy_usage_graph.total_returned",{num:h(a,r)}):""].filter(Boolean)}}},filler:{propagate:!1},legend:{display:!1,labels:{usePointStyle:!0}}},hover:{mode:"nearest"},elements:{bar:{borderWidth:1.5,borderRadius:4},point:{hitRadius:5}},locale:m(r)}}))}},{kind:"method",key:"_getStatistics",value:async function(e){const t=[],r={};for(const t of e.prefs.energy_sources)if("solar"!==t.type)if("battery"!==t.type){if("grid"===t.type){for(const e of t.flow_from)r.from_grid?r.from_grid.push(e.stat_energy_from):r.from_grid=[e.stat_energy_from];for(const e of t.flow_to)r.to_grid?r.to_grid.push(e.stat_energy_to):r.to_grid=[e.stat_energy_to]}}else r.to_battery?(r.to_battery.push(t.stat_energy_to),r.from_battery.push(t.stat_energy_from)):(r.to_battery=[t.stat_energy_to],r.from_battery=[t.stat_energy_from]);else r.solar?r.solar.push(t.stat_energy_from):r.solar=[t.stat_energy_from];this._start=e.start,this._end=e.end||k();const a={},o={},s=getComputedStyle(this),i={to_grid:s.getPropertyValue("--energy-grid-return-color").trim(),to_battery:s.getPropertyValue("--energy-battery-in-color").trim(),from_grid:s.getPropertyValue("--energy-grid-consumption-color").trim(),used_grid:s.getPropertyValue("--energy-grid-consumption-color").trim(),used_solar:s.getPropertyValue("--energy-solar-color").trim(),used_battery:s.getPropertyValue("--energy-battery-out-color").trim()},g={used_grid:this.hass.localize("ui.panel.lovelace.cards.energy.energy_usage_graph.combined_from_grid"),used_solar:this.hass.localize("ui.panel.lovelace.cards.energy.energy_usage_graph.consumed_solar"),used_battery:this.hass.localize("ui.panel.lovelace.cards.energy.energy_usage_graph.consumed_battery")};Object.entries(r).forEach((([t,r])=>{const s=["solar","to_grid","from_grid","to_battery","from_battery"].includes(t),i=!["solar","from_battery"].includes(t),n={},d={};r.forEach((t=>{const r=e.stats[t];if(!r)return;const a={};let o;r.forEach((e=>{if(null===e.sum)return;if(void 0===o)return void(o=e.sum);const t=e.sum-o;s&&(n[e.start]=e.start in n?n[e.start]+t:t),i&&!(e.start in a)&&(a[e.start]=t),o=e.sum})),d[t]=a})),s&&(o[t]=n),i&&(a[t]=d)}));const f={},h={};if((o.to_grid||o.to_battery)&&o.solar){const e={};for(const t of Object.keys(o.solar)){var y,m;if(e[t]=(o.solar[t]||0)-((null===(y=o.to_grid)||void 0===y?void 0:y[t])||0)-((null===(m=o.to_battery)||void 0===m?void 0:m[t])||0),e[t]<0){var b,v,j;if(o.to_battery)if(f[t]=-1*e[t],f[t]>((null===(b=o.from_grid)||void 0===b?void 0:b[t])||0))h[t]=Math.min(0,f[t]-((null===(v=o.from_grid)||void 0===v?void 0:v[t])||0)),f[t]=null===(j=o.from_grid)||void 0===j?void 0:j[t];e[t]=0}}a.used_solar={used_solar:e}}if(o.from_battery)if(o.to_grid){const e={};for(const t of Object.keys(o.from_battery))e[t]=(o.from_battery[t]||0)-(h[t]||0);a.used_battery={used_battery:e}}else a.used_battery={used_battery:o.from_battery};if(a.from_grid&&o.to_battery){const e={};for(const t of Object.keys(f)){let r,o=0;for(const[e,s]of Object.entries(a.from_grid))if(s[t]&&(r=e,o++),o>1)break;if(1===o)a.from_grid[r][t]-=f[t]||0;else{let r=0;Object.values(a.from_grid).forEach((e=>{r+=e[t]||0,delete e[t]})),e[t]=r-(f[t]||0)}}a.used_grid={used_grid:e}}let x=[];Object.values(a).forEach((e=>{Object.values(e).forEach((e=>{x=x.concat(Object.keys(e))}))}));const O=Array.from(new Set(x));Object.entries(a).forEach((([e,r])=>{Object.entries(r).forEach((([r,o],s)=>{const f=[],h=this.hass.states[r],y=s>0?this.hass.themes.darkMode?n(d(l(i[e])),s):c(d(l(i[e])),s):void 0,m=y?u(_(y)):i[e];f.push({label:e in g?g[e]:h?p(h):r,order:"used_solar"===e?0:"to_battery"===e?Object.keys(a).length:s+1,borderColor:m,backgroundColor:m+"7F",stack:"stack",data:[]});for(const t of O){const r=o[t]||0,a=new Date(t);f[0].data.push({x:a.getTime(),y:r&&["to_grid","to_battery"].includes(e)?-1*r:r})}Array.prototype.push.apply(t,f)}))})),this._chartData={datasets:t}}},{kind:"get",static:!0,key:"styles",value:function(){return g`
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
    `}}]}}),j(t));export{S as HuiEnergyUsageGraphCard};
