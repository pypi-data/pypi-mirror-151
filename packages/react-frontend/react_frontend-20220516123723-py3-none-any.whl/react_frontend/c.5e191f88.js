import{_ as e,s as i,e as t,t as o,m as a,$ as c,f as n,n as s}from"./main-ac83c92b.js";import{X as l,Y as r,Z as h,_ as d,$ as m,a0 as p}from"./c.3e14cfd3.js";import{T as u,h as f}from"./c.027db416.js";import"./c.1fca9ca6.js";import"./c.11a6fda3.js";import{a as g}from"./c.1430be7b.js";import{b as _}from"./c.461e571b.js";import{c as j}from"./c.ad12eed4.js";import"./c.8cbd7110.js";import"./c.4e93087d.js";import"./c.8eddd911.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.958cb46c.js";import"./c.57c0073c.js";import"./c.cfa85e17.js";import"./c.c018532e.js";import"./c.53212acc.js";import"./c.0e001851.js";import"./c.8d0ef0b0.js";import"./c.d6711a1d.js";import"./c.622dfac1.js";import"./c.8786ad90.js";import"./c.be47aa9a.js";import"./c.39da0aeb.js";import"./c.02ed471c.js";import"./c.9e7e5aa1.js";import"./c.3eb3ee48.js";import"./c.6999bfff.js";import"./c.2541228c.js";import"./c.0225555d.js";import"./c.6e13c00f.js";import"./c.40d6516d.js";import"./c.4860f91b.js";import"./c.550b6e59.js";import"./c.3fc42334.js";import"./c.86ce6bc8.js";import"./c.e38196bb.js";import"./c.5756eeee.js";const v=l(_,r({entity:h(d()),name:h(d()),show_name:h(m()),icon:h(d()),show_icon:h(m()),icon_height:h(d()),tap_action:h(g),hold_action:h(g),theme:h(d()),show_state:h(m())})),b=["more-info","toggle","navigate","url","call-service","none"];let $=e([s("hui-button-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){p(e,v),this._config=e}},{kind:"field",key:"_schema",value:()=>a(((e,i,t)=>[{name:"entity",selector:{entity:{}}},{name:"",type:"grid",schema:[{name:"name",selector:{text:{}}},{name:"icon",selector:{icon:{placeholder:i||(null==t?void 0:t.attributes.icon),fallbackPath:i||null!=t&&t.attributes.icon||!t||!e?void 0:u(f(e),t)}}}]},{name:"",type:"grid",column_min_width:"100px",schema:[{name:"show_name",selector:{boolean:{}}},{name:"show_state",selector:{boolean:{}}},{name:"show_icon",selector:{boolean:{}}}]},{name:"",type:"grid",schema:[{name:"icon_height",selector:{text:{suffix:"px"}}},{name:"theme",selector:{theme:{}}}]}]))},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"more-info"}}},{kind:"method",key:"render",value:function(){var e;if(!this.hass||!this._config)return c``;const i=this._config.entity?this.hass.states[this._config.entity]:void 0,t=this._schema(this._config.entity,this._config.icon,i),o={show_name:!0,show_icon:!0,...this._config};return null!==(e=o.icon_height)&&void 0!==e&&e.includes("px")&&(o.icon_height=String(parseFloat(o.icon_height))),c`
      <ha-form
        .hass=${this.hass}
        .data=${o}
        .schema=${t}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <div class="card-config">
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._tap_action}
          .actions=${b}
          .configValue=${"tap_action"}
          .tooltipText=${this.hass.localize("ui.panel.lovelace.editor.card.button.default_action_help")}
          @value-changed=${this._actionChanged}
        ></hui-action-editor>
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._hold_action}
          .actions=${b}
          .configValue=${"hold_action"}
          .tooltipText=${this.hass.localize("ui.panel.lovelace.editor.card.button.default_action_help")}
          @value-changed=${this._actionChanged}
        ></hui-action-editor>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){const i=e.detail.value;i.icon_height&&!i.icon_height.endsWith("px")&&(i.icon_height+="px"),n(this,"config-changed",{config:i})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"entity"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.entity")}`:"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}},{kind:"method",key:"_actionChanged",value:function(e){if(!this._config||!this.hass)return;const i=e.target,t=e.detail.value;if(this[`_${i.configValue}`]===t)return;let o;i.configValue&&(!1===t||t?o={...this._config,[i.configValue]:t}:(o={...this._config},delete o[i.configValue])),n(this,"config-changed",{config:o})}},{kind:"get",static:!0,key:"styles",value:function(){return j}}]}}),i);export{$ as HuiButtonCardEditor};
