import{_ as i,s as e,t as r,$ as o,aA as n,ar as t,n as d}from"./main-ac83c92b.js";i([d("hui-divider-row")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[r()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(i){if(!i)throw new Error("Error in card configuration.");this._config=i}},{kind:"method",key:"render",value:function(){return this._config?o`<div
      style=${this._config.style?n(this._config.style):""}
    ></div>`:o``}},{kind:"get",static:!0,key:"styles",value:function(){return t`
      div {
        height: 1px;
        background-color: var(--entities-divider-color, var(--divider-color));
      }
    `}}]}}),e);
