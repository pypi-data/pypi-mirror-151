import{_ as e,s as t,e as i,t as o,$ as r,aq as s,ar as n,n as a}from"./main-ac83c92b.js";import{h as d}from"./c.027db416.js";import{aE as c}from"./c.3e14cfd3.js";import"./c.0ab04093.js";import"./c.8cbd7110.js";import"./c.5ea5eadd.js";let l=e([a("hui-buttons-header-footer")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",static:!0,key:"getStubConfig",value:function(){return{entities:[]}}},{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"type",value:void 0},{kind:"field",decorators:[o()],key:"_configEntities",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._configEntities=c(e.entities).map((e=>{const t={tap_action:{action:"toggle"},hold_action:{action:"more-info"},...e};return"scene"===d(e.entity)&&(t.tap_action={action:"call-service",service:"scene.turn_on",target:{entity_id:t.entity}}),t}))}},{kind:"method",key:"render",value:function(){return r`
      ${"footer"===this.type?r`<li class="divider footer" role="separator"></li>`:""}
      <hui-buttons-base
        .hass=${this.hass}
        .configEntities=${this._configEntities}
        class=${s({footer:"footer"===this.type,header:"header"===this.type})}
      ></hui-buttons-base>
      ${"header"===this.type?r`<li class="divider header" role="separator"></li>`:""}
    `}},{kind:"field",static:!0,key:"styles",value:()=>n`
    .divider {
      height: 0;
      margin: 16px 0;
      list-style-type: none;
      border: none;
      border-bottom-width: 1px;
      border-bottom-style: solid;
      border-bottom-color: var(--divider-color);
    }
    .divider.header {
      margin-top: 0;
    }
    hui-buttons-base.footer {
      --padding-bottom: 16px;
    }
    hui-buttons-base.header {
      --padding-top: 16px;
    }
  `}]}}),t);export{l as HuiButtonsHeaderFooter};
