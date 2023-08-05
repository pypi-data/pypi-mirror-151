import{_ as t,s as e,e as s,t as i,$ as o,ar as a}from"./main-ac83c92b.js";import{d as r}from"./c.4e93087d.js";import{a as n}from"./c.027db416.js";import{p as d,q as h}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";let u=t(null,(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"stateObj",value:void 0},{kind:"field",decorators:[i()],key:"_groupDomainStateObj",value:void 0},{kind:"field",decorators:[i()],key:"_moreInfoType",value:void 0},{kind:"method",key:"updated",value:function(t){if(!this.hass||!this.stateObj||!t.has("hass")&&!t.has("stateObj"))return;const e=this.stateObj.attributes.entity_id.map((t=>this.hass.states[t])).filter((t=>t));if(!e.length)return this._groupDomainStateObj=void 0,void(this._moreInfoType=void 0);const s=e.find((t=>"on"===t.state))||e[0],i=n(s);if("group"!==i&&e.every((t=>i===n(t)))){this._groupDomainStateObj={...s,entity_id:this.stateObj.entity_id,attributes:{...s.attributes}};const t=h(i);d(t),this._moreInfoType="hidden"===t?void 0:`more-info-${t}`}else this._groupDomainStateObj=void 0,this._moreInfoType=void 0}},{kind:"method",key:"render",value:function(){return this.hass&&this.stateObj?o`${this._moreInfoType?r(this._moreInfoType,{hass:this.hass,stateObj:this._groupDomainStateObj}):""}
    ${this.stateObj.attributes.entity_id.map((t=>{const e=this.hass.states[t];return e?o`
        <state-card-content
          .stateObj=${e}
          .hass=${this.hass}
        ></state-card-content>
      `:""}))}`:o``}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      state-card-content {
        display: block;
        margin-top: 8px;
      }
    `}}]}}),e);customElements.define("more-info-group",u);
