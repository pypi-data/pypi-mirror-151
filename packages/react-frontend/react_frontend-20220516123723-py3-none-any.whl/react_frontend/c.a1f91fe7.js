import{_ as t,s as i,e,t as o,$ as n,n as s}from"./main-ac83c92b.js";import{$ as a,h as r}from"./c.027db416.js";import{aE as c}from"./c.3e14cfd3.js";import"./c.0ab04093.js";import"./c.8cbd7110.js";import"./c.5ea5eadd.js";let d=t([s("hui-buttons-row")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"method",static:!0,key:"getStubConfig",value:function(){return{entities:[]}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(t){this._configEntities=c(t.entities).map((t=>({tap_action:{action:t.entity&&a.has(r(t.entity))?"toggle":"more-info"},hold_action:{action:"more-info"},...t})))}},{kind:"method",key:"render",value:function(){return n`
      <hui-buttons-base
        .hass=${this.hass}
        .configEntities=${this._configEntities}
      ></hui-buttons-base>
    `}}]}}),i);export{d as HuiButtonsRow};
