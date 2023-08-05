import{_ as e,s as i,e as t,t as s,$ as a,f as o,ar as c,n}from"./main-ac83c92b.js";import"./c.1fca9ca6.js";import{X as r,Y as d,a2 as m,Z as h,_ as l,a7 as f,a0 as u}from"./c.3e14cfd3.js";import"./c.33355413.js";import{p}from"./c.cb759a4c.js";import{e as g}from"./c.60f8b094.js";import{b as _}from"./c.461e571b.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.027db416.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.8cbd7110.js";import"./c.6e13c00f.js";import"./c.53212acc.js";import"./c.cfa85e17.js";import"./c.0e001851.js";import"./c.1430be7b.js";const b=r(_,d({entities:m(g),title:h(l()),hours_to_show:h(f()),refresh_interval:h(f())})),j=[{name:"title",selector:{text:{}}},{name:"",type:"grid",schema:[{name:"hours_to_show",selector:{number:{min:1,mode:"box"}}},{name:"refresh_interval",selector:{number:{min:1,mode:"box"}}}]}];let k=e([n("hui-history-graph-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",decorators:[s()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(e){u(e,b),this._config=e,this._configEntities=p(e.entities)}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?a`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${j}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <hui-entity-editor
        .hass=${this.hass}
        .entities=${this._configEntities}
        @entities-changed=${this._entitiesChanged}
      ></hui-entity-editor>
    `:a``}},{kind:"method",key:"_valueChanged",value:function(e){o(this,"config-changed",{config:e.detail.value})}},{kind:"method",key:"_entitiesChanged",value:function(e){let i=this._config;i={...i,entities:e.detail.entities},this._configEntities=p(i.entities),o(this,"config-changed",{config:i})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}},{kind:"field",static:!0,key:"styles",value:()=>c`
    ha-form {
      margin-bottom: 24px;
    }
  `}]}}),i);export{k as HuiHistoryGraphCardEditor};
