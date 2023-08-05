import{_ as e,s as i,e as t,t as o,m as s,$ as n,f as a,n as r,de as l,ap as d,g as h,i as c,ar as u}from"./main-ac83c92b.js";import{d as g,l as f}from"./c.d6711a1d.js";import{h as m}from"./c.c018532e.js";import{a0 as v,am as _}from"./c.3e14cfd3.js";import"./c.622dfac1.js";import"./c.1fca9ca6.js";import{h as p,T as y}from"./c.027db416.js";import{e as k}from"./c.60f8b094.js";const E={none:{},"entity-id":{},"last-changed":{},"last-updated":{},"last-triggered":{domains:["automation","script"]},position:{domains:["cover"]},"tilt-position":{domains:["cover"]},brightness:{domains:["light"]}};e([r("hui-generic-entity-row-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){v(e,k),this._config=e}},{kind:"field",key:"_schema",value:()=>s(((e,i,t,o)=>{const s=p(e);return[{name:"entity",required:!0,selector:{entity:{}}},{type:"grid",name:"",schema:[{name:"name",selector:{text:{}}},{name:"icon",selector:{icon:{placeholder:i||(null==t?void 0:t.attributes.icon),fallbackPath:i||null!=t&&t.attributes.icon||!t?void 0:y(s,t)}}}]},{name:"secondary_info",selector:{select:{options:Object.keys(E).filter((e=>!("domains"in E[e])||"domains"in E[e]&&E[e].domains.includes(s))).map((e=>({value:e,label:o(`ui.panel.lovelace.editor.card.entities.secondary_info_values.${e}`)})))}}}]}))},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return n``;const e=this.hass.states[this._config.entity],i=this._schema(this._config.entity,this._config.icon,e,this.hass.localize);return n`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${i}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){a(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"entity"===e.name?this.hass.localize("ui.panel.lovelace.editor.card.generic.entity"):this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)||this.hass.localize(`ui.panel.lovelace.editor.card.entity-row.${e.name}`)}}]}}),i);class w extends Error{constructor(e,i,t){super(e),l(this,"warnings",void 0),l(this,"errors",void 0),this.name="GUISupportError",this.warnings=i,this.errors=t}}let $=e(null,(function(e,i){class s extends i{constructor(...i){super(...i),e(this)}}return{F:s,d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[o()],key:"_yaml",value:void 0},{kind:"field",decorators:[o()],key:"_config",value:void 0},{kind:"field",decorators:[o()],key:"_configElement",value:void 0},{kind:"field",decorators:[o()],key:"_configElementType",value:void 0},{kind:"field",decorators:[o()],key:"_guiMode",value:()=>!0},{kind:"field",decorators:[o()],key:"_errors",value:void 0},{kind:"field",decorators:[o()],key:"_warnings",value:void 0},{kind:"field",decorators:[o()],key:"_guiSupported",value:void 0},{kind:"field",decorators:[o()],key:"_loading",value:()=>!1},{kind:"field",decorators:[d("ha-code-editor")],key:"_yamlEditor",value:void 0},{kind:"get",key:"yaml",value:function(){return this._yaml||(this._yaml=g(this._config)),this._yaml||""}},{kind:"set",key:"yaml",value:function(e){this._yaml=e;try{this._config=f(this.yaml),this._errors=void 0}catch(e){this._errors=[e.message]}this._setConfig()}},{kind:"get",key:"value",value:function(){return this._config}},{kind:"set",key:"value",value:function(e){this._config&&_(e,this._config)||(this._config=e,this._yaml=void 0,this._errors=void 0,this._setConfig())}},{kind:"method",key:"_setConfig",value:function(){var e;if(!this._errors)try{this._updateConfigElement()}catch(e){this._errors=[e.message]}a(this,"config-changed",{config:this.value,error:null===(e=this._errors)||void 0===e?void 0:e.join(", "),guiModeAvailable:!(this.hasWarning||this.hasError||!1===this._guiSupported)})}},{kind:"get",key:"hasWarning",value:function(){return void 0!==this._warnings&&this._warnings.length>0}},{kind:"get",key:"hasError",value:function(){return void 0!==this._errors&&this._errors.length>0}},{kind:"get",key:"GUImode",value:function(){return this._guiMode}},{kind:"set",key:"GUImode",value:function(e){this._guiMode=e,a(this,"GUImode-changed",{guiMode:e,guiModeAvailable:!(this.hasWarning||this.hasError||!1===this._guiSupported)})}},{kind:"method",key:"toggleMode",value:function(){this.GUImode=!this.GUImode}},{kind:"method",key:"focusYamlEditor",value:function(){var e,i;null!==(e=this._configElement)&&void 0!==e&&e.focusYamlEditor&&this._configElement.focusYamlEditor(),null!==(i=this._yamlEditor)&&void 0!==i&&i.codemirror&&this._yamlEditor.codemirror.focus()}},{kind:"method",key:"getConfigElement",value:async function(){}},{kind:"get",key:"configElementType",value:function(){return this.value?this.value.type:void 0}},{kind:"method",key:"render",value:function(){return n`
      <div class="wrapper">
        ${this.GUImode?n`
              <div class="gui-editor">
                ${this._loading?n`
                      <ha-circular-progress
                        active
                        alt="Loading"
                        class="center margin-bot"
                      ></ha-circular-progress>
                    `:this._configElement}
              </div>
            `:n`
              <div class="yaml-editor">
                <ha-code-editor
                  mode="yaml"
                  autofocus
                  autocomplete-entities
                  .hass=${this.hass}
                  .value=${this.yaml}
                  .error=${Boolean(this._errors)}
                  @value-changed=${this._handleYAMLChanged}
                  @keydown=${this._ignoreKeydown}
                  dir="ltr"
                ></ha-code-editor>
              </div>
            `}
        ${!1===this._guiSupported&&this.configElementType?n`
              <div class="info">
                ${this.hass.localize("ui.errors.config.editor_not_available","type",this.configElementType)}
              </div>
            `:""}
        ${this.hasError?n`
              <div class="error">
                ${this.hass.localize("ui.errors.config.error_detected")}:
                <br />
                <ul>
                  ${this._errors.map((e=>n`<li>${e}</li>`))}
                </ul>
              </div>
            `:""}
        ${this.hasWarning?n`
              <ha-alert
                alert-type="warning"
                .title="${this.hass.localize("ui.errors.config.editor_not_supported")}:"
              >
                ${this._warnings.length>0&&void 0!==this._warnings[0]?n` <ul>
                      ${this._warnings.map((e=>n`<li>${e}</li>`))}
                    </ul>`:""}
                ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
              </ha-alert>
            `:""}
      </div>
    `}},{kind:"method",key:"updated",value:function(e){h(c(s.prototype),"updated",this).call(this,e),this._configElement&&e.has("hass")&&(this._configElement.hass=this.hass),this._configElement&&"lovelace"in this._configElement&&e.has("lovelace")&&(this._configElement.lovelace=this.lovelace)}},{kind:"method",key:"_handleUIConfigChanged",value:function(e){e.stopPropagation();const i=e.detail.config;this.value=i}},{kind:"method",key:"_handleYAMLChanged",value:function(e){e.stopPropagation();const i=e.detail.value;i!==this.yaml&&(this.yaml=i)}},{kind:"method",key:"_updateConfigElement",value:async function(){if(!this.value)return;let e;try{if(this._errors=void 0,this._warnings=void 0,this._configElementType!==this.configElementType){if(this._guiSupported=void 0,this._configElement=void 0,!this.configElementType)throw new Error(this.hass.localize("ui.errors.config.no_type_provided"));this._configElementType=this.configElementType,this._loading=!0,e=await this.getConfigElement(),e&&(e.hass=this.hass,"lovelace"in e&&(e.lovelace=this.lovelace),e.addEventListener("config-changed",(e=>this._handleUIConfigChanged(e))),this._configElement=e,this._guiSupported=!0)}if(this._configElement)try{this._configElement.setConfig(this.value)}catch(e){const i=m(this.hass,e);throw new w("Config is not supported",i.warnings,i.errors)}else this._guiSupported=!1,this.GUImode=!1}catch(e){var i;if(e instanceof w)this._warnings=null!==(i=e.warnings)&&void 0!==i?i:[e.message],this._errors=e.errors||void 0;else this._errors=[e.message];this.GUImode=!1}finally{this._loading=!1}}},{kind:"method",key:"_ignoreKeydown",value:function(e){e.stopPropagation()}},{kind:"get",static:!0,key:"styles",value:function(){return u`
      :host {
        display: flex;
      }
      .wrapper {
        width: 100%;
      }
      .gui-editor,
      .yaml-editor {
        padding: 8px 0px;
      }
      ha-code-editor {
        --code-mirror-max-height: calc(100vh - 245px);
      }
      .error,
      .warning,
      .info {
        word-break: break-word;
        margin-top: 8px;
      }
      .error {
        color: var(--error-color);
      }
      .warning {
        color: var(--warning-color);
      }
      .warning ul,
      .error ul {
        margin: 4px 0;
      }
      .warning li,
      .error li {
        white-space: pre-wrap;
      }
      ha-circular-progress {
        display: block;
        margin: auto;
      }
    `}}]}}),i);export{$ as H};
