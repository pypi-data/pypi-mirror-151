import{_ as t,s as i,e,t as s,g as a,i as n,$ as o,aq as c,ar as h,n as r}from"./main-ac83c92b.js";import{aE as d,be as l,b5 as _}from"./c.3e14cfd3.js";import"./c.b57a34a6.js";import"./c.027db416.js";import"./c.8cbd7110.js";let u=t([r("hui-statistics-graph-card")],(function(t,i){class r extends i{constructor(...i){super(...i),t(this)}}return{F:r,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.6d3b7987.js"),document.createElement("hui-statistics-graph-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"statistics-graph",entities:[]}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_statistics",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",key:"_entities",value:()=>[]},{kind:"field",key:"_names",value:()=>({})},{kind:"field",key:"_fetching",value:()=>!1},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){a(n(r.prototype),"disconnectedCallback",this).call(this),this._interval&&(clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"connectedCallback",value:function(){a(n(r.prototype),"connectedCallback",this).call(this),this.hasUpdated&&(this._getStatistics(),clearInterval(this._interval),this._interval=window.setInterval((()=>this._getStatistics()),36e5))}},{kind:"method",key:"getCardSize",value:function(){var t,i;return null!==(t=this._config)&&void 0!==t&&t.title?2:0+2*((null===(i=this._entities)||void 0===i?void 0:i.length)||1)}},{kind:"method",key:"setConfig",value:function(t){if(!t.entities||!Array.isArray(t.entities))throw new Error("Entities need to be an array");if(!t.entities.length)throw new Error("You must include at least one entity");const i=t.entities?d(t.entities,!1):[];this._entities=[],i.forEach((t=>{this._entities.push(t.entity),t.name&&(this._names[t.entity]=t.name)})),"string"==typeof t.stat_types?this._config={...t,stat_types:[t.stat_types]}:t.stat_types?this._config=t:this._config={...t,stat_types:["sum","min","max","mean"]}}},{kind:"method",key:"shouldUpdate",value:function(t){return!!t.has("_statistics")||l(this,t)}},{kind:"method",key:"willUpdate",value:function(t){if(a(n(r.prototype),"willUpdate",this).call(this,t),!this._config||!t.has("_config"))return;const i=t.get("_config");(null==i?void 0:i.entities)===this._config.entities&&(null==i?void 0:i.days_to_show)===this._config.days_to_show&&(null==i?void 0:i.period)===this._config.period||(this._getStatistics(),clearInterval(this._interval),this._interval=window.setInterval((()=>this._getStatistics()),36e5))}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?o`
      <ha-card .header=${this._config.title}>
        <div
          class="content ${c({"has-header":!!this._config.title})}"
        >
          <statistics-chart
            .hass=${this.hass}
            .isLoadingData=${!this._statistics}
            .statisticsData=${this._statistics}
            .chartType=${this._config.chart_type||"line"}
            .statTypes=${this._config.stat_types}
            .names=${this._names}
          ></statistics-chart>
        </div>
      </ha-card>
    `:o``}},{kind:"method",key:"_getStatistics",value:async function(){if(this._fetching)return;const t=new Date;t.setTime(t.getTime()-36e5*(24*(this._config.days_to_show||30)+1)),this._fetching=!0;try{this._statistics=await _(this.hass,t,void 0,this._entities,this._config.period)}finally{this._fetching=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      ha-card {
        height: 100%;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
    `}}]}}),i);export{u as HuiStatisticsGraphCard};
