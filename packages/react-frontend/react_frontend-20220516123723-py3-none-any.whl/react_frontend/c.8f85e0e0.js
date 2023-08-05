import{_ as e,s as i,e as a,t,$ as c,f as o,n as s}from"./main-ac83c92b.js";import{X as n,Y as r,Z as l,_ as d,$ as m,a0 as h}from"./c.3e14cfd3.js";import"./c.11a6fda3.js";import{a as p}from"./c.1430be7b.js";import{b as f}from"./c.461e571b.js";import{c as u}from"./c.ad12eed4.js";import"./c.027db416.js";import"./c.8cbd7110.js";import"./c.958cb46c.js";import"./c.57c0073c.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.4e93087d.js";import"./c.cfa85e17.js";import"./c.c018532e.js";import"./c.e9aa747b.js";import"./c.53212acc.js";import"./c.0e001851.js";import"./c.8d0ef0b0.js";import"./c.1fca9ca6.js";import"./c.8eddd911.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.d6711a1d.js";import"./c.622dfac1.js";import"./c.8786ad90.js";import"./c.be47aa9a.js";import"./c.39da0aeb.js";import"./c.02ed471c.js";import"./c.9e7e5aa1.js";import"./c.3eb3ee48.js";import"./c.6999bfff.js";import"./c.2541228c.js";import"./c.0225555d.js";import"./c.6e13c00f.js";import"./c.40d6516d.js";import"./c.4860f91b.js";import"./c.550b6e59.js";import"./c.3fc42334.js";import"./c.86ce6bc8.js";import"./c.e38196bb.js";import"./c.5756eeee.js";const g=n(f,r({entity:l(d()),image:l(d()),name:l(d()),camera_image:l(d()),camera_view:l(d()),aspect_ratio:l(d()),tap_action:l(p),hold_action:l(p),show_name:l(m()),show_state:l(m()),theme:l(d())})),_=[{name:"entity",required:!0,selector:{entity:{}}},{name:"name",selector:{text:{}}},{name:"image",selector:{text:{}}},{name:"camera_image",selector:{entity:{domain:"camera"}}},{name:"",type:"grid",schema:[{name:"camera_view",selector:{select:{options:["auto","live"]}}},{name:"aspect_ratio",selector:{text:{}}}]},{name:"",type:"grid",schema:[{name:"show_name",selector:{boolean:{}}},{name:"show_state",selector:{boolean:{}}}]},{name:"theme",selector:{theme:{}}}];let j=e([s("hui-picture-entity-card-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){h(e,g),this._config=e}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"more-info"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return c``;const e=["more-info","toggle","navigate","call-service","none"],i={show_state:!0,show_name:!0,camera_view:"auto",...this._config};return c`
      <ha-form
        .hass=${this.hass}
        .data=${i}
        .schema=${_}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
      <div class="card-config">
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._tap_action}
          .actions=${e}
          .configValue=${"tap_action"}
          @value-changed=${this._changed}
        ></hui-action-editor>
        <hui-action-editor
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass=${this.hass}
          .config=${this._hold_action}
          .actions=${e}
          .configValue=${"hold_action"}
          @value-changed=${this._changed}
        ></hui-action-editor>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){o(this,"config-changed",{config:e.detail.value})}},{kind:"method",key:"_changed",value:function(e){if(!this._config||!this.hass)return;const i=e.target,a=e.detail.value;this[`_${i.configValue}`]!==a&&(!1===a||a?this._config={...this._config,[i.configValue]:a}:(this._config={...this._config},delete this._config[i.configValue]),o(this,"config-changed",{config:this._config}))}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"entity"===e.name?this.hass.localize("ui.panel.lovelace.editor.card.generic.entity"):"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||this.hass.localize(`ui.panel.lovelace.editor.card.picture-entity.${e.name}`)}},{kind:"field",static:!0,key:"styles",value:()=>u}]}}),i);export{j as HuiPictureEntityCardEditor};
