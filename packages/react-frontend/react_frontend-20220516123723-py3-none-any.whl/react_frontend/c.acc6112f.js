import{_ as i,s as e,e as t,t as a,m as o,$ as c,f as s,ar as n,n as r}from"./main-ac83c92b.js";import{X as l,Y as d,Z as h,_ as m,a0 as f}from"./c.3e14cfd3.js";import"./c.11a6fda3.js";import{a as u}from"./c.1430be7b.js";import{c as p}from"./c.ad12eed4.js";import{b as g}from"./c.461e571b.js";import{T as _,h as j}from"./c.027db416.js";import"./c.8cbd7110.js";import"./c.958cb46c.js";import"./c.57c0073c.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.4e93087d.js";import"./c.cfa85e17.js";import"./c.c018532e.js";import"./c.e9aa747b.js";import"./c.53212acc.js";import"./c.0e001851.js";import"./c.8d0ef0b0.js";import"./c.1fca9ca6.js";import"./c.8eddd911.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.d6711a1d.js";import"./c.622dfac1.js";import"./c.8786ad90.js";import"./c.be47aa9a.js";import"./c.39da0aeb.js";import"./c.02ed471c.js";import"./c.9e7e5aa1.js";import"./c.3eb3ee48.js";import"./c.6999bfff.js";import"./c.2541228c.js";import"./c.0225555d.js";import"./c.6e13c00f.js";import"./c.40d6516d.js";import"./c.4860f91b.js";import"./c.550b6e59.js";import"./c.3fc42334.js";import"./c.86ce6bc8.js";import"./c.e38196bb.js";import"./c.5756eeee.js";const b=l(g,d({name:h(m()),entity:h(m()),theme:h(m()),icon:h(m()),hold_action:h(u),double_tap_action:h(u)}));let v=i([r("hui-light-card-editor")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(i){f(i,b),this._config=i}},{kind:"field",key:"_schema",value:()=>o(((i,e,t)=>[{name:"entity",required:!0,selector:{entity:{domain:"light"}}},{type:"grid",name:"",schema:[{name:"name",selector:{text:{}}},{name:"icon",selector:{icon:{placeholder:e||(null==t?void 0:t.attributes.icon),fallbackPath:e||null!=t&&t.attributes.icon||!t?void 0:_(j(i),t)}}}]},{name:"theme",selector:{theme:{}}}]))},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"more-info"}}},{kind:"get",key:"_double_tap_action",value:function(){return this._config.double_tap_action}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return c``;const i=["more-info","toggle","navigate","url","call-service","none"],e=this.hass.states[this._config.entity],t=this._schema(this._config.entity,this._config.icon,e);return c`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${t}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <div class="card-config">
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._hold_action}
          .actions=${i}
          .configValue=${"hold_action"}
          @value-changed=${this._actionChanged}
        ></hui-action-editor>

        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.double_tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._double_tap_action}
          .actions=${i}
          .configValue=${"double_tap_action"}
          @value-changed=${this._actionChanged}
        ></hui-action-editor>
      </div>
    `}},{kind:"method",key:"_actionChanged",value:function(i){if(!this._config||!this.hass)return;const e=i.target,t=i.detail.value;this[`_${e.configValue}`]!==t&&(e.configValue&&(!1===t||t?this._config={...this._config,[e.configValue]:t}:(this._config={...this._config},delete this._config[e.configValue])),s(this,"config-changed",{config:this._config}))}},{kind:"method",key:"_valueChanged",value:function(i){s(this,"config-changed",{config:i.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return i=>"entity"===i.name?this.hass.localize("ui.panel.lovelace.editor.card.generic.entity"):"theme"===i.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${i.name}`)}},{kind:"field",static:!0,key:"styles",value:()=>[p,n`
      ha-form,
      hui-action-editor {
        display: block;
        margin-bottom: 24px;
        overflow: auto;
      }
    `]}]}}),e);export{v as HuiLightCardEditor};
