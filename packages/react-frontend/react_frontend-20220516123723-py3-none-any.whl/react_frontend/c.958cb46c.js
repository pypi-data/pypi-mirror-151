import{_ as e,s as t,e as i,$ as a,f as o,n,ec as s,h as d,ar as l,t as r,cu as c,g as u,i as h,m as v,ap as k,aq as p,ed as m,ee as g,aA as y,cD as f,ef as _,bu as b,bw as $,eg as x,eh as w,ei as C,ej as z,ek as P,cJ as F,ea as A,W as D,eb as q}from"./main-ac83c92b.js";import{_ as T,k as M,c as U,a as E,z as L,d as I,i as B,g as O,h as j,an as N}from"./c.027db416.js";import{Y as S,_ as V,Z as W,a7 as R,a3 as K,a1 as Y,a0 as X,d as G,a8 as H,D as J,a9 as Z,a6 as Q,aa as ee,ab as te,X as ie,ac as ae,ad as oe,ae as ne,af as se}from"./c.3e14cfd3.js";import{d as de}from"./c.57c0073c.js";import"./c.c8193d47.js";import{d as le}from"./c.4e93087d.js";import{s as re,c as ce}from"./c.cfa85e17.js";import{h as ue}from"./c.c018532e.js";import"./c.e9aa747b.js";import"./c.53212acc.js";import{e as he}from"./c.8d0ef0b0.js";import"./c.1fca9ca6.js";import{D as ve,d as ke,l as pe}from"./c.d6711a1d.js";import"./c.622dfac1.js";import{a as me,s as ge}from"./c.8786ad90.js";import"./c.be47aa9a.js";import"./c.9e7e5aa1.js";import"./c.0e001851.js";import{b as ye,e as fe}from"./c.3eb3ee48.js";import{s as _e}from"./c.6999bfff.js";import{e as be}from"./c.2541228c.js";import"./c.0225555d.js";import{i as $e}from"./c.6e13c00f.js";import{g as xe}from"./c.40d6516d.js";import"./c.4860f91b.js";import{S as we}from"./c.02ed471c.js";import"./c.25e73c3c.js";import"./c.550b6e59.js";import"./c.3fc42334.js";import{c as Ce}from"./c.5ea5eadd.js";import{a as ze,s as Pe,c as Fe}from"./c.39da0aeb.js";import"./c.86ce6bc8.js";import"./c.e38196bb.js";import"./c.5756eeee.js";import"./c.8cbd7110.js";import"./c.47fa9be3.js";import"./c.8eddd911.js";import"./c.8e198788.js";const Ae=(e,t)=>e.callWS({type:"validate_config",...t}),De=["scene"];e([n("ha-automation-action-activate_scene")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{service:"scene.turn_on",target:{entity_id:""},metadata:{}}}},{kind:"method",key:"render",value:function(){let e;var t;"scene"in this.action?e=this.action.scene:e=null===(t=this.action.target)||void 0===t?void 0:t.entity_id;return a`
      <ha-entity-picker
        .hass=${this.hass}
        .value=${e}
        @value-changed=${this._entityPicked}
        .includeDomains=${De}
        allow-custom-entity
      ></ha-entity-picker>
    `}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{service:"scene.turn_on",target:{entity_id:e.detail.value},metadata:{}}})}}]}}),t),e([n("ha-automation-action-choose")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{choose:[{conditions:[],sequence:[]}],default:[]}}},{kind:"method",key:"render",value:function(){const e=this.action;return a`
      ${(e.choose?he(e.choose):[]).map(((e,t)=>a`<ha-card>
          <ha-icon-button
            .idx=${t}
            @click=${this._removeOption}
            .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.remove_option")}
            .path=${s}
          ></ha-icon-button>
          <div class="card-content">
            <h2>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.option","number",t+1)}:
            </h2>
            <h3>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.conditions")}:
            </h3>
            <ha-automation-condition
              .conditions=${e.conditions}
              .hass=${this.hass}
              .idx=${t}
              @value-changed=${this._conditionChanged}
            ></ha-automation-condition>
            <h3>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.sequence")}:
            </h3>
            <ha-form
              .hass=${this.hass}
              .schema=${[{name:"sequence",selector:{action:{}}}]}
              .data=${e}
              .idx=${t}
              @value-changed=${this._actionChanged}
            ></ha-form>
          </div>
        </ha-card>`))}
      <ha-card>
        <div class="card-actions add-card">
          <mwc-button @click=${this._addOption}>
            ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.add_option")}
          </mwc-button>
        </div>
      </ha-card>
      <h2>
        ${this.hass.localize("ui.panel.config.automation.editor.actions.type.choose.default")}:
      </h2>
      <ha-automation-action
        .actions=${e.default||[]}
        @value-changed=${this._defaultChanged}
        .hass=${this.hass}
      ></ha-automation-action>
    `}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation();const t=e.detail.value,i=e.target.idx,a=this.action.choose?[...he(this.action.choose)]:[];a[i].conditions=t,o(this,"value-changed",{value:{...this.action,choose:a}})}},{kind:"method",key:"_actionChanged",value:function(e){e.stopPropagation();const t=e.detail.value.sequence,i=e.target.idx,a=this.action.choose?[...he(this.action.choose)]:[];a[i].sequence=t,o(this,"value-changed",{value:{...this.action,choose:a}})}},{kind:"method",key:"_addOption",value:function(){const e=this.action.choose?[...he(this.action.choose)]:[];e.push({conditions:[],sequence:[]}),o(this,"value-changed",{value:{...this.action,choose:e}})}},{kind:"method",key:"_removeOption",value:function(e){const t=e.currentTarget.idx,i=this.action.choose?[...he(this.action.choose)]:[];i.splice(t,1),o(this,"value-changed",{value:{...this.action,choose:i}})}},{kind:"method",key:"_defaultChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:{...this.action,default:t}})}},{kind:"get",static:!0,key:"styles",value:function(){return[d,l`
        ha-card {
          margin-top: 16px;
        }
        .add-card mwc-button {
          display: block;
          text-align: center;
        }
        ha-icon-button {
          position: absolute;
          right: 0;
          padding: 4px;
        }
        ha-form::part(root) {
          overflow: visible;
        }
      `]}}]}}),t);e([n("ha-yaml-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"yamlSchema",value:()=>ve},{kind:"field",decorators:[i()],key:"defaultValue",value:void 0},{kind:"field",decorators:[i()],key:"isValid",value:()=>!0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[r()],key:"_yaml",value:()=>""},{kind:"method",key:"setValue",value:function(e){try{this._yaml=e&&!(e=>{if("object"!=typeof e)return!1;for(const t in e)if(Object.prototype.hasOwnProperty.call(e,t))return!1;return!0})(e)?ke(e,{schema:this.yamlSchema}):""}catch(t){console.error(t,e),alert(`There was an error converting to YAML: ${t}`)}}},{kind:"method",key:"firstUpdated",value:function(){this.defaultValue&&this.setValue(this.defaultValue)}},{kind:"method",key:"render",value:function(){return void 0===this._yaml?a``:a`
      ${this.label?a`<p>${this.label}${this.required?"*":""}</p>`:""}
      <ha-code-editor
        .hass=${this.hass}
        .value=${this._yaml}
        .readOnly=${this.readOnly}
        mode="yaml"
        autocomplete-entities
        .error=${!1===this.isValid}
        @value-changed=${this._onChange}
        dir="ltr"
      ></ha-code-editor>
    `}},{kind:"method",key:"_onChange",value:function(e){let t;e.stopPropagation(),this._yaml=e.detail.value;let i=!0;if(this._yaml)try{t=pe(this._yaml,{schema:this.yamlSchema})}catch(e){i=!1}else t={};this.value=t,this.isValid=i,o(this,"value-changed",{value:t,isValid:i})}},{kind:"get",key:"yaml",value:function(){return this._yaml}}]}}),t);e([n("ha-automation-condition-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"condition",value:void 0},{kind:"field",decorators:[r()],key:"_yamlMode",value:()=>!1},{kind:"field",decorators:[r()],key:"_warnings",value:void 0},{kind:"method",key:"render",value:function(){return this.condition?a`
      <ha-card>
        <div class="card-content">
          <div class="card-menu">
            <ha-progress-button @click=${this._testCondition}>
              ${this.hass.localize("ui.panel.config.automation.editor.conditions.test")}
            </ha-progress-button>
            <ha-button-menu corner="BOTTOM_START" @action=${this._handleAction}>
              <ha-icon-button
                slot="trigger"
                .label=${this.hass.localize("ui.common.menu")}
                .path=${c}
              >
              </ha-icon-button>
              <mwc-list-item>
                ${this._yamlMode?this.hass.localize("ui.panel.config.automation.editor.edit_ui"):this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
              </mwc-list-item>
              <mwc-list-item>
                ${this.hass.localize("ui.panel.config.automation.editor.actions.duplicate")}
              </mwc-list-item>
              <mwc-list-item class="warning">
                ${this.hass.localize("ui.panel.config.automation.editor.actions.delete")}
              </mwc-list-item>
            </ha-button-menu>
          </div>
          ${this._warnings?a`<ha-alert
                alert-type="warning"
                .title=${this.hass.localize("ui.errors.config.editor_not_supported")}
              >
                ${this._warnings.length>0&&void 0!==this._warnings[0]?a` <ul>
                      ${this._warnings.map((e=>a`<li>${e}</li>`))}
                    </ul>`:""}
                ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
              </ha-alert>`:""}
          <ha-automation-condition-editor
            @ui-mode-not-available=${this._handleUiModeNotAvailable}
            @value-changed=${this._handleChangeEvent}
            .yamlMode=${this._yamlMode}
            .hass=${this.hass}
            .condition=${this.condition}
          ></ha-automation-condition-editor>
        </div>
      </ha-card>
    `:a``}},{kind:"method",key:"_handleUiModeNotAvailable",value:function(e){e.stopPropagation(),this._warnings=ue(this.hass,e.detail).warnings,this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"_handleChangeEvent",value:function(e){e.detail.yaml&&(this._warnings=void 0)}},{kind:"method",key:"_handleAction",value:function(e){switch(e.detail.index){case 0:this._switchYamlMode();break;case 1:o(this,"duplicate");break;case 2:this._onDelete()}}},{kind:"method",key:"_onDelete",value:function(){T(this,{text:this.hass.localize("ui.panel.config.automation.editor.conditions.delete_confirm"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),confirm:()=>{o(this,"value-changed",{value:null})}})}},{kind:"method",key:"_switchYamlMode",value:function(){this._warnings=void 0,this._yamlMode=!this._yamlMode}},{kind:"method",key:"_testCondition",value:async function(e){const t=this.condition,i=e.target;if(!i.progress){i.progress=!0;try{const e=await Ae(this.hass,{condition:t});if(this.condition!==t)return;if(!e.condition.valid)return void M(this,{title:this.hass.localize("ui.panel.config.automation.editor.conditions.invalid_condition"),text:e.condition.error});let a;try{a=await me(this.hass,t)}catch(e){if(this.condition!==t)return;return void M(this,{title:this.hass.localize("ui.panel.config.automation.editor.conditions.test_failed"),text:e.message})}if(this.condition!==t)return;a.result?i.actionSuccess():i.actionError()}finally{i.progress=!1}}}},{kind:"get",static:!0,key:"styles",value:function(){return[d,l`
        .card-menu {
          float: right;
          z-index: 3;
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .rtl .card-menu {
          float: left;
        }
        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
      `]}}]}}),t);const qe=(e,t)=>e.callWS({type:"device_automation/action/list",device_id:t}),Te=(e,t)=>e.callWS({type:"device_automation/condition/list",device_id:t}),Me=(e,t)=>e.callWS({type:"device_automation/trigger/list",device_id:t}),Ue=["device_id","domain","entity_id","type","subtype","event","condition","platform"],Ee=(e,t)=>{if(typeof e!=typeof t)return!1;for(const i in e)if(Ue.includes(i)&&!Object.is(e[i],t[i]))return!1;for(const i in t)if(Ue.includes(i)&&!Object.is(e[i],t[i]))return!1;return!0},Le=(e,t)=>{const i=t.entity_id?e.states[t.entity_id]:void 0;return e.localize(`component.${t.domain}.device_automation.action_type.${t.type}`,"entity_name",i?U(i):t.entity_id||"<unknown>","subtype",t.subtype?e.localize(`component.${t.domain}.device_automation.action_subtype.${t.subtype}`)||t.subtype:"")||(t.subtype?`"${t.subtype}" ${t.type}`:t.type)},Ie=(e,t)=>{const i=t.entity_id?e.states[t.entity_id]:void 0;return e.localize(`component.${t.domain}.device_automation.condition_type.${t.type}`,"entity_name",i?U(i):t.entity_id||"<unknown>","subtype",t.subtype?e.localize(`component.${t.domain}.device_automation.condition_subtype.${t.subtype}`)||t.subtype:"")||(t.subtype?`"${t.subtype}" ${t.type}`:t.type)},Be=(e,t)=>{const i=t.entity_id?e.states[t.entity_id]:void 0;return e.localize(`component.${t.domain}.device_automation.trigger_type.${t.type}`,"entity_name",i?U(i):t.entity_id||"<unknown>","subtype",t.subtype?e.localize(`component.${t.domain}.device_automation.trigger_subtype.${t.subtype}`)||t.subtype:"")||(t.subtype?`"${t.subtype}" ${t.type}`:t.type)},Oe="NO_AUTOMATION",je="UNKNOWN_AUTOMATION";let Ne=e(null,(function(e,t){class n extends t{constructor(t,i,a){super(),e(this),this._localizeDeviceAutomation=t,this._fetchDeviceAutomations=i,this._createNoAutomation=a}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"deviceId",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[r()],key:"_automations",value:()=>[]},{kind:"field",decorators:[r()],key:"_renderEmpty",value:()=>!1},{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.no_actions")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.unknown_action")}},{kind:"field",key:"_localizeDeviceAutomation",value:void 0},{kind:"field",key:"_fetchDeviceAutomations",value:void 0},{kind:"field",key:"_createNoAutomation",value:void 0},{kind:"get",key:"_value",value:function(){if(!this.value)return"";if(!this._automations.length)return Oe;const e=this._automations.findIndex((e=>Ee(e,this.value)));return-1===e?je:`${this._automations[e].device_id}_${e}`}},{kind:"method",key:"render",value:function(){if(this._renderEmpty)return a``;const e=this._value;return a`
      <ha-select
        .label=${this.label}
        .value=${e}
        @selected=${this._automationChanged}
        .disabled=${0===this._automations.length}
      >
        ${e===Oe?a`<mwc-list-item .value=${Oe}>
              ${this.NO_AUTOMATION_TEXT}
            </mwc-list-item>`:""}
        ${e===je?a`<mwc-list-item .value=${je}>
              ${this.UNKNOWN_AUTOMATION_TEXT}
            </mwc-list-item>`:""}
        ${this._automations.map(((e,t)=>a`
            <mwc-list-item .value=${`${e.device_id}_${t}`}>
              ${this._localizeDeviceAutomation(this.hass,e)}
            </mwc-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"updated",value:function(e){u(h(n.prototype),"updated",this).call(this,e),e.has("deviceId")&&this._updateDeviceInfo()}},{kind:"method",key:"_updateDeviceInfo",value:async function(){this._automations=this.deviceId?await this._fetchDeviceAutomations(this.hass,this.deviceId):[],this.value&&this.value.device_id===this.deviceId||this._setValue(this._automations.length?this._automations[0]:this._createNoAutomation(this.deviceId)),this._renderEmpty=!0,await this.updateComplete,this._renderEmpty=!1}},{kind:"method",key:"_automationChanged",value:function(e){const t=e.target.value;if(!t||[je,Oe].includes(t))return;const[i,a]=t.split("_"),o=this._automations[a];o.device_id===i&&this._setValue(o)}},{kind:"method",key:"_setValue",value:function(e){this.value&&Ee(e,this.value)||(o(this,"change"),o(this,"value-changed",{value:e}))}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-select {
        width: 100%;
        margin-top: 4px;
      }
    `}}]}}),t);e([n("ha-device-condition-picker")],(function(e,t){return{F:class extends t{constructor(){super(Ie,Te,(e=>({device_id:e||"",condition:"device",domain:"",entity_id:""}))),e(this)}},d:[{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.conditions.no_conditions")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.conditions.unknown_condition")}}]}}),Ne);let Se=e([n("ha-automation-condition-device")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Object})],key:"condition",value:void 0},{kind:"field",decorators:[r()],key:"_deviceId",value:void 0},{kind:"field",decorators:[r()],key:"_capabilities",value:void 0},{kind:"field",key:"_origCondition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{device_id:"",domain:"",entity_id:""}}},{kind:"field",key:"_extraFieldsData",value:()=>v(((e,t)=>{const i={};return t.extra_fields.forEach((t=>{void 0!==e[t.name]&&(i[t.name]=e[t.name])})),i}))},{kind:"method",key:"render",value:function(){var e;const t=this._deviceId||this.condition.device_id;return a`
      <ha-device-picker
        .value=${t}
        @value-changed=${this._devicePicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.device.label")}
      ></ha-device-picker>
      <ha-device-condition-picker
        .value=${this.condition}
        .deviceId=${t}
        @value-changed=${this._deviceConditionPicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.device.condition")}
      ></ha-device-condition-picker>
      ${null!==(e=this._capabilities)&&void 0!==e&&e.extra_fields?a`
            <ha-form
              .hass=${this.hass}
              .data=${this._extraFieldsData(this.condition,this._capabilities)}
              .schema=${this._capabilities.extra_fields}
              .computeLabel=${this._extraFieldsComputeLabelCallback(this.hass.localize)}
              @value-changed=${this._extraFieldsChanged}
            ></ha-form>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._capabilities||this._getCapabilities(),this.condition&&(this._origCondition=this.condition)}},{kind:"method",key:"updated",value:function(e){const t=e.get("condition");t&&!Ee(t,this.condition)&&this._getCapabilities()}},{kind:"method",key:"_getCapabilities",value:async function(){const e=this.condition;this._capabilities=e.domain?await((e,t)=>e.callWS({type:"device_automation/condition/capabilities",condition:t}))(this.hass,e):void 0}},{kind:"method",key:"_devicePicked",value:function(e){e.stopPropagation(),this._deviceId=e.target.value,void 0===this._deviceId&&o(this,"value-changed",{value:{...n.defaultConfig,condition:"device"}})}},{kind:"method",key:"_deviceConditionPicked",value:function(e){e.stopPropagation();let t=e.detail.value;this._origCondition&&Ee(this._origCondition,t)&&(t=this._origCondition),o(this,"value-changed",{value:t})}},{kind:"method",key:"_extraFieldsChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.condition,...e.detail.value}})}},{kind:"method",key:"_extraFieldsComputeLabelCallback",value:function(e){return t=>e(`ui.panel.config.automation.editor.conditions.type.device.extra_fields.${t.name}`)||t.name}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-device-picker {
      display: block;
      margin-bottom: 24px;
    }
  `}]}}),t);e([n("ha-automation-condition")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"conditions",value:void 0},{kind:"method",key:"updated",value:function(e){if(!e.has("conditions"))return;let t;Array.isArray(this.conditions)||(t=[this.conditions]),(t||this.conditions).forEach(((e,i)=>{"string"==typeof e&&(t=t||[...this.conditions],t[i]={condition:"template",value_template:e})})),t&&o(this,"value-changed",{value:t})}},{kind:"method",key:"render",value:function(){return Array.isArray(this.conditions)?a`
      ${this.conditions.map(((e,t)=>a`
          <ha-automation-condition-row
            .index=${t}
            .condition=${e}
            @duplicate=${this._duplicateCondition}
            @value-changed=${this._conditionChanged}
            .hass=${this.hass}
          ></ha-automation-condition-row>
        `))}
      <ha-card>
        <div class="card-actions add-card">
          <mwc-button @click=${this._addCondition}>
            ${this.hass.localize("ui.panel.config.automation.editor.conditions.add")}
          </mwc-button>
        </div>
      </ha-card>
    `:a``}},{kind:"method",key:"_addCondition",value:function(){const e=this.conditions.concat({condition:"device",...Se.defaultConfig});o(this,"value-changed",{value:e})}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation();const t=[...this.conditions],i=e.detail.value,a=e.target.index;null===i?t.splice(a,1):t[a]=i,o(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateCondition",value:function(e){e.stopPropagation();const t=e.target.index;o(this,"value-changed",{value:this.conditions.concat(this.conditions[t])})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-automation-condition-row,
      ha-card {
        display: block;
        margin-top: 16px;
      }
      .add-card mwc-button {
        display: block;
        text-align: center;
      }
    `}}]}}),t);const Ve=e=>{if(void 0===e)return;if("object"!=typeof e){if("string"==typeof e||isNaN(e)){const t=(null==e?void 0:e.toString().split(":"))||[];return{hours:Number(t[0])||0,minutes:Number(t[1])||0,seconds:Number(t[2])||0,milliseconds:Number(t[3])||0}}return{seconds:e}}if(!("days"in e))return e;const{days:t,minutes:i,seconds:a,milliseconds:o}=e;let n=e.hours||0;return n=(n||0)+24*(t||0),{hours:n,minutes:i,seconds:a,milliseconds:o}},We=S({platform:V(),id:W(V())}),Re=S({days:W(R()),hours:W(R()),minutes:W(R()),seconds:W(R())}),Ke=S({condition:K("state"),entity_id:W(V()),attribute:W(V()),state:W(V()),for:W(Y([V(),Re]))});let Ye=e([n("ha-automation-condition-state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:"",state:""}}},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"entity_id",required:!0,selector:{entity:{}}},{name:"attribute",selector:{attribute:{entity_id:e}}},{name:"state",selector:{text:{}}},{name:"for",selector:{duration:{}}}]))},{kind:"method",key:"shouldUpdate",value:function(e){if(e.has("condition"))try{X(this.condition,Ke)}catch(e){return o(this,"ui-mode-not-available",e),!1}return!0}},{kind:"method",key:"render",value:function(){const e=Ve(this.condition.for),t={...this.condition,for:e},i=this._schema(this.condition.entity_id);return a`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${i}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"entity_id":return this.hass.localize("ui.components.entity.entity-picker.entity");case"attribute":return this.hass.localize("ui.components.entity.entity-attribute-picker.attribute");case"for":return this.hass.localize("ui.panel.config.automation.editor.triggers.type.state.for");default:return this.hass.localize(`ui.panel.config.automation.editor.conditions.type.state.${e.name}`)}}}}]}}),t),Xe=e([n("ha-automation-condition-logical")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{conditions:[{condition:"state",...Ye.defaultConfig}]}}},{kind:"method",key:"render",value:function(){return a`
      <ha-automation-condition
        .conditions=${this.condition.conditions||[]}
        @value-changed=${this._valueChanged}
        .hass=${this.hass}
      ></ha-automation-condition>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.condition,conditions:e.detail.value}})}}]}}),t);e([n("ha-automation-condition-and")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[]}}),Xe),e([n("ha-automation-condition-not")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[]}}),Xe),e([n("ha-automation-condition-numeric_state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:""}}},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"entity_id",required:!0,selector:{entity:{}}},{name:"attribute",selector:{attribute:{entity_id:e}}},{name:"above",selector:{text:{}}},{name:"below",selector:{text:{}}},{name:"value_template",selector:{text:{multiline:!0}}}]))},{kind:"method",key:"render",value:function(){const e=this._schema(this.condition.entity_id);return a`
      <ha-form
        .hass=${this.hass}
        .data=${this.condition}
        .schema=${e}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"entity_id":return this.hass.localize("ui.components.entity.entity-picker.entity");case"attribute":return this.hass.localize("ui.components.entity.entity-attribute-picker.attribute");default:return this.hass.localize(`ui.panel.config.automation.editor.triggers.type.numeric_state.${e.name}`)}}}}]}}),t),e([n("ha-automation-condition-or")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[]}}),Xe),e([n("ha-automation-condition-sun")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{}}},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"before",type:"select",required:!0,options:[["sunrise",e("ui.panel.config.automation.editor.conditions.type.sun.sunrise")],["sunset",e("ui.panel.config.automation.editor.conditions.type.sun.sunset")]]},{name:"before_offset",selector:{text:{}}},{name:"after",type:"select",required:!0,options:[["sunrise",e("ui.panel.config.automation.editor.conditions.type.sun.sunrise")],["sunset",e("ui.panel.config.automation.editor.conditions.type.sun.sunset")]]},{name:"after_offset",selector:{text:{}}}]))},{kind:"method",key:"render",value:function(){const e=this._schema(this.hass.localize);return a`
      <ha-form
        .schema=${e}
        .data=${this.condition}
        .hass=${this.hass}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.conditions.type.sun.${e.name}`)}}]}}),t),e([n("ha-automation-condition-template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{value_template:""}}},{kind:"method",key:"render",value:function(){const{value_template:e}=this.condition;return a`
      <ha-textarea
        name="value_template"
        .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.template.value_template")}
        .value=${e}
        @input=${this._valueChanged}
        dir="ltr"
        autogrow
      ></ha-textarea>
    `}},{kind:"method",key:"_valueChanged",value:function(e){((e,t)=>{var i,a,n;t.stopPropagation();const s=null===(i=t.currentTarget)||void 0===i?void 0:i.name;if(!s)return;const d=(null===(a=t.detail)||void 0===a?void 0:a.value)||(null===(n=t.currentTarget)||void 0===n?void 0:n.value);if((e.condition[s]||"")===d)return;let l;d?l={...e.condition,[s]:d}:(l={...e.condition},delete l[s]),o(e,"value-changed",{value:l})})(this,e)}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-textarea {
      display: block;
    }
  `}]}}),t);const Ge={mon:1,tue:2,wed:3,thu:4,fri:5,sat:6,sun:7};e([n("ha-automation-condition-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"field",decorators:[r()],key:"_inputModeBefore",value:void 0},{kind:"field",decorators:[r()],key:"_inputModeAfter",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{}}},{kind:"field",key:"_schema",value:()=>v(((e,t,i)=>{const a=t?{name:"after",selector:{entity:{domain:"input_datetime"}}}:{name:"after",selector:{time:{}}},o=i?{name:"before",selector:{entity:{domain:"input_datetime"}}}:{name:"before",selector:{time:{}}};return[{name:"mode_after",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.conditions.type.time.type_value")],["input",e("ui.panel.config.automation.editor.conditions.type.time.type_input")]]},a,{name:"mode_before",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.conditions.type.time.type_value")],["input",e("ui.panel.config.automation.editor.conditions.type.time.type_input")]]},o,{type:"multi_select",name:"weekday",options:Object.keys(Ge).map((t=>[t,e(`ui.panel.config.automation.editor.conditions.type.time.weekdays.${t}`)]))}]}))},{kind:"method",key:"render",value:function(){var e,t,i,o;const n=null!==(e=this._inputModeBefore)&&void 0!==e?e:null===(t=this.condition.before)||void 0===t?void 0:t.startsWith("input_datetime."),s=null!==(i=this._inputModeAfter)&&void 0!==i?i:null===(o=this.condition.after)||void 0===o?void 0:o.startsWith("input_datetime."),d=this._schema(this.hass.localize,s,n),l={mode_before:n?"input":"value",mode_after:s?"input":"value",...this.condition};return a`
      <ha-form
        .hass=${this.hass}
        .data=${l}
        .schema=${d}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;this._inputModeAfter="input"===t.mode_after,this._inputModeBefore="input"===t.mode_before,delete t.mode_after,delete t.mode_before,Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.conditions.type.time.${e.name}`)}}]}}),t),e([n("ha-automation-condition-trigger")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"condition",value:void 0},{kind:"field",decorators:[r()],key:"_triggers",value:()=>[]},{kind:"field",key:"_unsub",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{id:""}}},{kind:"method",key:"connectedCallback",value:function(){u(h(n.prototype),"connectedCallback",this).call(this);const e={callback:e=>this._automationUpdated(e)};o(this,"subscribe-automation-config",e),this._unsub=e.unsub}},{kind:"method",key:"disconnectedCallback",value:function(){u(h(n.prototype),"disconnectedCallback",this).call(this),this._unsub&&this._unsub()}},{kind:"method",key:"render",value:function(){const{id:e}=this.condition;return this._triggers.length?a`<ha-select
      .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.trigger.id")}
      .value=${e}
      @selected=${this._triggerPicked}
    >
      ${this._triggers.map((e=>a`
            <mwc-list-item .value=${e.id}> ${e.id} </mwc-list-item>
          `))}
    </ha-select>`:this.hass.localize("ui.panel.config.automation.editor.conditions.type.trigger.no_triggers")}},{kind:"method",key:"_automationUpdated",value:function(e){this._triggers=null!=e&&e.trigger?he(e.trigger).filter((e=>e.id)):[]}},{kind:"method",key:"_triggerPicked",value:function(e){if(e.stopPropagation(),!e.target.value)return;const t=e.target.value;this.condition.id!==t&&o(this,"value-changed",{value:{...this.condition,id:t}})}}]}}),t);const He=e=>"latitude"in e.attributes&&"longitude"in e.attributes;function Je(e){return He(e)&&"zone"!==E(e)}const Ze=["zone"];e([n("ha-automation-condition-zone")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"condition",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:"",zone:""}}},{kind:"method",key:"render",value:function(){const{entity_id:e,zone:t}=this.condition;return a`
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.zone.entity")}
        .value=${e}
        @value-changed=${this._entityPicked}
        .hass=${this.hass}
        allow-custom-entity
        .entityFilter=${Je}
      ></ha-entity-picker>
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type.zone.zone")}
        .value=${t}
        @value-changed=${this._zonePicked}
        .hass=${this.hass}
        allow-custom-entity
        .includeDomains=${Ze}
      ></ha-entity-picker>
      <label id="eventlabel">
        ${this.hass.localize("ui.panel.config.automation.editor.conditions.type.zone.event")}
      </label>
    `}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.condition,entity_id:e.detail.value}})}},{kind:"method",key:"_zonePicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.condition,zone:e.detail.value}})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-entity-picker {
      display: block;
      margin-bottom: 24px;
    }
  `}]}}),t);const Qe=["device","and","or","not","state","numeric_state","sun","template","time","trigger","zone"];e([n("ha-automation-condition-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"condition",value:void 0},{kind:"field",decorators:[i()],key:"yamlMode",value:()=>!1},{kind:"field",key:"_processedTypes",value:()=>v((e=>Qe.map((t=>[t,e(`ui.panel.config.automation.editor.conditions.type.${t}.label`)])).sort(((e,t)=>re(e[1],t[1])))))},{kind:"method",key:"render",value:function(){const e=Qe.indexOf(this.condition.condition),t=this.yamlMode||-1===e;return a`
      ${t?a`
            ${-1===e?a`
                  ${this.hass.localize("ui.panel.config.automation.editor.conditions.unsupported_condition","condition",this.condition.condition)}
                `:""}
            <h2>
              ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
            </h2>
            <ha-yaml-editor
              .hass=${this.hass}
              .defaultValue=${this.condition}
              @value-changed=${this._onYamlChange}
            ></ha-yaml-editor>
          `:a`
            <ha-select
              .label=${this.hass.localize("ui.panel.config.automation.editor.conditions.type_select")}
              .value=${this.condition.condition}
              naturalMenuWidth
              @selected=${this._typeChanged}
            >
              ${this._processedTypes(this.hass.localize).map((([e,t])=>a`
                  <mwc-list-item .value=${e}>${t}</mwc-list-item>
                `))}
            </ha-select>

            <div>
              ${le(`ha-automation-condition-${this.condition.condition}`,{hass:this.hass,condition:this.condition})}
            </div>
          `}
    `}},{kind:"method",key:"_typeChanged",value:function(e){const t=e.target.value;if(!t)return;const i=customElements.get(`ha-automation-condition-${t}`);t!==this.condition.condition&&o(this,"value-changed",{value:{condition:t,...i.defaultConfig}})}},{kind:"method",key:"_onYamlChange",value:function(e){e.stopPropagation(),e.detail.isValid&&o(this,"value-changed",{value:e.detail.value,yaml:!0})}},{kind:"field",static:!0,key:"styles",value:()=>[d,l`
      ha-select {
        margin-bottom: 24px;
      }
    `]}]}}),t),e([n("ha-automation-action-condition")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{condition:"state"}}},{kind:"method",key:"render",value:function(){return a`
      <ha-automation-condition-editor
        .condition=${this.action}
        .hass=${this.hass}
        @value-changed=${this._conditionChanged}
      ></ha-automation-condition-editor>
    `}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:e.detail.value})}}]}}),t);const et=new RegExp("{%|{{"),tt=e=>{if(!e)return!1;if("string"==typeof e)return(e=>et.test(e))(e);if("object"==typeof e){return(Array.isArray(e)?e:Object.values(e)).some((e=>e&&tt(e)))}return!1};e([n("ha-automation-action-delay")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"field",decorators:[i()],key:"_timeData",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{delay:""}}},{kind:"method",key:"willUpdate",value:function(e){e.has("action")&&(this.action&&tt(this.action)?o(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))):this._timeData=Ve(this.action.delay))}},{kind:"method",key:"render",value:function(){return a`<ha-duration-input
      .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.delay.delay")}
      .data=${this._timeData}
      enableMillisecond
      @value-changed=${this._valueChanged}
    ></ha-duration-input>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;t&&o(this,"value-changed",{value:{...this.action,delay:t}})}}]}}),t),e([n("ha-device-action-picker")],(function(e,t){return{F:class extends t{constructor(){super(Le,qe,(e=>({device_id:e||"",domain:"",entity_id:""}))),e(this)}},d:[{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.no_actions")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.actions.unknown_action")}}]}}),Ne);let it=e([n("ha-automation-action-device_id")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Object})],key:"action",value:void 0},{kind:"field",decorators:[r()],key:"_deviceId",value:void 0},{kind:"field",decorators:[r()],key:"_capabilities",value:void 0},{kind:"field",key:"_origAction",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{device_id:"",domain:"",entity_id:""}}},{kind:"field",key:"_extraFieldsData",value:()=>v(((e,t)=>{const i={};return t.extra_fields.forEach((t=>{void 0!==e[t.name]&&(i[t.name]=e[t.name])})),i}))},{kind:"method",key:"render",value:function(){var e;const t=this._deviceId||this.action.device_id;return a`
      <ha-device-picker
        .value=${t}
        @value-changed=${this._devicePicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.device_id.label")}
      ></ha-device-picker>
      <ha-device-action-picker
        .value=${this.action}
        .deviceId=${t}
        @value-changed=${this._deviceActionPicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.device_id.action")}
      ></ha-device-action-picker>
      ${null!==(e=this._capabilities)&&void 0!==e&&e.extra_fields?a`
            <ha-form
              .hass=${this.hass}
              .data=${this._extraFieldsData(this.action,this._capabilities)}
              .schema=${this._capabilities.extra_fields}
              .computeLabel=${this._extraFieldsComputeLabelCallback(this.hass.localize)}
              @value-changed=${this._extraFieldsChanged}
            ></ha-form>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._capabilities||this._getCapabilities(),this.action&&(this._origAction=this.action)}},{kind:"method",key:"updated",value:function(e){const t=e.get("action");t&&!Ee(t,this.action)&&(this._deviceId=void 0,this._getCapabilities())}},{kind:"method",key:"_getCapabilities",value:async function(){var e,t;this._capabilities=this.action.domain?await(e=this.hass,t=this.action,e.callWS({type:"device_automation/action/capabilities",action:t})):void 0}},{kind:"method",key:"_devicePicked",value:function(e){e.stopPropagation(),this._deviceId=e.target.value,void 0===this._deviceId&&o(this,"value-changed",{value:n.defaultConfig})}},{kind:"method",key:"_deviceActionPicked",value:function(e){e.stopPropagation();let t=e.detail.value;this._origAction&&Ee(this._origAction,t)&&(t=this._origAction),o(this,"value-changed",{value:t})}},{kind:"method",key:"_extraFieldsChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.action,...e.detail.value}})}},{kind:"method",key:"_extraFieldsComputeLabelCallback",value:function(e){return t=>e(`ui.panel.config.automation.editor.actions.type.device_id.extra_fields.${t.name}`)||t.name}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-device-picker {
      display: block;
      margin-bottom: 16px;
    }
    ha-device-action-picker {
      display: block;
    }
  `}]}}),t);const at=e=>a`<mwc-list-item twoline>
  <span>${e.name}</span>
  <span slot="secondary"
    >${e.name===e.service?"":e.service}</span
  >
</mwc-list-item>`;let ot=e(null,(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[r()],key:"_filter",value:void 0},{kind:"method",key:"render",value:function(){return a`
      <ha-combo-box
        .hass=${this.hass}
        .label=${this.hass.localize("ui.components.service-picker.service")}
        .filteredItems=${this._filteredServices(this.hass.localize,this.hass.services,this._filter)}
        .value=${this.value}
        .renderer=${at}
        item-value-path="service"
        item-label-path="name"
        allow-custom-value
        @filter-changed=${this._filterChanged}
        @value-changed=${this._valueChanged}
      ></ha-combo-box>
    `}},{kind:"field",key:"_services",value:()=>v(((e,t)=>{if(!t)return[];const i=[];return Object.keys(t).sort().forEach((a=>{const o=Object.keys(t[a]).sort();for(const n of o)i.push({service:`${a}.${n}`,name:`${G(e,a)}: ${t[a][n].name||n}`})})),i}))},{kind:"field",key:"_filteredServices",value(){return v(((e,t,i)=>{if(!t)return[];const a=this._services(e,t);return i?a.filter((e=>{var t;return e.service.toLowerCase().includes(i)||(null===(t=e.name)||void 0===t?void 0:t.toLowerCase().includes(i))})):a}))}},{kind:"method",key:"_filterChanged",value:function(e){this._filter=e.detail.value.toLowerCase()}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value,o(this,"change"),o(this,"value-changed",{value:this.value})}}]}}),t);customElements.define("ha-service-picker",ot),e([n("ha-automation-action-event")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"field",decorators:[k("ha-yaml-editor",!0)],key:"_yamlEditor",value:void 0},{kind:"field",key:"_actionData",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{event:"",event_data:{}}}},{kind:"method",key:"updated",value:function(e){e.has("action")&&(this._actionData&&this._actionData!==this.action.event_data&&this._yamlEditor&&this._yamlEditor.setValue(this.action.event_data),this._actionData=this.action.event_data)}},{kind:"method",key:"render",value:function(){const{event:e,event_data:t}=this.action;return a`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.event.event")}
        .value=${e}
        @change=${this._eventChanged}
      ></ha-textfield>
      <ha-yaml-editor
        .hass=${this.hass}
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.event.event_data")}
        .name=${"event_data"}
        .defaultValue=${t}
        @value-changed=${this._dataChanged}
      ></ha-yaml-editor>
    `}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&(this._actionData=e.detail.value,bt(this,e))}},{kind:"method",key:"_eventChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.action,event:e.target.value}})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-textfield {
        display: block;
      }
    `}}]}}),t);const nt=[{name:"media_content_id",required:!1,selector:{text:{}}},{name:"media_content_type",required:!1,selector:{text:{}}}];e([n("ha-selector-media")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"required",value:()=>!0},{kind:"field",decorators:[r()],key:"_thumbnailUrl",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(e.has("value")){var t,i,a,o;const s=null===(t=this.value)||void 0===t||null===(i=t.metadata)||void 0===i?void 0:i.thumbnail;if(s===(null===(a=e.get("value"))||void 0===a||null===(o=a.metadata)||void 0===o?void 0:o.thumbnail))return;if(s&&s.startsWith("/"))this._thumbnailUrl=void 0,H(this.hass,s).then((e=>{this._thumbnailUrl=e.path}));else if(s&&s.startsWith("https://brands.home-assistant.io")){var n;this._thumbnailUrl=ye({domain:fe(s),type:"icon",useFallback:!0,darkOptimized:null===(n=this.hass.themes)||void 0===n?void 0:n.darkMode})}else this._thumbnailUrl=s}}},{kind:"method",key:"render",value:function(){var e,t,i,o,n,s,d,l,r,c,u,h,v;const k=null!==(e=this.value)&&void 0!==e&&e.entity_id?this.hass.states[this.value.entity_id]:void 0,y=!(null!==(t=this.value)&&void 0!==t&&t.entity_id)||k&&L(k,J);return a`<ha-entity-picker
        .hass=${this.hass}
        .value=${null===(i=this.value)||void 0===i?void 0:i.entity_id}
        .label=${this.label||this.hass.localize("ui.components.selectors.media.pick_media_player")}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .required=${this.required}
        include-domains='["media_player"]'
        allow-custom-entity
        @value-changed=${this._entityChanged}
      ></ha-entity-picker>
      ${y?a`<ha-card
            outlined
            @click=${this._pickMedia}
            class=${this.disabled||null===(o=this.value)||void 0===o||!o.entity_id?"disabled":""}
          >
            <div
              class="thumbnail ${p({portrait:!(null===(n=this.value)||void 0===n||null===(s=n.metadata)||void 0===s||!s.media_class)&&"portrait"===Z[this.value.metadata.children_media_class||this.value.metadata.media_class].thumbnail_ratio})}"
            >
              ${null!==(d=this.value)&&void 0!==d&&null!==(l=d.metadata)&&void 0!==l&&l.thumbnail?a`
                    <div
                      class="${p({"centered-image":!!this.value.metadata.media_class&&["app","directory"].includes(this.value.metadata.media_class)})}
                        image"
                      style=${this._thumbnailUrl?`background-image: url(${this._thumbnailUrl});`:""}
                    ></div>
                  `:a`
                    <div class="icon-holder image">
                      <ha-svg-icon
                        class="folder"
                        .path=${null!==(r=this.value)&&void 0!==r&&r.media_content_id?null!==(c=this.value)&&void 0!==c&&null!==(u=c.metadata)&&void 0!==u&&u.media_class?Z["directory"===this.value.metadata.media_class&&this.value.metadata.children_media_class||this.value.metadata.media_class].icon:g:m}
                      ></ha-svg-icon>
                    </div>
                  `}
            </div>
            <div class="title">
              ${null!==(h=this.value)&&void 0!==h&&h.media_content_id?(null===(v=this.value.metadata)||void 0===v?void 0:v.title)||this.value.media_content_id:this.hass.localize("ui.components.selectors.media.pick_media")}
            </div>
          </ha-card>`:a`<ha-alert>
              ${this.hass.localize("ui.components.selectors.media.browse_not_supported")}
            </ha-alert>
            <ha-form
              .hass=${this.hass}
              .data=${this.value}
              .schema=${nt}
              .computeLabel=${this._computeLabelCallback}
            ></ha-form>`}`}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.components.selectors.media.${e.name}`)}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{entity_id:e.detail.value,media_content_id:"",media_content_type:""}})}},{kind:"method",key:"_pickMedia",value:function(){var e;_e(this,{action:"pick",entityId:this.value.entity_id,navigateIds:null===(e=this.value.metadata)||void 0===e?void 0:e.navigateIds,mediaPickedCallback:e=>{var t;o(this,"value-changed",{value:{...this.value,media_content_id:e.item.media_content_id,media_content_type:e.item.media_content_type,metadata:{title:e.item.title,thumbnail:e.item.thumbnail,media_class:e.item.media_class,children_media_class:e.item.children_media_class,navigateIds:null===(t=e.navigateIds)||void 0===t?void 0:t.map((e=>({media_content_type:e.media_content_type,media_content_id:e.media_content_id})))}}})}})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-entity-picker {
        display: block;
        margin-bottom: 16px;
      }
      mwc-button {
        margin-top: 8px;
      }
      ha-alert {
        display: block;
        margin-bottom: 16px;
      }
      ha-card {
        position: relative;
        width: 200px;
        box-sizing: border-box;
        cursor: pointer;
      }
      ha-card.disabled {
        pointer-events: none;
        color: var(--disabled-text-color);
      }
      ha-card .thumbnail {
        width: 100%;
        position: relative;
        box-sizing: border-box;
        transition: padding-bottom 0.1s ease-out;
        padding-bottom: 100%;
      }
      ha-card .thumbnail.portrait {
        padding-bottom: 150%;
      }
      ha-card .image {
        border-radius: 3px 3px 0 0;
      }
      .folder {
        --mdc-icon-size: calc(var(--media-browse-item-size, 175px) * 0.4);
      }
      .title {
        font-size: 16px;
        padding-top: 16px;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 16px;
        padding-left: 16px;
        padding-right: 4px;
        white-space: nowrap;
      }
      .image {
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
      }
      .centered-image {
        margin: 0 8px;
        background-size: contain;
      }
      .icon-holder {
        display: flex;
        justify-content: center;
        align-items: center;
      }
    `}}]}}),t),e([n("ha-automation-action-play_media")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:()=>!1},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{service:"media_player.play_media",target:{entity_id:""},data:{media_content_id:"",media_content_type:""},metadata:{}}}},{kind:"field",key:"_getSelectorValue",value:()=>v((e=>{var t,i,a;return{entity_id:(null===(t=e.target)||void 0===t?void 0:t.entity_id)||e.entity_id,media_content_id:null===(i=e.data)||void 0===i?void 0:i.media_content_id,media_content_type:null===(a=e.data)||void 0===a?void 0:a.media_content_type,metadata:e.metadata}}))},{kind:"method",key:"render",value:function(){return a`
      <ha-selector-media
        .hass=${this.hass}
        .value=${this._getSelectorValue(this.action)}
        @value-changed=${this._valueChanged}
      ></ha-selector-media>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{service:"media_player.play_media",target:{entity_id:e.detail.value.entity_id},data:{media_content_id:e.detail.value.media_content_id,media_content_type:e.detail.value.media_content_type},metadata:e.detail.value.metadata||{}}})}}]}}),t);const st=["count","while","until"],dt=e=>st.find((t=>t in e));e([n("ha-automation-action-repeat")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{repeat:{count:2,sequence:[]}}}},{kind:"method",key:"render",value:function(){const e=this.action.repeat,t=dt(e);return a`
      <ha-select
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type_select")}
        .value=${t}
        @selected=${this._typeChanged}
      >
        ${st.map((e=>a`
            <mwc-list-item .value=${e}>
              ${this.hass.localize(`ui.panel.config.automation.editor.actions.type.repeat.type.${e}.label`)}
            </mwc-list-item>
          `))}
      </ha-select>
      ${"count"===t?a`
            <ha-textfield
              .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.count.label")}
              name="count"
              .value=${e.count||"0"}
              @change=${this._countChanged}
            ></ha-textfield>
          `:""}
      ${"while"===t?a` <h3>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.while.conditions")}:
            </h3>
            <ha-automation-condition
              .conditions=${e.while||[]}
              .hass=${this.hass}
              @value-changed=${this._conditionChanged}
            ></ha-automation-condition>`:""}
      ${"until"===t?a` <h3>
              ${this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.type.until.conditions")}:
            </h3>
            <ha-automation-condition
              .conditions=${e.until||[]}
              .hass=${this.hass}
              @value-changed=${this._conditionChanged}
            ></ha-automation-condition>`:""}
      <h3>
        ${this.hass.localize("ui.panel.config.automation.editor.actions.type.repeat.sequence")}:
      </h3>
      <ha-automation-action
        .actions=${e.sequence}
        @value-changed=${this._actionChanged}
        .hass=${this.hass}
      ></ha-automation-action>
    `}},{kind:"method",key:"_typeChanged",value:function(e){const t=e.target.value;if(!t||t===dt(this.action.repeat))return;o(this,"value-changed",{value:{repeat:{[t]:"count"===t?2:[],sequence:this.action.repeat.sequence}}})}},{kind:"method",key:"_conditionChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:{repeat:{...this.action.repeat,[dt(this.action.repeat)]:t}}})}},{kind:"method",key:"_actionChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:{repeat:{...this.action.repeat,sequence:t}}})}},{kind:"method",key:"_countChanged",value:function(e){const t=e.target.value;this.action.repeat.count!==t&&o(this,"value-changed",{value:{repeat:{...this.action.repeat,count:t}}})}},{kind:"get",static:!0,key:"styles",value:function(){return[d,l`
        ha-textfield {
          margin-top: 16px;
        }
      `]}}]}}),t);const lt=S({service:W(V()),entity_id:W(be()),target:W(Q()),data:W(Q())});e([n("ha-automation-action-service")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"action",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[r()],key:"_action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{service:"",data:{}}}},{kind:"method",key:"willUpdate",value:function(e){if(e.has("action")){try{X(this.action,lt)}catch(e){return void o(this,"ui-mode-not-available",e)}this.action&&tt(this.action)?o(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))):this.action.entity_id?(this._action={...this.action,data:{...this.action.data,entity_id:this.action.entity_id}},delete this._action.entity_id):this._action=this.action}}},{kind:"method",key:"render",value:function(){var e;return a`
      <ha-service-control
        .narrow=${this.narrow}
        .hass=${this.hass}
        .value=${this._action}
        .showAdvanced=${null===(e=this.hass.userData)||void 0===e?void 0:e.showAdvanced}
        @value-changed=${this._actionChanged}
      ></ha-service-control>
    `}},{kind:"method",key:"_actionChanged",value:function(e){e.detail.value===this._action&&e.stopPropagation()}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-service-control {
        display: block;
        margin: 0 -16px;
      }
    `}}]}}),t),e([n("ha-device-trigger-picker")],(function(e,t){return{F:class extends t{constructor(){super(Be,Me,(e=>({device_id:e||"",platform:"device",domain:"",entity_id:""}))),e(this)}},d:[{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.triggers.no_triggers")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.triggers.unknown_trigger")}}]}}),Ne);let rt=e([n("ha-automation-trigger-device")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Object})],key:"trigger",value:void 0},{kind:"field",decorators:[r()],key:"_deviceId",value:void 0},{kind:"field",decorators:[r()],key:"_capabilities",value:void 0},{kind:"field",key:"_origTrigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{device_id:"",domain:"",entity_id:""}}},{kind:"field",key:"_extraFieldsData",value:()=>v(((e,t)=>{const i={};return t.extra_fields.forEach((t=>{void 0!==e[t.name]&&(i[t.name]=e[t.name])})),i}))},{kind:"method",key:"render",value:function(){var e;const t=this._deviceId||this.trigger.device_id;return a`
      <ha-device-picker
        .value=${t}
        @value-changed=${this._devicePicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.device.label")}
      ></ha-device-picker>
      <ha-device-trigger-picker
        .value=${this.trigger}
        .deviceId=${t}
        @value-changed=${this._deviceTriggerPicked}
        .hass=${this.hass}
        label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.device.trigger")}
      ></ha-device-trigger-picker>
      ${null!==(e=this._capabilities)&&void 0!==e&&e.extra_fields?a`
            <ha-form
              .hass=${this.hass}
              .data=${this._extraFieldsData(this.trigger,this._capabilities)}
              .schema=${this._capabilities.extra_fields}
              .computeLabel=${this._extraFieldsComputeLabelCallback(this.hass.localize)}
              @value-changed=${this._extraFieldsChanged}
            ></ha-form>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._capabilities||this._getCapabilities(),this.trigger&&(this._origTrigger=this.trigger)}},{kind:"method",key:"updated",value:function(e){if(!e.has("trigger"))return;const t=e.get("trigger");t&&!Ee(t,this.trigger)&&this._getCapabilities()}},{kind:"method",key:"_getCapabilities",value:async function(){const e=this.trigger;this._capabilities=e.domain?await((e,t)=>e.callWS({type:"device_automation/trigger/capabilities",trigger:t}))(this.hass,e):void 0}},{kind:"method",key:"_devicePicked",value:function(e){e.stopPropagation(),this._deviceId=e.target.value,void 0===this._deviceId&&o(this,"value-changed",{value:{...n.defaultConfig,platform:"device"}})}},{kind:"method",key:"_deviceTriggerPicked",value:function(e){e.stopPropagation();let t=e.detail.value;this._origTrigger&&Ee(this._origTrigger,t)&&(t=this._origTrigger),this.trigger.id&&(t.id=this.trigger.id),o(this,"value-changed",{value:t})}},{kind:"method",key:"_extraFieldsChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.trigger,...e.detail.value}})}},{kind:"method",key:"_extraFieldsComputeLabelCallback",value:function(e){return t=>e(`ui.panel.config.automation.editor.triggers.type.device.extra_fields.${t.name}`)||t.name}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-device-picker {
      display: block;
      margin-bottom: 24px;
    }
  `}]}}),t);e([n("ha-user-badge")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"user",value:void 0},{kind:"field",decorators:[r()],key:"_personPicture",value:void 0},{kind:"field",key:"_personEntityId",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if(u(h(o.prototype),"willUpdate",this).call(this,e),e.has("user"))return void this._getPersonPicture();const t=e.get("hass");if(this._personEntityId&&t&&this.hass.states[this._personEntityId]!==t.states[this._personEntityId]){const e=this.hass.states[this._personEntityId];e?this._personPicture=e.attributes.entity_picture:this._getPersonPicture()}else!this._personEntityId&&t&&this._getPersonPicture()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.user)return a``;const e=this._personPicture;if(e)return a`<div
        style=${y({backgroundImage:`url(${e})`})}
        class="picture"
      ></div>`;const t=ee(this.user.name);return a`<div
      class="initials ${p({long:t.length>2})}"
    >
      ${t}
    </div>`}},{kind:"method",key:"_getPersonPicture",value:function(){if(this._personEntityId=void 0,this._personPicture=void 0,this.hass&&this.user)for(const e of Object.values(this.hass.states))if(e.attributes.user_id===this.user.id&&"person"===E(e)){this._personEntityId=e.entity_id,this._personPicture=e.attributes.entity_picture;break}}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: contents;
      }
      .picture {
        width: 40px;
        height: 40px;
        background-size: cover;
        border-radius: 50%;
      }
      .initials {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }
      .initials.long {
        font-size: 80%;
      }
    `}}]}}),t);let ct=e(null,(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"noUserLabel",value:void 0},{kind:"field",decorators:[i()],key:"value",value:()=>""},{kind:"field",decorators:[i()],key:"users",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",key:"_sortedUsers",value:()=>v((e=>e?e.filter((e=>!e.system_generated)).sort(((e,t)=>re(e.name,t.name))):[]))},{kind:"method",key:"render",value:function(){var e,t;return a`
      <ha-select
        .label=${this.label}
        .disabled=${this.disabled}
        .value=${this.value}
        @selected=${this._userChanged}
      >
        ${0===(null===(e=this.users)||void 0===e?void 0:e.length)?a`<mwc-list-item value="">
              ${this.noUserLabel||(null===(t=this.hass)||void 0===t?void 0:t.localize("ui.components.user-picker.no_user"))}
            </mwc-list-item>`:""}
        ${this._sortedUsers(this.users).map((e=>a`
            <mwc-list-item graphic="avatar" .value=${e.id}>
              <ha-user-badge
                .hass=${this.hass}
                .user=${e}
                slot="graphic"
              ></ha-user-badge>
              ${e.name}
            </mwc-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){u(h(n.prototype),"firstUpdated",this).call(this,e),void 0===this.users&&te(this.hass).then((e=>{this.users=e}))}},{kind:"method",key:"_userChanged",value:function(e){const t=e.target.value;t!==this.value&&(this.value=t,setTimeout((()=>{o(this,"value-changed",{value:t}),o(this,"change")}),0))}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: inline-block;
      }
      mwc-list {
        display: block;
      }
    `}}]}}),t);customElements.define("ha-user-picker",ct),e([n("ha-users-picker")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i({attribute:"picked-user-label"})],key:"pickedUserLabel",value:void 0},{kind:"field",decorators:[i({attribute:"pick-user-label"})],key:"pickUserLabel",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"users",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){u(h(n.prototype),"firstUpdated",this).call(this,e),void 0===this.users&&te(this.hass).then((e=>{this.users=e}))}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.users)return a``;const e=this._notSelectedUsers(this.users,this.value);return a`
      ${$e([e],(()=>{var t;return null===(t=this.value)||void 0===t?void 0:t.map(((t,i)=>a`
            <div>
              <ha-user-picker
                .label=${this.pickedUserLabel}
                .noUserLabel=${this.hass.localize("ui.components.user-picker.remove_user")}
                .index=${i}
                .hass=${this.hass}
                .value=${t}
                .users=${this._notSelectedUsersAndSelected(t,this.users,e)}
                @value-changed=${this._userChanged}
              ></ha-user-picker>
              <ha-icon-button
                .userId=${t}
                .label=${this.hass.localize("ui.components.user-picker.remove_user")}
                .path=${f}
                @click=${this._removeUser}
              >
                ></ha-icon-button
              >
            </div>
          `))}))}
      <ha-user-picker
        .label=${this.pickUserLabel||this.hass.localize("ui.components.user-picker.add_user")}
        .hass=${this.hass}
        .users=${e}
        .disabled=${!(null!=e&&e.length)}
        @value-changed=${this._addUser}
      ></ha-user-picker>
    `}},{kind:"field",key:"_notSelectedUsers",value:()=>v(((e,t)=>t?null==e?void 0:e.filter((e=>!e.system_generated&&!t.includes(e.id))):null==e?void 0:e.filter((e=>!e.system_generated))))},{kind:"field",key:"_notSelectedUsersAndSelected",value:()=>(e,t,i)=>{const a=null==t?void 0:t.find((t=>t.id===e));return a?i?[...i,a]:[a]:i}},{kind:"get",key:"_currentUsers",value:function(){return this.value||[]}},{kind:"method",key:"_updateUsers",value:async function(e){this.value=e,o(this,"value-changed",{value:e})}},{kind:"method",key:"_userChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.index,i=e.detail.value,a=[...this._currentUsers];""===i?a.splice(t,1):a.splice(t,1,i),this._updateUsers(a)}},{kind:"method",key:"_addUser",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentUsers;i.includes(t)||this._updateUsers([...i,t])}},{kind:"method",key:"_removeUser",value:function(e){const t=e.currentTarget.userId;this._updateUsers(this._currentUsers.filter((e=>e!==t)))}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
      }
      div {
        display: flex;
        align-items: center;
      }
    `}}]}}),t),e([n("ha-automation-trigger-event")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{event_type:""}}},{kind:"method",key:"render",value:function(){const{event_type:e,event_data:t,context:i}=this.trigger;return a`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.event_type")}
        name="event_type"
        .value=${e}
        @change=${this._valueChanged}
      ></ha-textfield>
      <ha-yaml-editor
        .hass=${this.hass}
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.event_data")}
        .name=${"event_data"}
        .defaultValue=${t}
        @value-changed=${this._dataChanged}
      ></ha-yaml-editor>
      <br />
      ${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_users")}
      <ha-users-picker
        .pickedUserLabel=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_user_picked")}
        .pickUserLabel=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_user_pick")}
        .hass=${this.hass}
        .value=${this._wrapUsersInArray(null==i?void 0:i.user_id)}
        @value-changed=${this._usersChanged}
      ></ha-users-picker>
    `}},{kind:"method",key:"_wrapUsersInArray",value:function(e){return e?"string"==typeof e?[e]:e:[]}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),gt(this,e)}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&gt(this,e)}},{kind:"method",key:"_usersChanged",value:function(e){e.stopPropagation();const t={...this.trigger};!e.detail.value.length&&t.context?delete t.context.user_id:(t.context||(t.context={}),t.context.user_id=e.detail.value),o(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-textfield {
        display: block;
      }
    `}}]}}),t),e([n("ha-automation-trigger-geo_location")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"trigger",value:void 0},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"source",selector:{text:{}}},{name:"zone",selector:{entity:{domain:"zone"}}},{name:"event",type:"select",required:!0,options:[["enter",e("ui.panel.config.automation.editor.triggers.type.geo_location.enter")],["leave",e("ui.panel.config.automation.editor.triggers.type.geo_location.leave")]]}]))},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{source:"",zone:"",event:"enter"}}},{kind:"method",key:"render",value:function(){return a`
      <ha-form
        .schema=${this._schema(this.hass.localize)}
        .data=${this.trigger}
        .hass=${this.hass}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.geo_location.${e.name}`)}}]}}),t),e([n("ha-automation-trigger-homeassistant")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"trigger",value:void 0},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"event",type:"select",required:!0,options:[["start",e("ui.panel.config.automation.editor.triggers.type.homeassistant.start")],["shutdown",e("ui.panel.config.automation.editor.triggers.type.homeassistant.shutdown")]]}]))},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{event:"start"}}},{kind:"method",key:"render",value:function(){return a`
      <ha-form
        .schema=${this._schema(this.hass.localize)}
        .data=${this.trigger}
        .hass=${this.hass}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.geo_location.${e.name}`)}},{kind:"field",static:!0,key:"styles",value:()=>l`
    label {
      display: flex;
      align-items: center;
    }
  `}]}}),t);const ut=[{name:"topic",required:!0,selector:{text:{}}},{name:"payload",selector:{text:{}}}];e([n("ha-automation-trigger-mqtt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{topic:""}}},{kind:"method",key:"render",value:function(){return a`
      <ha-form
        .schema=${ut}
        .data=${this.trigger}
        .hass=${this.hass}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.mqtt.${e.name}`)}}]}}),t),e([n("ha-automation-trigger-numeric_state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"entity_id",required:!0,selector:{entity:{}}},{name:"attribute",selector:{attribute:{entity_id:e}}},{name:"above",selector:{text:{}}},{name:"below",selector:{text:{}}},{name:"value_template",selector:{text:{multiline:!0}}},{name:"for",selector:{duration:{}}}]))},{kind:"method",key:"willUpdate",value:function(e){e.has("trigger")&&this.trigger&&tt(this.trigger)&&o(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support")))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:""}}},{kind:"method",key:"render",value:function(){const e=Ve(this.trigger.for),t={...this.trigger,for:e},i=this._schema(this.trigger.entity_id);return a`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${i}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"entity_id":return this.hass.localize("ui.components.entity.entity-picker.entity");case"attribute":return this.hass.localize("ui.components.entity.entity-attribute-picker.attribute");case"for":return this.hass.localize("ui.panel.config.automation.editor.triggers.type.state.for");default:return this.hass.localize(`ui.panel.config.automation.editor.triggers.type.numeric_state.${e.name}`)}}}}]}}),t);const ht=ie(We,S({platform:K("state"),entity_id:W(V()),attribute:W(V()),from:W(V()),to:W(V()),for:W(Y([V(),Re]))}));e([n("ha-automation-trigger-state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:""}}},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"entity_id",required:!0,selector:{entity:{}}},{name:"attribute",selector:{attribute:{entity_id:e}}},{name:"from",selector:{text:{}}},{name:"to",selector:{text:{}}},{name:"for",selector:{duration:{}}}]))},{kind:"method",key:"shouldUpdate",value:function(e){if(!e.has("trigger"))return!0;if(this.trigger.for&&"object"==typeof this.trigger.for&&0===this.trigger.for.milliseconds&&delete this.trigger.for.milliseconds,this.trigger&&tt(this.trigger))return o(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))),!1;try{X(this.trigger,ht)}catch(e){return o(this,"ui-mode-not-available",e),!1}return!0}},{kind:"method",key:"render",value:function(){const e=Ve(this.trigger.for),t={...this.trigger,for:e},i=this._schema(this.trigger.entity_id);return a`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${i}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize("entity_id"===e.name?"ui.components.entity.entity-picker.entity":`ui.panel.config.automation.editor.triggers.type.state.${e.name}`)}}]}}),t),e([n("ha-automation-trigger-sun")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"trigger",value:void 0},{kind:"field",key:"_schema",value:()=>v((e=>[{name:"event",type:"select",required:!0,options:[["sunrise",e("ui.panel.config.automation.editor.triggers.type.sun.sunrise")],["sunset",e("ui.panel.config.automation.editor.triggers.type.sun.sunset")]]},{name:"offset",selector:{text:{}}}]))},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{event:"sunrise",offset:0}}},{kind:"method",key:"render",value:function(){const e=this._schema(this.hass.localize);return a`
      <ha-form
        .schema=${e}
        .data=${this.trigger}
        .hass=${this.hass}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.sun.${e.name}`)}}]}}),t);e([n("ha-automation-trigger-tag")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"field",decorators:[r()],key:"_tags",value:()=>[]},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{tag_id:""}}},{kind:"method",key:"firstUpdated",value:function(e){u(h(n.prototype),"firstUpdated",this).call(this,e),this._fetchTags()}},{kind:"method",key:"render",value:function(){const{tag_id:e}=this.trigger;return a`
      <ha-select
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.tag.label")}
        .disabled=${0===this._tags.length}
        .value=${e}
        @selected=${this._tagChanged}
      >
        ${this._tags.map((e=>a`
            <mwc-list-item .value=${e.id}>
              ${e.name||e.id}
            </mwc-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"_fetchTags",value:async function(){this._tags=await(async e=>e.callWS({type:"tag/list"}))(this.hass),this._tags.sort(((e,t)=>ce(e.name||e.id,t.name||t.id)))}},{kind:"method",key:"_tagChanged",value:function(e){o(this,"value-changed",{value:{...this.trigger,tag_id:e.target.value}})}}]}}),t),e([n("ha-automation-trigger-template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{value_template:""}}},{kind:"method",key:"render",value:function(){const{value_template:e}=this.trigger;return a`
      <ha-textarea
        name="value_template"
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.template.value_template")}
        .value=${e}
        @input=${this._valueChanged}
        dir="ltr"
        autogrow
      ></ha-textarea>
    `}},{kind:"method",key:"_valueChanged",value:function(e){gt(this,e)}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-textarea {
      display: block;
    }
  `}]}}),t),e([n("ha-automation-trigger-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[r()],key:"_inputMode",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{at:""}}},{kind:"field",key:"_schema",value:()=>v(((e,t)=>{const i=t?{entity:{domain:"input_datetime"}}:{time:{}};return[{name:"mode",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.triggers.type.time.type_value")],["input",e("ui.panel.config.automation.editor.triggers.type.time.type_input")]]},{name:"at",selector:i}]}))},{kind:"method",key:"willUpdate",value:function(e){e.has("trigger")&&this.trigger&&Array.isArray(this.trigger.at)&&o(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.editor_not_supported")))}},{kind:"method",key:"render",value:function(){var e;const t=this.trigger.at;if(Array.isArray(t))return a``;const i=null!==(e=this._inputMode)&&void 0!==e?e:(null==t?void 0:t.startsWith("input_datetime."))||(null==t?void 0:t.startsWith("sensor.")),o=this._schema(this.hass.localize,i),n={mode:i?"input":"value",...this.trigger};return a`
      <ha-form
        .hass=${this.hass}
        .data=${n}
        .schema=${o}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;this._inputMode="input"===t.mode,delete t.mode,Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.time.${e.name}`)}}]}}),t);const vt=[{name:"hours",selector:{text:{}}},{name:"minutes",selector:{text:{}}},{name:"seconds",selector:{text:{}}}];e([n("ha-automation-trigger-time_pattern")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{}}},{kind:"method",key:"render",value:function(){return a`
      <ha-form
        .hass=${this.hass}
        .schema=${vt}
        .data=${this.trigger}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;o(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.time_pattern.${e.name}`)}}]}}),t);function kt(e){return He(e)&&"zone"!==E(e)}e([n("ha-automation-trigger-webhook")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"field",decorators:[r()],key:"_config",value:void 0},{kind:"field",key:"_unsub",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{webhook_id:""}}},{kind:"method",key:"connectedCallback",value:function(){u(h(n.prototype),"connectedCallback",this).call(this);const e={callback:e=>{this._config=e}};o(this,"subscribe-automation-config",e),this._unsub=e.unsub}},{kind:"method",key:"disconnectedCallback",value:function(){u(h(n.prototype),"disconnectedCallback",this).call(this),this._unsub&&this._unsub()}},{kind:"method",key:"_generateWebhookId",value:function(){var e;const t=crypto.getRandomValues(new Uint8Array(18)),i=btoa(String.fromCharCode(...t)).replace(/\+/g,"-").replace(/\//g,"_");return`${((e,t="_")=>{const i="àáäâãåăæąçćčđďèéěėëêęğǵḧìíïîįłḿǹńňñòóöôœøṕŕřßşśšșťțùúüûǘůűūųẃẍÿýźžż·/_,:;",a=`aaaaaaaaacccddeeeeeeegghiiiiilmnnnnooooooprrsssssttuuuuuuuuuwxyyzzz${t}${t}${t}${t}${t}${t}`,o=new RegExp(i.split("").join("|"),"g");return e.toString().toLowerCase().replace(/\s+/g,t).replace(o,(e=>a.charAt(i.indexOf(e)))).replace(/&/g,`${t}and${t}`).replace(/[^\w-]+/g,"").replace(/-/g,t).replace(new RegExp(`(${t})\\1+`,"g"),"$1").replace(new RegExp(`^${t}+`),"").replace(new RegExp(`${t}+$`),"")})((null===(e=this._config)||void 0===e?void 0:e.alias)||"","-")}-${i}`}},{kind:"method",key:"willUpdate",value:function(e){u(h(n.prototype),"willUpdate",this).call(this,e),e.has("trigger")&&""===this.trigger.webhook_id&&(this.trigger.webhook_id=this._generateWebhookId())}},{kind:"method",key:"render",value:function(){const{webhook_id:e}=this.trigger;return a`
      <ha-textfield
        name="webhook_id"
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.webhook_id")}
        .helper=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.webhook_id_helper")}
        iconTrailing
        .value=${e||""}
        @input=${this._valueChanged}
      >
        <ha-icon-button
          @click=${this._copyUrl}
          slot="trailingIcon"
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.copy_url")}
          .path=${_}
        ></ha-icon-button>
      </ha-textfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){gt(this,e)}},{kind:"method",key:"_copyUrl",value:async function(e){const t=e.target.parentElement,i=this.hass.hassUrl(`/api/webhook/${t.value}`);await(async e=>{if(navigator.clipboard)try{return void await navigator.clipboard.writeText(e)}catch{}const t=document.createElement("textarea");t.value=e,document.body.appendChild(t),t.select(),document.execCommand("copy"),document.body.removeChild(t)})(i),ae(this,{message:this.hass.localize("ui.common.copied_clipboard")})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-textfield {
      display: block;
    }

    ha-textfield > ha-icon-button {
      --mdc-icon-button-size: 24px;
      --mdc-icon-size: 18px;
    }
  `}]}}),t);const pt=["zone"];e([n("ha-automation-trigger-zone")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{entity_id:"",zone:"",event:"enter"}}},{kind:"method",key:"render",value:function(){const{entity_id:e,zone:t,event:i}=this.trigger;return a`
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.entity")}
        .value=${e}
        @value-changed=${this._entityPicked}
        .hass=${this.hass}
        allow-custom-entity
        .entityFilter=${kt}
      ></ha-entity-picker>
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.zone")}
        .value=${t}
        @value-changed=${this._zonePicked}
        .hass=${this.hass}
        allow-custom-entity
        .includeDomains=${pt}
      ></ha-entity-picker>

      <label>
        ${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.event")}
        <ha-formfield
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.enter")}
        >
          <ha-radio
            name="event"
            value="enter"
            .checked=${"enter"===i}
            @change=${this._radioGroupPicked}
          ></ha-radio>
        </ha-formfield>
        <ha-formfield
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.leave")}
        >
          <ha-radio
            name="event"
            value="leave"
            .checked=${"leave"===i}
            @change=${this._radioGroupPicked}
          ></ha-radio>
        </ha-formfield>
      </label>
    `}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.trigger,entity_id:e.detail.value}})}},{kind:"method",key:"_zonePicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.trigger,zone:e.detail.value}})}},{kind:"method",key:"_radioGroupPicked",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:{...this.trigger,event:e.target.value}})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    label {
      display: flex;
      align-items: center;
    }
    ha-entity-picker {
      display: block;
      margin-bottom: 24px;
    }
  `}]}}),t);const mt=["device","event","state","geo_location","homeassistant","mqtt","numeric_state","sun","tag","template","time","time_pattern","webhook","zone"],gt=(e,t)=>{var i,a;t.stopPropagation();const n=null===(i=t.currentTarget)||void 0===i?void 0:i.name;if(!n)return;const s=null===(a=t.target)||void 0===a?void 0:a.value;if((e.trigger[n]||"")===s)return;let d;void 0===s||""===s?(d={...e.trigger},delete d[n]):d={...e.trigger,[n]:s},o(e,"value-changed",{value:d})};e([n("ha-automation-trigger-row")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"trigger",value:void 0},{kind:"field",decorators:[r()],key:"_warnings",value:void 0},{kind:"field",decorators:[r()],key:"_yamlMode",value:()=>!1},{kind:"field",decorators:[r()],key:"_requestShowId",value:()=>!1},{kind:"field",decorators:[r()],key:"_triggered",value:void 0},{kind:"field",decorators:[r()],key:"_triggerColor",value:()=>!1},{kind:"field",key:"_triggerUnsub",value:void 0},{kind:"field",key:"_processedTypes",value:()=>v((e=>mt.map((t=>[t,e(`ui.panel.config.automation.editor.triggers.type.${t}.label`)])).sort(((e,t)=>re(e[1],t[1])))))},{kind:"method",key:"render",value:function(){const e=mt.indexOf(this.trigger.platform),t=this._yamlMode||-1===e,i="id"in this.trigger||this._requestShowId;return a`
      <ha-card>
        <div class="card-content">
          <div class="card-menu">
            <ha-button-menu corner="BOTTOM_START" @action=${this._handleAction}>
              <ha-icon-button
                slot="trigger"
                .label=${this.hass.localize("ui.common.menu")}
                .path=${c}
              ></ha-icon-button>
              <mwc-list-item>
                ${this.hass.localize("ui.panel.config.automation.editor.triggers.edit_id")}
              </mwc-list-item>
              <mwc-list-item .disabled=${-1===e}>
                ${t?this.hass.localize("ui.panel.config.automation.editor.edit_ui"):this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
              </mwc-list-item>
              <mwc-list-item>
                ${this.hass.localize("ui.panel.config.automation.editor.actions.duplicate")}
              </mwc-list-item>
              <mwc-list-item class="warning">
                ${this.hass.localize("ui.panel.config.automation.editor.actions.delete")}
              </mwc-list-item>
            </ha-button-menu>
          </div>
          ${this._warnings?a`<ha-alert
                alert-type="warning"
                .title=${this.hass.localize("ui.errors.config.editor_not_supported")}
              >
                ${this._warnings.length&&void 0!==this._warnings[0]?a` <ul>
                      ${this._warnings.map((e=>a`<li>${e}</li>`))}
                    </ul>`:""}
                ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
              </ha-alert>`:""}
          ${t?a`
                ${-1===e?a`
                      ${this.hass.localize("ui.panel.config.automation.editor.triggers.unsupported_platform","platform",this.trigger.platform)}
                    `:""}
                <h2>
                  ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
                </h2>
                <ha-yaml-editor
                  .hass=${this.hass}
                  .defaultValue=${this.trigger}
                  @value-changed=${this._onYamlChange}
                ></ha-yaml-editor>
              `:a`
                <ha-select
                  .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type_select")}
                  .value=${this.trigger.platform}
                  naturalMenuWidth
                  @selected=${this._typeChanged}
                >
                  ${this._processedTypes(this.hass.localize).map((([e,t])=>a`
                      <mwc-list-item .value=${e}>${t}</mwc-list-item>
                    `))}
                </ha-select>

                ${i?a`
                      <ha-textfield
                        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.id")}
                        .value=${this.trigger.id||""}
                        @change=${this._idChanged}
                      >
                      </ha-textfield>
                    `:""}
                <div @ui-mode-not-available=${this._handleUiModeNotAvailable}>
                  ${le(`ha-automation-trigger-${this.trigger.platform}`,{hass:this.hass,trigger:this.trigger})}
                </div>
              `}
        </div>
        <div
          class="triggered ${p({active:void 0!==this._triggered,accent:this._triggerColor})}"
          @click=${this._showTriggeredInfo}
        >
          ${this.hass.localize("ui.panel.config.automation.editor.triggers.triggered")}
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){u(h(n.prototype),"updated",this).call(this,e),e.has("trigger")&&this._subscribeTrigger()}},{kind:"method",key:"connectedCallback",value:function(){u(h(n.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.trigger&&this._subscribeTrigger()}},{kind:"method",key:"disconnectedCallback",value:function(){u(h(n.prototype),"disconnectedCallback",this).call(this),this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0),this._doSubscribeTrigger.cancel()}},{kind:"method",key:"_subscribeTrigger",value:function(){this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0),this._doSubscribeTrigger()}},{kind:"field",key:"_doSubscribeTrigger",value(){return I((async()=>{let e;const t=this.trigger;this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0);if(!(await Ae(this.hass,{trigger:t})).trigger.valid||this.trigger!==t)return;const i=ge(this.hass,(t=>{void 0!==e?(clearTimeout(e),this._triggerColor=!this._triggerColor):this._triggerColor=!1,this._triggered=t,e=window.setTimeout((()=>{this._triggered=void 0,e=void 0}),5e3)}),t);i.catch((()=>{this._triggerUnsub===i&&(this._triggerUnsub=void 0)})),this._triggerUnsub=i}),5e3)}},{kind:"method",key:"_handleUiModeNotAvailable",value:function(e){this._warnings=ue(this.hass,e.detail).warnings,this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"_handleAction",value:function(e){switch(e.detail.index){case 0:this._requestShowId=!0;break;case 1:this._switchYamlMode();break;case 2:o(this,"duplicate");break;case 3:this._onDelete()}}},{kind:"method",key:"_onDelete",value:function(){T(this,{text:this.hass.localize("ui.panel.config.automation.editor.triggers.delete_confirm"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),confirm:()=>{o(this,"value-changed",{value:null})}})}},{kind:"method",key:"_typeChanged",value:function(e){const t=e.target.value;if(!t)return;const i=customElements.get(`ha-automation-trigger-${t}`);if(t!==this.trigger.platform){const e={platform:t,...i.defaultConfig};this.trigger.id&&(e.id=this.trigger.id),o(this,"value-changed",{value:e})}}},{kind:"method",key:"_idChanged",value:function(e){var t;const i=e.target.value;if(i===(null!==(t=this.trigger.id)&&void 0!==t?t:""))return;this._requestShowId=!0;const a={...this.trigger};i?a.id=i:delete a.id,o(this,"value-changed",{value:a})}},{kind:"method",key:"_onYamlChange",value:function(e){e.stopPropagation(),e.detail.isValid&&(this._warnings=void 0,o(this,"value-changed",{value:e.detail.value}))}},{kind:"method",key:"_switchYamlMode",value:function(){this._warnings=void 0,this._yamlMode=!this._yamlMode}},{kind:"method",key:"_showTriggeredInfo",value:function(){M(this,{text:a`
        <ha-yaml-editor
          readOnly
          .hass=${this.hass}
          .defaultValue=${this._triggered}
        ></ha-yaml-editor>
      `})}},{kind:"get",static:!0,key:"styles",value:function(){return[d,l`
        .card-menu {
          float: right;
          z-index: 3;
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
        }
        .rtl .card-menu {
          float: left;
        }
        .triggered {
          cursor: pointer;
          position: absolute;
          top: 0px;
          right: 0px;
          left: 0px;
          text-transform: uppercase;
          font-weight: bold;
          font-size: 14px;
          background-color: var(--primary-color);
          color: var(--text-primary-color);
          max-height: 0px;
          overflow: hidden;
          transition: max-height 0.3s;
          text-align: center;
          border-top-right-radius: var(--ha-card-border-radius, 4px);
          border-top-left-radius: var(--ha-card-border-radius, 4px);
        }
        .triggered.active {
          max-height: 100px;
        }
        .triggered:hover {
          opacity: 0.8;
        }
        .triggered.accent {
          background-color: var(--accent-color);
          color: var(--text-accent-color, var(--text-primary-color));
        }
        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
        ha-select {
          margin-bottom: 24px;
        }
        ha-textfield {
          display: block;
          margin-bottom: 24px;
        }
      `]}}]}}),t),e([n("ha-automation-trigger")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"triggers",value:void 0},{kind:"method",key:"render",value:function(){return a`
      ${this.triggers.map(((e,t)=>a`
          <ha-automation-trigger-row
            .index=${t}
            .trigger=${e}
            @duplicate=${this._duplicateTrigger}
            @value-changed=${this._triggerChanged}
            .hass=${this.hass}
          ></ha-automation-trigger-row>
        `))}
      <ha-card>
        <div class="card-actions add-card">
          <mwc-button @click=${this._addTrigger}>
            ${this.hass.localize("ui.panel.config.automation.editor.triggers.add")}
          </mwc-button>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_addTrigger",value:function(){const e=this.triggers.concat({platform:"device",...rt.defaultConfig});o(this,"value-changed",{value:e})}},{kind:"method",key:"_triggerChanged",value:function(e){e.stopPropagation();const t=[...this.triggers],i=e.detail.value,a=e.target.index;null===i?t.splice(a,1):t[a]=i,o(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateTrigger",value:function(e){e.stopPropagation();const t=e.target.index;o(this,"value-changed",{value:this.triggers.concat(this.triggers[t])})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-automation-trigger-row,
      ha-card {
        display: block;
        margin-top: 16px;
      }
      .add-card mwc-button {
        display: block;
        text-align: center;
      }
    `}}]}}),t),e([n("ha-automation-action-wait_for_trigger")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{wait_for_trigger:[]}}},{kind:"method",key:"render",value:function(){const{wait_for_trigger:e,continue_on_timeout:t,timeout:i}=this.action;return a`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.wait_for_trigger.timeout")}
        .name=${"timeout"}
        .value=${i||""}
        @change=${this._valueChanged}
      ></ha-textfield>
      <ha-formfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type.wait_for_trigger.continue_timeout")}
      >
        <ha-switch
          .checked=${null==t||t}
          @change=${this._continueChanged}
        ></ha-switch>
      </ha-formfield>
      <ha-automation-trigger
        .triggers=${e}
        .hass=${this.hass}
        .name=${"wait_for_trigger"}
        @value-changed=${this._valueChanged}
      ></ha-automation-trigger>
    `}},{kind:"method",key:"_continueChanged",value:function(e){o(this,"value-changed",{value:{...this.action,continue_on_timeout:e.target.checked}})}},{kind:"method",key:"_valueChanged",value:function(e){bt(this,e)}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-textfield {
        display: block;
        margin-bottom: 24px;
      }
    `}}]}}),t);const yt=[{name:"wait_template",selector:{text:{multiline:!0}}},{name:"timeout",required:!1,selector:{text:{}}},{name:"continue_on_timeout",selector:{boolean:{}}}];e([n("ha-automation-action-wait_template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"action",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{wait_template:""}}},{kind:"method",key:"render",value:function(){return a`
      <ha-form
        .hass=${this.hass}
        .data=${this.action}
        .schema=${yt}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.actions.type.wait_template.${"continue_on_timeout"===e.name?"continue_timeout":e.name}`)}}]}}),t);const ft=["condition","delay","event","play_media","activate_scene","service","wait_template","wait_for_trigger","repeat","choose","device_id"],_t=e=>{if(e)return"service"in e||"scene"in e?oe(e):ft.find((t=>t in e))},bt=(e,t)=>{var i,a;t.stopPropagation();const n=null===(i=t.target)||void 0===i?void 0:i.name;if(!n)return;const s=(null===(a=t.detail)||void 0===a?void 0:a.value)||t.target.value;if((e.action[n]||"")===s)return;let d;s?d={...e.action,[n]:s}:(d={...e.action},delete d[n]),o(e,"value-changed",{value:d})};e([n("ha-automation-action-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"action",value:void 0},{kind:"field",decorators:[i()],key:"index",value:void 0},{kind:"field",decorators:[i()],key:"totalActions",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[r()],key:"_warnings",value:void 0},{kind:"field",decorators:[r()],key:"_uiModeAvailable",value:()=>!0},{kind:"field",decorators:[r()],key:"_yamlMode",value:()=>!1},{kind:"field",decorators:[k("ha-yaml-editor")],key:"_yamlEditor",value:void 0},{kind:"field",key:"_processedTypes",value:()=>v((e=>ft.map((t=>[t,e(`ui.panel.config.automation.editor.actions.type.${t}.label`)])).sort(((e,t)=>re(e[1],t[1])))))},{kind:"method",key:"willUpdate",value:function(e){e.has("action")&&(this._uiModeAvailable=void 0!==_t(this.action),this._uiModeAvailable||this._yamlMode||(this._yamlMode=!0))}},{kind:"method",key:"updated",value:function(e){if(e.has("action")&&this._yamlMode){const e=this._yamlEditor;e&&e.value!==this.action&&e.setValue(this.action)}}},{kind:"method",key:"render",value:function(){const e=_t(this.action),t=this._yamlMode;return a`
      <ha-card>
        <div class="card-content">
          <div class="card-menu">
            ${0!==this.index?a`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.panel.config.automation.editor.move_up")}
                    .path=${b}
                    @click=${this._moveUp}
                  ></ha-icon-button>
                `:""}
            ${this.index!==this.totalActions-1?a`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.panel.config.automation.editor.move_down")}
                    .path=${$}
                    @click=${this._moveDown}
                  ></ha-icon-button>
                `:""}
            <ha-button-menu corner="BOTTOM_START" @action=${this._handleAction}>
              <ha-icon-button
                slot="trigger"
                .label=${this.hass.localize("ui.common.menu")}
                .path=${c}
              ></ha-icon-button>
              <mwc-list-item>
                ${this.hass.localize("ui.panel.config.automation.editor.actions.run_action")}
              </mwc-list-item>
              <mwc-list-item .disabled=${!this._uiModeAvailable}>
                ${t?this.hass.localize("ui.panel.config.automation.editor.edit_ui"):this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
              </mwc-list-item>
              <mwc-list-item>
                ${this.hass.localize("ui.panel.config.automation.editor.actions.duplicate")}
              </mwc-list-item>
              <mwc-list-item class="warning">
                ${this.hass.localize("ui.panel.config.automation.editor.actions.delete")}
              </mwc-list-item>
            </ha-button-menu>
          </div>
          ${this._warnings?a`<ha-alert
                alert-type="warning"
                .title=${this.hass.localize("ui.errors.config.editor_not_supported")}
              >
                ${this._warnings.length>0&&void 0!==this._warnings[0]?a` <ul>
                      ${this._warnings.map((e=>a`<li>${e}</li>`))}
                    </ul>`:""}
                ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
              </ha-alert>`:""}
          ${t?a`
                ${void 0===e?a`
                      ${this.hass.localize("ui.panel.config.automation.editor.actions.unsupported_action","action",e)}
                    `:""}
                <h2>
                  ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
                </h2>
                <ha-yaml-editor
                  .hass=${this.hass}
                  .defaultValue=${this.action}
                  @value-changed=${this._onYamlChange}
                ></ha-yaml-editor>
              `:a`
                <ha-select
                  .label=${this.hass.localize("ui.panel.config.automation.editor.actions.type_select")}
                  .value=${_t(this.action)}
                  naturalMenuWidth
                  @selected=${this._typeChanged}
                >
                  ${this._processedTypes(this.hass.localize).map((([e,t])=>a`
                      <mwc-list-item .value=${e}>${t}</mwc-list-item>
                    `))}
                </ha-select>

                <div @ui-mode-not-available=${this._handleUiModeNotAvailable}>
                  ${le(`ha-automation-action-${e}`,{hass:this.hass,action:this.action,narrow:this.narrow})}
                </div>
              `}
        </div>
      </ha-card>
    `}},{kind:"method",key:"_handleUiModeNotAvailable",value:function(e){e.stopPropagation(),this._warnings=ue(this.hass,e.detail).warnings,this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"_moveUp",value:function(){o(this,"move-action",{direction:"up"})}},{kind:"method",key:"_moveDown",value:function(){o(this,"move-action",{direction:"down"})}},{kind:"method",key:"_handleAction",value:function(e){switch(e.detail.index){case 0:this._runAction();break;case 1:this._switchYamlMode();break;case 2:o(this,"duplicate");break;case 3:this._onDelete()}}},{kind:"method",key:"_runAction",value:async function(){const e=await Ae(this.hass,{action:this.action});if(e.action.valid){try{await(t=this.hass,i=this.action,t.callWS({type:"execute_script",sequence:i}))}catch(e){return void M(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.run_action_error"),text:e.message||e})}var t,i;ae(this,{message:this.hass.localize("ui.panel.config.automation.editor.actions.run_action_success")})}else M(this,{title:this.hass.localize("ui.panel.config.automation.editor.actions.invalid_action"),text:e.action.error})}},{kind:"method",key:"_onDelete",value:function(){T(this,{text:this.hass.localize("ui.panel.config.automation.editor.actions.delete_confirm"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),confirm:()=>{o(this,"value-changed",{value:null})}})}},{kind:"method",key:"_typeChanged",value:function(e){const t=e.target.value;if(t&&(this._uiModeAvailable=ft.includes(t),this._uiModeAvailable||this._yamlMode||(this._yamlMode=!1),t!==_t(this.action))){const e=customElements.get(`ha-automation-action-${t}`);o(this,"value-changed",{value:{...e.defaultConfig}})}}},{kind:"method",key:"_onYamlChange",value:function(e){e.stopPropagation(),e.detail.isValid&&o(this,"value-changed",{value:e.detail.value})}},{kind:"method",key:"_switchYamlMode",value:function(){this._warnings=void 0,this._yamlMode=!this._yamlMode}},{kind:"get",static:!0,key:"styles",value:function(){return[d,l`
        .card-menu {
          position: absolute;
          right: 16px;
          z-index: 3;
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
        }
        .rtl .card-menu {
          right: initial;
          left: 16px;
        }
        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
        .warning {
          margin-bottom: 8px;
        }
        .warning ul {
          margin: 4px 0;
        }
        ha-select {
          margin-bottom: 24px;
        }
      `]}}]}}),t),e([n("ha-automation-action")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[i()],key:"actions",value:void 0},{kind:"method",key:"render",value:function(){return a`
      ${this.actions.map(((e,t)=>a`
          <ha-automation-action-row
            .index=${t}
            .totalActions=${this.actions.length}
            .action=${e}
            .narrow=${this.narrow}
            @duplicate=${this._duplicateAction}
            @move-action=${this._move}
            @value-changed=${this._actionChanged}
            .hass=${this.hass}
          ></ha-automation-action-row>
        `))}
      <ha-card>
        <div class="card-actions add-card">
          <mwc-button @click=${this._addAction}>
            ${this.hass.localize("ui.panel.config.automation.editor.actions.add")}
          </mwc-button>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_addAction",value:function(){const e=this.actions.concat({...it.defaultConfig});o(this,"value-changed",{value:e})}},{kind:"method",key:"_move",value:function(e){e.stopPropagation();const t=e.target.index,i="up"===e.detail.direction?t-1:t+1,a=this.actions.concat(),n=a.splice(t,1)[0];a.splice(i,0,n),o(this,"value-changed",{value:a})}},{kind:"method",key:"_actionChanged",value:function(e){e.stopPropagation();const t=[...this.actions],i=e.detail.value,a=e.target.index;null===i?t.splice(a,1):t[a]=i,o(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateAction",value:function(e){e.stopPropagation();const t=e.target.index;o(this,"value-changed",{value:this.actions.concat(this.actions[t])})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-automation-action-row,
      ha-card {
        display: block;
        margin-top: 16px;
      }
      .add-card mwc-button {
        display: block;
        text-align: center;
      }
    `}}]}}),t),e([n("ha-selector-action")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){return a`<ha-automation-action
      .disabled=${this.disabled}
      .actions=${this.value||[]}
      .hass=${this.hass}
    ></ha-automation-action>`}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-automation-action {
        display: block;
        margin-bottom: 16px;
      }
      :host([disabled]) ha-automation-action {
        opacity: var(--light-disabled-opacity);
        pointer-events: none;
      }
    `}}]}}),t);const $t=async e=>((e,t,i,a)=>{const[o,n,s]=e.split(".",3);return Number(o)>t||Number(o)===t&&(void 0===a?Number(n)>=i:Number(n)>i)||void 0!==a&&Number(o)===t&&Number(n)===i&&Number(s)>=a})(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(await e.callApi("GET","hassio/supervisor/info")).data,xt=e=>a`<mwc-list-item twoline graphic="icon">
  <span>${e.name}</span>
  <span slot="secondary">${e.slug}</span>
  ${e.icon?a`<img slot="graphic" .src="/api/hassio/addons/${e.slug}/icon" />`:""}
</mwc-list-item>`;e([n("ha-addon-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"value",value:()=>""},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[r()],key:"_addons",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[k("ha-combo-box")],key:"_comboBox",value:void 0},{kind:"method",key:"open",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this._comboBox)||void 0===e||e.focus()}},{kind:"method",key:"firstUpdated",value:function(){this._getAddons()}},{kind:"method",key:"render",value:function(){return this._addons?a`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${xt}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:a``}},{kind:"method",key:"_getAddons",value:async function(){try{if(B(this.hass,"hassio")){const e=await $t(this.hass);this._addons=e.addons.sort(((e,t)=>re(e.name,t.name)))}else M(this,{title:this.hass.localize("ui.componencts.addon-picker.error.no_supervisor.title"),text:this.hass.localize("ui.componencts.addon-picker.error.no_supervisor.description")})}catch(e){M(this,{title:this.hass.localize("ui.componencts.addon-picker.error.fetch_addons.title"),text:this.hass.localize("ui.componencts.addon-picker.error.fetch_addons.description")})}}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_addonChanged",value:function(e){e.stopPropagation();const t=e.detail.value;t!==this._value&&this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{o(this,"value-changed",{value:e}),o(this,"change")}),0)}}]}}),t),e([n("ha-selector-addon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-addon-picker {
      width: 100%;
    }
  `}]}}),t),e([n("ha-areas-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i()],key:"placeholder",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"no-add"})],key:"noAdd",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[i()],key:"deviceFilter",value:void 0},{kind:"field",decorators:[i()],key:"entityFilter",value:void 0},{kind:"field",decorators:[i({attribute:"picked-area-label"})],key:"pickedAreaLabel",value:void 0},{kind:"field",decorators:[i({attribute:"pick-area-label"})],key:"pickAreaLabel",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return a``;const e=this._currentAreas;return a`
      ${e.map((e=>a`
          <div>
            <ha-area-picker
              .curValue=${e}
              .noAdd=${this.noAdd}
              .hass=${this.hass}
              .value=${e}
              .label=${this.pickedAreaLabel}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .disabled=${this.disabled}
              @value-changed=${this._areaChanged}
            ></ha-area-picker>
          </div>
        `))}
      <div>
        <ha-area-picker
          .noAdd=${this.noAdd}
          .hass=${this.hass}
          .label=${this.pickAreaLabel}
          .helper=${this.helper}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .disabled=${this.disabled}
          .placeholder=${this.placeholder}
          .required=${this.required&&!e.length}
          @value-changed=${this._addArea}
        ></ha-area-picker>
      </div>
    `}},{kind:"get",key:"_currentAreas",value:function(){return this.value||[]}},{kind:"method",key:"_updateAreas",value:async function(e){this.value=e,o(this,"value-changed",{value:e})}},{kind:"method",key:"_areaChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t)return;const a=this._currentAreas;i&&!a.includes(i)?this._updateAreas(a.map((e=>e===t?i:e))):this._updateAreas(a.filter((e=>e!==t)))}},{kind:"method",key:"_addArea",value:function(e){e.stopPropagation();const t=e.detail.value;if(!t)return;e.currentTarget.value="";const i=this._currentAreas;i.includes(t)||this._updateAreas([...i,t])}},{kind:"field",static:!0,key:"styles",value:()=>l`
    div {
      margin-top: 8px;
    }
  `}]}}),we(t)),e([n("ha-selector-area")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[r()],key:"_configEntries",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"updated",value:function(e){if(e.has("selector")){var t;e.get("selector")!==this.selector&&null!==(t=this.selector.area.device)&&void 0!==t&&t.integration&&xe(this.hass,{domain:this.selector.area.device.integration}).then((e=>{this._configEntries=e}))}}},{kind:"method",key:"render",value:function(){var e,t,i,o;return this.selector.area.multiple?a`
      <ha-areas-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .pickAreaLabel=${this.label}
        no-add
        .deviceFilter=${this._filterDevices}
        .entityFilter=${this._filterEntities}
        .includeDeviceClasses=${null!==(e=this.selector.area.entity)&&void 0!==e&&e.device_class?[this.selector.area.entity.device_class]:void 0}
        .includeDomains=${null!==(t=this.selector.area.entity)&&void 0!==t&&t.domain?[this.selector.area.entity.domain]:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-areas-picker>
    `:a`
        <ha-area-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          no-add
          .deviceFilter=${this._filterDevices}
          .entityFilter=${this._filterEntities}
          .includeDeviceClasses=${null!==(i=this.selector.area.entity)&&void 0!==i&&i.device_class?[this.selector.area.entity.device_class]:void 0}
          .includeDomains=${null!==(o=this.selector.area.entity)&&void 0!==o&&o.domain?[this.selector.area.entity.domain]:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
        ></ha-area-picker>
      `}},{kind:"field",key:"_filterEntities",value(){return e=>{var t;return null===(t=this.selector.area.entity)||void 0===t||!t.integration||e.platform===this.selector.area.entity.integration}}},{kind:"field",key:"_filterDevices",value(){return e=>{var t,i,a;return(null===(t=this.selector.area.device)||void 0===t||!t.manufacturer||e.manufacturer===this.selector.area.device.manufacturer)&&((null===(i=this.selector.area.device)||void 0===i||!i.model||e.model===this.selector.area.device.model)&&!(null!==(a=this.selector.area.device)&&void 0!==a&&a.integration&&this._configEntries&&!this._configEntries.some((t=>e.config_entries.includes(t.entry_id)))))}}}]}}),t),e([n("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"entityId",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"_opened",value:()=>!1},{kind:"field",decorators:[k("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes).map((e=>({value:e,label:ne(e)}))):[]}}},{kind:"method",key:"render",value:function(){var e;return this.hass?a`
      <ha-combo-box
        .hass=${this.hass}
        .value=${this.value||""}
        .autofocus=${this.autofocus}
        .label=${null!==(e=this.label)&&void 0!==e?e:this.hass.localize("ui.components.entity.entity-attribute-picker.attribute")}
        .disabled=${this.disabled||!this.entityId}
        .required=${this.required}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomValue}
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
      </ha-combo-box>
    `:a``}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value}}]}}),t),e([n("ha-selector-attribute")],(function(e,t){class n extends t{constructor(...t){super(...t),e(this)}}return{F:n,d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[i()],key:"context",value:void 0},{kind:"method",key:"render",value:function(){var e;return a`
      <ha-entity-attribute-picker
        .hass=${this.hass}
        .entityId=${this.selector.attribute.entity_id||(null===(e=this.context)||void 0===e?void 0:e.filter_entity)}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `}},{kind:"method",key:"updated",value:function(e){if(u(h(n.prototype),"updated",this).call(this,e),!this.value||this.selector.attribute.entity_id||!e.has("context"))return;const t=e.get("context");if(!this.context||(null==t?void 0:t.filter_entity)===this.context.filter_entity)return;let i=!1;if(this.context.filter_entity){const e=this.hass.states[this.context.filter_entity];e&&this.value in e.attributes||(i=!0)}else i=void 0!==this.value;i&&o(this,"value-changed",{value:void 0})}}]}}),we(t)),e([n("ha-selector-boolean")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <ha-formfield alignEnd spaceBetween .label=${this.label}>
        <ha-switch
          .checked=${this.value}
          @change=${this._handleChange}
          .disabled=${this.disabled}
        ></ha-switch>
      </ha-formfield>
      ${this.helper?a`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"method",key:"_handleChange",value:function(e){const t=e.target.checked;this.value!==t&&o(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-formfield {
        display: flex;
        height: 56px;
        align-items: center;
        --mdc-typography-body2-font-size: 1em;
      }
    `}}]}}),t),e([n("ha-selector-color_rgb")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`
      <ha-textfield
        type="color"
        helperPersistent
        .value=${this.value?x(this.value):""}
        .label=${this.label||""}
        .required=${this.required}
        .helper=${this.helper}
        .disalbled=${this.disabled}
        @change=${this._valueChanged}
      ></ha-textfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.target.value;o(this,"value-changed",{value:w(t)})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    :host {
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }
    ha-textfield {
      --text-field-padding: 8px;
      min-width: 75px;
      flex-grow: 1;
      margin: 0 4px;
    }
  `}]}}),t),e([n("ha-selector-date")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`
      <ha-date-input
        .label=${this.label}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .value=${this.value}
        .required=${this.required}
        .helper=${this.helper}
      >
      </ha-date-input>
    `}}]}}),t),e([n("ha-selector-datetime")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[k("ha-date-input")],key:"_dateInput",value:void 0},{kind:"field",decorators:[k("ha-time-input")],key:"_timeInput",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=null===(e=this.value)||void 0===e?void 0:e.split(" ");return a`
      <div class="input">
        <ha-date-input
          .label=${this.label}
          .locale=${this.hass.locale}
          .disabled=${this.disabled}
          .required=${this.required}
          .value=${null==t?void 0:t[0]}
          @value-changed=${this._valueChanged}
        >
        </ha-date-input>
        <ha-time-input
          enable-second
          .value=${(null==t?void 0:t[1])||"0:00:00"}
          .locale=${this.hass.locale}
          .disabled=${this.disabled}
          .required=${this.required}
          @value-changed=${this._valueChanged}
        ></ha-time-input>
      </div>
      ${this.helper?a`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),o(this,"value-changed",{value:`${this._dateInput.value} ${this._timeInput.value}`})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    .input {
      display: flex;
      align-items: center;
      flex-direction: row;
    }

    ha-date-input {
      min-width: 150px;
      margin-right: 4px;
    }
  `}]}}),t),e([n("ha-devices-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[i({attribute:"picked-device-label"}),i({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[i({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return a``;const e=this._currentDevices;return a`
      ${e.map((e=>a`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .value=${e}
              .label=${this.pickedDeviceLabel}
              @value-changed=${this._deviceChanged}
            ></ha-device-picker>
          </div>
        `))}
      <div>
        <ha-device-picker
          .hass=${this.hass}
          .helper=${this.helper}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .label=${this.pickDeviceLabel}
          .required=${this.required&&!e.length}
          @value-changed=${this._addDevice}
        ></ha-device-picker>
      </div>
    `}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){o(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;i!==t&&""===i&&(""===i?this._updateDevices(this._currentDevices.filter((e=>e!==t))):this._updateDevices(this._currentDevices.map((e=>e===t?i:e))))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentDevices;i.includes(t)||this._updateDevices([...i,t])}},{kind:"field",static:!0,key:"styles",value:()=>l`
    div {
      margin-top: 8px;
    }
  `}]}}),t),e([n("ha-selector-device")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[r()],key:"_configEntries",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"updated",value:function(e){if(e.has("selector")){var t;e.get("selector")!==this.selector&&null!==(t=this.selector.device)&&void 0!==t&&t.integration&&xe(this.hass,{domain:this.selector.device.integration}).then((e=>{this._configEntries=e}))}}},{kind:"method",key:"render",value:function(){var e,t,i,o;return this.selector.device.multiple?a`
      ${this.label?a`<label>${this.label}</label>`:""}
      <ha-devices-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .includeDeviceClasses=${null!==(e=this.selector.device.entity)&&void 0!==e&&e.device_class?[this.selector.device.entity.device_class]:void 0}
        .includeDomains=${null!==(t=this.selector.device.entity)&&void 0!==t&&t.domain?[this.selector.device.entity.domain]:void 0}
        .required=${this.required}
      ></ha-devices-picker>
    `:a`
        <ha-device-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          .deviceFilter=${this._filterDevices}
          .includeDeviceClasses=${null!==(i=this.selector.device.entity)&&void 0!==i&&i.device_class?[this.selector.device.entity.device_class]:void 0}
          .includeDomains=${null!==(o=this.selector.device.entity)&&void 0!==o&&o.domain?[this.selector.device.entity.domain]:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
          allow-custom-entity
        ></ha-device-picker>
      `}},{kind:"field",key:"_filterDevices",value(){return e=>{var t,i,a;return(null===(t=this.selector.device)||void 0===t||!t.manufacturer||e.manufacturer===this.selector.device.manufacturer)&&((null===(i=this.selector.device)||void 0===i||!i.model||e.model===this.selector.device.model)&&!(null!==(a=this.selector.device)&&void 0!==a&&a.integration&&this._configEntries&&!this._configEntries.some((t=>e.config_entries.includes(t.entry_id)))))}}}]}}),t),e([n("ha-selector-duration")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`
      <ha-duration-input
        .label=${this.label}
        .helper=${this.helper}
        .data=${this.value}
        .disabled=${this.disabled}
        .required=${this.required}
        .enableDay=${this.selector.duration.enable_day}
      ></ha-duration-input>
    `}}]}}),t);const wt=async(e,t,i,a,o,...n)=>{const s=o,d=s[e],l=d=>a&&a(o,d.result)!==d.cacheKey?(s[e]=void 0,wt(e,t,i,a,o,...n)):d.result;if(d)return d instanceof Promise?d.then(l):l(d);const r=i(o,...n);return s[e]=r,r.then((i=>{s[e]={result:i,cacheKey:null==a?void 0:a(o,i)},setTimeout((()=>{s[e]=void 0}),t)}),(()=>{s[e]=void 0})),r},Ct=(e,t)=>e.callWS({type:"entity/source",entity_id:t});e([n("ha-selector-entity")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[r()],key:"_entitySources",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return this.selector.entity.multiple?a`
      ${this.label?a`<label>${this.label}</label>`:""}
      <ha-entities-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .entityFilter=${this._filterEntities}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .required=${this.required}
      ></ha-entities-picker>
    `:a`<ha-entity-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .includeEntities=${this.selector.entity.include_entities}
        .excludeEntities=${this.selector.entity.exclude_entities}
        .entityFilter=${this._filterEntities}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-entity-picker>`}},{kind:"method",key:"updated",value:function(e){var t,i;u(h(o.prototype),"updated",this).call(this,e),e.has("selector")&&this.selector.entity.integration&&!this._entitySources&&(t=this.hass,i?Ct(t,i):wt("_entitySources",3e4,Ct,(e=>Object.keys(e.states).length),t)).then((e=>{this._entitySources=e}))}},{kind:"field",key:"_filterEntities",value(){return e=>{var t,i;const{domain:a,device_class:o,integration:n}=this.selector.entity;if(a){const t=E(e);if(Array.isArray(a)?!a.includes(t):t!==a)return!1}return(!o||e.attributes.device_class===o)&&(!n||(null===(t=this._entitySources)||void 0===t||null===(i=t[e.entity_id])||void 0===i?void 0:i.domain)===n)}}}]}}),t),e([n("ha-selector-number")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"placeholder",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){var e,t,i;const o="box"===this.selector.number.mode;return a`
      ${this.label}${this.required?"*":""}
      <div class="input">
        ${o?"":a`<ha-slider
              .min=${this.selector.number.min}
              .max=${this.selector.number.max}
              .value=${this._value}
              .step=${null!==(e=this.selector.number.step)&&void 0!==e?e:1}
              .disabled=${this.disabled}
              .required=${this.required}
              pin
              ignore-bar-touch
              @change=${this._handleSliderChange}
            >
            </ha-slider>`}
        <ha-textfield
          inputMode="numeric"
          pattern="[0-9]+([\\.][0-9]+)?"
          .label=${"box"!==this.selector.number.mode?void 0:this.label}
          .placeholder=${this.placeholder}
          class=${p({single:"box"===this.selector.number.mode})}
          .min=${this.selector.number.min}
          .max=${this.selector.number.max}
          .value=${null!==(t=this.value)&&void 0!==t?t:""}
          .step=${null!==(i=this.selector.number.step)&&void 0!==i?i:1}
          helperPersistent
          .helper=${o?this.helper:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
          .suffix=${this.selector.number.unit_of_measurement}
          type="number"
          autoValidate
          ?no-spinner=${"box"!==this.selector.number.mode}
          @input=${this._handleInputChange}
        >
        </ha-textfield>
      </div>
      ${!o&&this.helper?a`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"get",key:"_value",value:function(){var e;return null!==(e=this.value)&&void 0!==e?e:this.selector.number.min||0}},{kind:"method",key:"_handleInputChange",value:function(e){e.stopPropagation();const t=""===e.target.value||isNaN(e.target.value)?this.required?this.selector.number.min||0:void 0:Number(e.target.value);this.value!==t&&o(this,"value-changed",{value:t})}},{kind:"method",key:"_handleSliderChange",value:function(e){e.stopPropagation();const t=Number(e.target.value);this.value!==t&&o(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      .input {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      ha-slider {
        flex: 1;
      }
      ha-textfield {
        --ha-textfield-input-width: 40px;
      }
      .single {
        --ha-textfield-input-width: unset;
        flex: 1;
      }
    `}}]}}),t),e([n("ha-selector-object")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"placeholder",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`<ha-yaml-editor
      .hass=${this.hass}
      .readonly=${this.disabled}
      .required=${this.required}
      .placeholder=${this.placeholder}
      .defaultValue=${this.value}
      @value-changed=${this._handleChange}
    ></ha-yaml-editor>`}},{kind:"method",key:"_handleChange",value:function(e){const t=e.target.value;e.target.isValid&&this.value!==t&&o(this,"value-changed",{value:t})}}]}}),t),e([n("ha-target-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[i({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[i()],key:"deviceFilter",value:void 0},{kind:"field",decorators:[i()],key:"entityRegFilter",value:void 0},{kind:"field",decorators:[i()],key:"entityFilter",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[r()],key:"_areas",value:void 0},{kind:"field",decorators:[r()],key:"_devices",value:void 0},{kind:"field",decorators:[r()],key:"_entities",value:void 0},{kind:"field",decorators:[r()],key:"_addMode",value:void 0},{kind:"field",decorators:[k("#input")],key:"_inputElement",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[ze(this.hass.connection,(e=>{const t={};for(const i of e)t[i.area_id]=i;this._areas=t})),Pe(this.hass.connection,(e=>{const t={};for(const i of e)t[i.id]=i;this._devices=t})),O(this.hass.connection,(e=>{this._entities=e}))]}},{kind:"method",key:"render",value:function(){var e,t,i;return this._areas&&this._devices&&this._entities?a`<div class="mdc-chip-set items">
        ${null!==(e=this.value)&&void 0!==e&&e.area_id?he(this.value.area_id).map((e=>{const t=this._areas[e];return this._renderChip("area_id",e,(null==t?void 0:t.name)||e,void 0,C)})):""}
        ${null!==(t=this.value)&&void 0!==t&&t.device_id?he(this.value.device_id).map((e=>{const t=this._devices[e];return this._renderChip("device_id",e,t?Fe(t,this.hass):e,void 0,z)})):""}
        ${null!==(i=this.value)&&void 0!==i&&i.entity_id?he(this.value.entity_id).map((e=>{const t=this.hass.states[e];return this._renderChip("entity_id",e,t?U(t):e,t)})):""}
      </div>
      ${this._renderPicker()}
      <div class="mdc-chip-set">
        <div
          class="mdc-chip area_id add"
          .type=${"area_id"}
          @click=${this._showPicker}
        >
          <div class="mdc-chip__ripple"></div>
          <ha-svg-icon
            class="mdc-chip__icon mdc-chip__icon--leading"
            .path=${m}
          ></ha-svg-icon>
          <span role="gridcell">
            <span role="button" tabindex="0" class="mdc-chip__primary-action">
              <span class="mdc-chip__text"
                >${this.hass.localize("ui.components.target-picker.add_area_id")}</span
              >
            </span>
          </span>
        </div>
        <div
          class="mdc-chip device_id add"
          .type=${"device_id"}
          @click=${this._showPicker}
        >
          <div class="mdc-chip__ripple"></div>
          <ha-svg-icon
            class="mdc-chip__icon mdc-chip__icon--leading"
            .path=${m}
          ></ha-svg-icon>
          <span role="gridcell">
            <span role="button" tabindex="0" class="mdc-chip__primary-action">
              <span class="mdc-chip__text"
                >${this.hass.localize("ui.components.target-picker.add_device_id")}</span
              >
            </span>
          </span>
        </div>
        <div
          class="mdc-chip entity_id add"
          .type=${"entity_id"}
          @click=${this._showPicker}
        >
          <div class="mdc-chip__ripple"></div>
          <ha-svg-icon
            class="mdc-chip__icon mdc-chip__icon--leading"
            .path=${m}
          ></ha-svg-icon>
          <span role="gridcell">
            <span role="button" tabindex="0" class="mdc-chip__primary-action">
              <span class="mdc-chip__text"
                >${this.hass.localize("ui.components.target-picker.add_entity_id")}</span
              >
            </span>
          </span>
        </div>
      </div>

      ${this.helper?a`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""} `:a``}},{kind:"method",key:"_showPicker",value:async function(e){this._addMode=e.currentTarget.type,await this.updateComplete,setTimeout((()=>{var e,t;null===(e=this._inputElement)||void 0===e||e.open(),null===(t=this._inputElement)||void 0===t||t.focus()}),0)}},{kind:"method",key:"_renderChip",value:function(e,t,i,o,n){return a`
      <div
        class="mdc-chip ${p({[e]:!0})}"
      >
        ${n?a`<ha-svg-icon
              class="mdc-chip__icon mdc-chip__icon--leading"
              .path=${n}
            ></ha-svg-icon>`:""}
        ${o?a`<ha-state-icon
              class="mdc-chip__icon mdc-chip__icon--leading"
              .state=${o}
            ></ha-state-icon>`:""}
        <span role="gridcell">
          <span role="button" tabindex="0" class="mdc-chip__primary-action">
            <span class="mdc-chip__text">${i}</span>
          </span>
        </span>
        ${"entity_id"===e?"":a` <span role="gridcell">
              <ha-icon-button
                class="expand-btn mdc-chip__icon mdc-chip__icon--trailing"
                tabindex="-1"
                role="button"
                .label=${this.hass.localize("ui.components.target-picker.expand")}
                .path=${P}
                hideTooltip
                .id=${t}
                .type=${e}
                @click=${this._handleExpand}
              ></ha-icon-button>
              <paper-tooltip class="expand" animation-delay="0"
                >${this.hass.localize(`ui.components.target-picker.expand_${e}`)}</paper-tooltip
              >
            </span>`}
        <span role="gridcell">
          <ha-icon-button
            class="mdc-chip__icon mdc-chip__icon--trailing"
            tabindex="-1"
            role="button"
            .label=${this.hass.localize("ui.components.target-picker.expand")}
            .path=${f}
            hideTooltip
            .id=${t}
            .type=${e}
            @click=${this._handleRemove}
          ></ha-icon-button>
          <paper-tooltip animation-delay="0"
            >${this.hass.localize(`ui.components.target-picker.remove_${e}`)}</paper-tooltip
          >
        </span>
      </div>
    `}},{kind:"method",key:"_renderPicker",value:function(){switch(this._addMode){case"area_id":return a`<ha-area-picker
          .hass=${this.hass}
          id="input"
          .type=${"area_id"}
          .label=${this.hass.localize("ui.components.target-picker.add_area_id")}
          no-add
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityRegFilter}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeDomains=${this.includeDomains}
          @value-changed=${this._targetPicked}
        ></ha-area-picker>`;case"device_id":return a`<ha-device-picker
          .hass=${this.hass}
          id="input"
          .type=${"device_id"}
          .label=${this.hass.localize("ui.components.target-picker.add_device_id")}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityRegFilter}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeDomains=${this.includeDomains}
          @value-changed=${this._targetPicked}
        ></ha-device-picker>`;case"entity_id":return a`<ha-entity-picker
          .hass=${this.hass}
          id="input"
          .type=${"entity_id"}
          .label=${this.hass.localize("ui.components.target-picker.add_entity_id")}
          .entityFilter=${this.entityFilter}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .includeDomains=${this.includeDomains}
          @value-changed=${this._targetPicked}
          allow-custom-entity
        ></ha-entity-picker>`}return a``}},{kind:"method",key:"_targetPicked",value:function(e){if(e.stopPropagation(),!e.detail.value)return;const t=e.detail.value,i=e.currentTarget;i.value="",this._addMode=void 0,o(this,"value-changed",{value:this.value?{...this.value,[i.type]:this.value[i.type]?[...he(this.value[i.type]),t]:t}:{[i.type]:t}})}},{kind:"method",key:"_handleExpand",value:function(e){const t=e.currentTarget,i=[],a=[];if("area_id"===t.type)Object.values(this._devices).forEach((e=>{var a;e.area_id!==t.id||null!==(a=this.value.device_id)&&void 0!==a&&a.includes(e.id)||!this._deviceMeetsFilter(e)||i.push(e.id)})),this._entities.forEach((e=>{var i;e.area_id!==t.id||null!==(i=this.value.entity_id)&&void 0!==i&&i.includes(e.entity_id)||!this._entityRegMeetsFilter(e)||a.push(e.entity_id)}));else{if("device_id"!==t.type)return;this._entities.forEach((e=>{var i;e.device_id!==t.id||null!==(i=this.value.entity_id)&&void 0!==i&&i.includes(e.entity_id)||!this._entityRegMeetsFilter(e)||a.push(e.entity_id)}))}let n=this.value;a.length&&(n=this._addItems(n,"entity_id",a)),i.length&&(n=this._addItems(n,"device_id",i)),n=this._removeItem(n,t.type,t.id),o(this,"value-changed",{value:n})}},{kind:"method",key:"_handleRemove",value:function(e){const t=e.currentTarget;o(this,"value-changed",{value:this._removeItem(this.value,t.type,t.id)})}},{kind:"method",key:"_addItems",value:function(e,t,i){return{...e,[t]:e[t]?he(e[t]).concat(i):i}}},{kind:"method",key:"_removeItem",value:function(e,t,i){const a=he(e[t]).filter((e=>String(e)!==i));if(a.length)return{...e,[t]:a};const o={...e};return delete o[t],Object.keys(o).length?o:void 0}},{kind:"method",key:"_deviceMeetsFilter",value:function(e){var t;const i=null===(t=this._entities)||void 0===t?void 0:t.filter((t=>t.device_id===e.id));if(this.includeDomains){if(!i||!i.length)return!1;if(!i.some((e=>this.includeDomains.includes(j(e.entity_id)))))return!1}if(this.includeDeviceClasses){if(!i||!i.length)return!1;if(!i.some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&this.includeDeviceClasses.includes(t.attributes.device_class))})))return!1}return!this.deviceFilter||this.deviceFilter(e)}},{kind:"method",key:"_entityRegMeetsFilter",value:function(e){if(e.entity_category)return!1;if(this.includeDomains&&!this.includeDomains.includes(j(e.entity_id)))return!1;if(this.includeDeviceClasses){const t=this.hass.states[e.entity_id];if(!t)return!1;if(!t.attributes.device_class||!this.includeDeviceClasses.includes(t.attributes.device_class))return!1}return!this.entityRegFilter||this.entityRegFilter(e)}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ${F(Ce)}
      .mdc-chip {
        color: var(--primary-text-color);
      }
      .items {
        z-index: 2;
      }
      .mdc-chip-set {
        padding: 4px 0;
      }
      .mdc-chip.add {
        color: rgba(0, 0, 0, 0.87);
      }
      .mdc-chip:not(.add) {
        cursor: default;
      }
      .mdc-chip ha-icon-button {
        --mdc-icon-button-size: 24px;
        display: flex;
        align-items: center;
        outline: none;
      }
      .mdc-chip ha-icon-button ha-svg-icon {
        border-radius: 50%;
        background: var(--secondary-text-color);
      }
      .mdc-chip__icon.mdc-chip__icon--trailing {
        width: 16px;
        height: 16px;
        --mdc-icon-size: 14px;
        color: var(--secondary-text-color);
      }
      .mdc-chip__icon--leading {
        display: flex;
        align-items: center;
        justify-content: center;
        --mdc-icon-size: 20px;
        border-radius: 50%;
        padding: 6px;
        margin-left: -14px !important;
      }
      .expand-btn {
        margin-right: 0;
      }
      .mdc-chip.area_id:not(.add) {
        border: 2px solid #fed6a4;
        background: var(--card-background-color);
      }
      .mdc-chip.area_id:not(.add) .mdc-chip__icon--leading,
      .mdc-chip.area_id.add {
        background: #fed6a4;
      }
      .mdc-chip.device_id:not(.add) {
        border: 2px solid #a8e1fb;
        background: var(--card-background-color);
      }
      .mdc-chip.device_id:not(.add) .mdc-chip__icon--leading,
      .mdc-chip.device_id.add {
        background: #a8e1fb;
      }
      .mdc-chip.entity_id:not(.add) {
        border: 2px solid #d2e7b9;
        background: var(--card-background-color);
      }
      .mdc-chip.entity_id:not(.add) .mdc-chip__icon--leading,
      .mdc-chip.entity_id.add {
        background: #d2e7b9;
      }
      .mdc-chip:hover {
        z-index: 5;
      }
      paper-tooltip.expand {
        min-width: 200px;
      }
      :host([disabled]) .mdc-chip {
        opacity: var(--light-disabled-opacity);
        pointer-events: none;
      }
    `}}]}}),we(t)),e([n("ha-selector-target")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[r()],key:"_entityPlaformLookup",value:void 0},{kind:"field",decorators:[r()],key:"_configEntries",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"method",key:"hassSubscribe",value:function(){return[O(this.hass.connection,(e=>{const t={};for(const i of e)i.platform&&(t[i.entity_id]=i.platform);this._entityPlaformLookup=t}))]}},{kind:"method",key:"updated",value:function(e){if(e.has("selector")){var t,i;e.get("selector")!==this.selector&&(null!==(t=this.selector.target.device)&&void 0!==t&&t.integration||null!==(i=this.selector.target.entity)&&void 0!==i&&i.integration)&&this._loadConfigEntries()}}},{kind:"method",key:"render",value:function(){var e,t;return a`<ha-target-picker
      .hass=${this.hass}
      .value=${this.value}
      .helper=${this.helper}
      .deviceFilter=${this._filterDevices}
      .entityRegFilter=${this._filterRegEntities}
      .entityFilter=${this._filterEntities}
      .includeDeviceClasses=${null!==(e=this.selector.target.entity)&&void 0!==e&&e.device_class?[this.selector.target.entity.device_class]:void 0}
      .includeDomains=${null!==(t=this.selector.target.entity)&&void 0!==t&&t.domain?[this.selector.target.entity.domain]:void 0}
      .disabled=${this.disabled}
    ></ha-target-picker>`}},{kind:"field",key:"_filterEntities",value(){return e=>{var t,i,a,o;if((null!==(t=this.selector.target.entity)&&void 0!==t&&t.integration||null!==(i=this.selector.target.device)&&void 0!==i&&i.integration)&&(!this._entityPlaformLookup||this._entityPlaformLookup[e.entity_id]!==((null===(a=this.selector.target.entity)||void 0===a?void 0:a.integration)||(null===(o=this.selector.target.device)||void 0===o?void 0:o.integration))))return!1;return!0}}},{kind:"field",key:"_filterRegEntities",value(){return e=>{var t;return null===(t=this.selector.target.entity)||void 0===t||!t.integration||e.platform===this.selector.target.entity.integration}}},{kind:"field",key:"_filterDevices",value(){return e=>{var t,i,a,o,n;if(null!==(t=this.selector.target.device)&&void 0!==t&&t.manufacturer&&e.manufacturer!==this.selector.target.device.manufacturer)return!1;if(null!==(i=this.selector.target.device)&&void 0!==i&&i.model&&e.model!==this.selector.target.device.model)return!1;if((null!==(a=this.selector.target.device)&&void 0!==a&&a.integration||null!==(o=this.selector.target.entity)&&void 0!==o&&o.integration)&&(null===(n=this._configEntries)||void 0===n||!n.some((t=>e.config_entries.includes(t.entry_id)))))return!1;return!0}}},{kind:"method",key:"_loadConfigEntries",value:async function(){this._configEntries=(await xe(this.hass)).filter((e=>{var t,i;return e.domain===(null===(t=this.selector.target.device)||void 0===t?void 0:t.integration)||e.domain===(null===(i=this.selector.target.entity)||void 0===i?void 0:i.integration)}))}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-target-picker {
        display: block;
      }
    `}}]}}),we(t)),e([n("ha-selector-text")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"placeholder",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[r()],key:"_unmaskedPassword",value:()=>!1},{kind:"method",key:"render",value:function(){var e,t,i,o,n;return null!==(e=this.selector.text)&&void 0!==e&&e.multiline?a`<ha-textarea
        .label=${this.label}
        .placeholder=${this.placeholder}
        .value=${this.value||""}
        .helper=${this.helper}
        helperPersistent
        .disabled=${this.disabled}
        @input=${this._handleChange}
        autocapitalize="none"
        autocomplete="off"
        spellcheck="false"
        .required=${this.required}
        autogrow
      ></ha-textarea>`:a`<ha-textfield
        .value=${this.value||""}
        .placeholder=${this.placeholder||""}
        .helper=${this.helper}
        helperPersistent
        .disabled=${this.disabled}
        .type=${this._unmaskedPassword?"text":null===(t=this.selector.text)||void 0===t?void 0:t.type}
        @input=${this._handleChange}
        .label=${this.label||""}
        .suffix=${"password"===(null===(i=this.selector.text)||void 0===i?void 0:i.type)?a`<div style="width: 24px"></div>`:null===(o=this.selector.text)||void 0===o?void 0:o.suffix}
        .required=${this.required}
      ></ha-textfield>
      ${"password"===(null===(n=this.selector.text)||void 0===n?void 0:n.type)?a`<ha-icon-button
            toggles
            .label=${(this._unmaskedPassword?"Hide":"Show")+" password"}
            @click=${this._toggleUnmaskedPassword}
            .path=${this._unmaskedPassword?A:D}
          ></ha-icon-button>`:""}`}},{kind:"method",key:"_toggleUnmaskedPassword",value:function(){this._unmaskedPassword=!this._unmaskedPassword}},{kind:"method",key:"_handleChange",value:function(e){let t=e.target.value;this.value!==t&&(""!==t||this.required||(t=void 0),o(this,"value-changed",{value:t}))}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: block;
        position: relative;
      }
      ha-textarea,
      ha-textfield {
        width: 100%;
      }
      ha-icon-button {
        position: absolute;
        top: 16px;
        right: 16px;
        --mdc-icon-button-size: 24px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
      }
    `}}]}}),t),e([n("ha-selector-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <ha-time-input
        .value=${this.value}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .required=${this.required}
        .helper=${this.helper}
        .label=${this.label}
        enable-second
      ></ha-time-input>
    `}}]}}),t),e([n("ha-selector-icon")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`
      <ha-icon-picker
        .label=${this.label}
        .value=${this.value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .fallbackPath=${this.selector.icon.fallbackPath}
        .placeholder=${this.selector.icon.placeholder}
        @value-changed=${this._valueChanged}
      ></ha-icon-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(e){o(this,"value-changed",{value:e.detail.value})}}]}}),t),e([n("ha-selector-theme")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return a`
      <ha-theme-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-theme-picker>
    `}}]}}),t),e([n("ha-locations-editor")],(function(e,t){class n extends t{constructor(){super(),e(this),import("./c.3b41e231.js").then((e=>{import("./c.5700eccf.js").then((()=>{this.Leaflet=e.default,this._updateMarkers(),this.updateComplete.then((()=>this.fitMap()))}))}))}}return{F:n,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"locations",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"autoFit",value:()=>!1},{kind:"field",decorators:[i({type:Number})],key:"zoom",value:()=>16},{kind:"field",decorators:[i({type:Boolean})],key:"darkMode",value:void 0},{kind:"field",decorators:[r()],key:"_locationMarkers",value:void 0},{kind:"field",decorators:[r()],key:"_circles",value:()=>({})},{kind:"field",decorators:[k("ha-map",!0)],key:"map",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"method",key:"fitMap",value:function(){this.map.fitMap()}},{kind:"method",key:"fitMarker",value:function(e){if(!this.map.leafletMap||!this._locationMarkers)return;const t=this._locationMarkers[e];if(t)if("getBounds"in t)this.map.leafletMap.fitBounds(t.getBounds()),t.bringToFront();else{const i=this._circles[e];i?this.map.leafletMap.fitBounds(i.getBounds()):this.map.leafletMap.setView(t.getLatLng(),this.zoom)}}},{kind:"method",key:"render",value:function(){return a`
      <ha-map
        .hass=${this.hass}
        .layers=${this._getLayers(this._circles,this._locationMarkers)}
        .zoom=${this.zoom}
        .autoFit=${this.autoFit}
        .darkMode=${this.darkMode}
      ></ha-map>
      ${this.helper?a`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}
    `}},{kind:"field",key:"_getLayers",value:()=>v(((e,t)=>{const i=[];return Array.prototype.push.apply(i,Object.values(e)),t&&Array.prototype.push.apply(i,Object.values(t)),i}))},{kind:"method",key:"willUpdate",value:function(e){u(h(n.prototype),"willUpdate",this).call(this,e),this.Leaflet&&e.has("locations")&&this._updateMarkers()}},{kind:"method",key:"_updateLocation",value:function(e){const t=e.target,i=t.getLatLng();let a=i.lng;Math.abs(a)>180&&(a=(a%360+540)%360-180);const n=[i.lat,a];o(this,"location-updated",{id:t.id,location:n},{bubbles:!1})}},{kind:"method",key:"_updateRadius",value:function(e){const t=e.target,i=this._locationMarkers[t.id];o(this,"radius-updated",{id:t.id,radius:i.getRadius()},{bubbles:!1})}},{kind:"method",key:"_markerClicked",value:function(e){const t=e.target;o(this,"marker-clicked",{id:t.id},{bubbles:!1})}},{kind:"method",key:"_updateMarkers",value:function(){if(!this.locations||!this.locations.length)return this._circles={},void(this._locationMarkers=void 0);const e={},t={},i=getComputedStyle(this).getPropertyValue("--accent-color");this.locations.forEach((a=>{let o;if(a.icon){const e=document.createElement("div");e.className="named-icon",a.name&&(e.innerText=a.name);const t=document.createElement("ha-icon");t.setAttribute("icon",a.icon),e.prepend(t),o=this.Leaflet.divIcon({html:e.outerHTML,iconSize:[24,24],className:"light"})}if(a.radius){const n=this.Leaflet.circle([a.latitude,a.longitude],{color:a.radius_color||i,radius:a.radius});a.radius_editable||a.location_editable?(n.editing.enable(),n.addEventListener("add",(()=>{const e=n.editing._moveMarker,t=n.editing._resizeMarkers[0];o&&e.setIcon(o),t.id=e.id=a.id,e.addEventListener("dragend",(e=>this._updateLocation(e))).addEventListener("click",(e=>this._markerClicked(e))),a.radius_editable?t.addEventListener("dragend",(e=>this._updateRadius(e))):t.remove()})),e[a.id]=n):t[a.id]=n}if(!a.radius||!a.radius_editable&&!a.location_editable){const t={title:a.name,draggable:a.location_editable};o&&(t.icon=o);const i=this.Leaflet.marker([a.latitude,a.longitude],t).addEventListener("dragend",(e=>this._updateLocation(e))).addEventListener("click",(e=>this._markerClicked(e)));i.id=a.id,e[a.id]=i}})),this._circles=t,this._locationMarkers=e,o(this,"markers-updated")}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-map {
        display: block;
        height: 300px;
      }
    `}}]}}),t),e([n("ha-selector-location")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <ha-locations-editor
        class="flex"
        .hass=${this.hass}
        .helper=${this.helper}
        .locations=${this._location(this.selector,this.value)}
        @location-updated=${this._locationChanged}
        @radius-updated=${this._radiusChanged}
      ></ha-locations-editor>
    `}},{kind:"field",key:"_location",value(){return v(((e,t)=>{const i=getComputedStyle(this),a=e.location.radius?i.getPropertyValue("--zone-radius-color")||i.getPropertyValue("--accent-color"):void 0;return[{id:"location",latitude:(null==t?void 0:t.latitude)||this.hass.config.latitude,longitude:(null==t?void 0:t.longitude)||this.hass.config.longitude,radius:e.location.radius?(null==t?void 0:t.radius)||1e3:void 0,radius_color:a,icon:e.location.icon||e.location.radius?"mdi:map-marker-radius":"mdi:map-marker",location_editable:!0,radius_editable:!0}]}))}},{kind:"method",key:"_locationChanged",value:function(e){const[t,i]=e.detail.location;o(this,"value-changed",{value:{...this.value,latitude:t,longitude:i}})}},{kind:"method",key:"_radiusChanged",value:function(e){const t=e.detail.radius;o(this,"value-changed",{value:{...this.value,radius:t}})}}]}}),t),e([n("ha-selector-color_temp")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){var e,t;return a`
      <ha-labeled-slider
        pin
        icon="hass:thermometer"
        .caption=${this.label}
        .min=${null!==(e=this.selector.color_temp.min_mireds)&&void 0!==e?e:153}
        .max=${null!==(t=this.selector.color_temp.max_mireds)&&void 0!==t?t:500}
        .value=${this.value}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .required=${this.required}
        @change=${this._valueChanged}
      ></ha-labeled-slider>
    `}},{kind:"method",key:"_valueChanged",value:function(e){o(this,"value-changed",{value:Number(e.target.value)})}},{kind:"field",static:!0,key:"styles",value:()=>l`
    ha-labeled-slider {
      --ha-slider-background: -webkit-linear-gradient(
        right,
        rgb(255, 160, 0) 0%,
        white 50%,
        rgb(166, 209, 255) 100%
      );
      /* The color temp minimum value shouldn't be rendered differently. It's not "off". */
      --paper-slider-knob-start-border-color: var(--primary-color);
    }
  `}]}}),t);let zt=e([n("ha-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i()],key:"placeholder",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[i()],key:"context",value:void 0},{kind:"method",key:"focus",value:function(){var e,t;null===(e=this.shadowRoot)||void 0===e||null===(t=e.getElementById("selector"))||void 0===t||t.focus()}},{kind:"get",key:"_type",value:function(){return Object.keys(this.selector)[0]}},{kind:"method",key:"render",value:function(){return a`
      ${le(`ha-selector-${this._type}`,{hass:this.hass,selector:this.selector,value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,id:"selector"})}
    `}}]}}),t);e([n("ha-settings-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"three-line"})],key:"threeLine",value:()=>!1},{kind:"method",key:"render",value:function(){return a`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <paper-item-body
          ?two-line=${!this.threeLine}
          ?three-line=${this.threeLine}
        >
          <slot name="heading"></slot>
          <div secondary><slot name="description"></slot></div>
        </paper-item-body>
      </div>
      <div class="content"><slot></slot></div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      :host {
        display: flex;
        padding: 0 16px;
        align-content: normal;
        align-self: auto;
        align-items: center;
      }
      paper-item-body {
        padding: 8px 16px 8px 0;
      }
      paper-item-body[two-line] {
        min-height: calc(
          var(--paper-item-body-two-line-min-height, 72px) - 16px
        );
        flex: 1;
      }
      .content {
        display: contents;
      }
      :host(:not([narrow])) .content {
        display: flex;
        justify-content: flex-end;
        flex: 1;
        padding: 16px 0;
      }
      .content ::slotted(*) {
        width: var(--settings-row-content-width);
      }
      :host([narrow]) {
        align-items: normal;
        flex-direction: column;
        border-top: 1px solid var(--divider-color);
        padding-bottom: 8px;
      }
      ::slotted(ha-switch) {
        padding: 16px 0;
      }
      div[secondary] {
        white-space: normal;
      }
      .prefix-wrap {
        display: contents;
      }
      :host([narrow]) .prefix-wrap {
        display: flex;
        align-items: center;
      }
    `}}]}}),t);const Pt=e=>e.selector&&!e.required&&!("boolean"in e.selector&&e.default);e([n("ha-service-control")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[r()],key:"_value",value:void 0},{kind:"field",decorators:[i({reflect:!0,type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"showAdvanced",value:void 0},{kind:"field",decorators:[r()],key:"_checkedKeys",value:()=>new Set},{kind:"field",decorators:[r()],key:"_manifest",value:void 0},{kind:"field",decorators:[k("ha-yaml-editor")],key:"_yamlEditor",value:void 0},{kind:"method",key:"willUpdate",value:function(e){var t,i,a,n,s,d,l,r,c,u,h;if(!e.has("value"))return;const v=e.get("value");(null==v?void 0:v.service)!==(null===(t=this.value)||void 0===t?void 0:t.service)&&(this._checkedKeys=new Set);const k=this._getServiceInfo(null===(i=this.value)||void 0===i?void 0:i.service,this.hass.services);var p;null!==(a=this.value)&&void 0!==a&&a.service?null!=v&&v.service&&j(this.value.service)===j(v.service)||this._fetchManifest(j(null===(p=this.value)||void 0===p?void 0:p.service)):this._manifest=void 0;if(k&&"target"in k&&(null!==(n=this.value)&&void 0!==n&&null!==(s=n.data)&&void 0!==s&&s.entity_id||null!==(d=this.value)&&void 0!==d&&null!==(l=d.data)&&void 0!==l&&l.area_id||null!==(r=this.value)&&void 0!==r&&null!==(c=r.data)&&void 0!==c&&c.device_id)){var m,g,y;const e={...this.value.target};!this.value.data.entity_id||null!==(m=this.value.target)&&void 0!==m&&m.entity_id||(e.entity_id=this.value.data.entity_id),!this.value.data.area_id||null!==(g=this.value.target)&&void 0!==g&&g.area_id||(e.area_id=this.value.data.area_id),!this.value.data.device_id||null!==(y=this.value.target)&&void 0!==y&&y.device_id||(e.device_id=this.value.data.device_id),this._value={...this.value,target:e,data:{...this.value.data}},delete this._value.data.entity_id,delete this._value.data.device_id,delete this._value.data.area_id}else this._value=this.value;if((null==v?void 0:v.service)!==(null===(u=this.value)||void 0===u?void 0:u.service)){let e=!1;this._value&&k&&(this._value.data||(this._value.data={}),k.fields.forEach((t=>{t.selector&&t.required&&void 0===t.default&&"boolean"in t.selector&&void 0===this._value.data[t.key]&&(e=!0,this._value.data[t.key]=!1)}))),e&&o(this,"value-changed",{value:{...this._value}})}if(null!==(h=this._value)&&void 0!==h&&h.data){const e=this._yamlEditor;e&&e.value!==this._value.data&&e.setValue(this._value.data)}}},{kind:"field",key:"_getServiceInfo",value:()=>v(((e,t)=>{if(!e||!t)return;const i=j(e),a=N(e);if(!(i in t))return;if(!(a in t[i]))return;const o=Object.entries(t[i][a].fields).map((([e,t])=>({key:e,...t,selector:t.selector})));return{...t[i][a],fields:o,hasSelector:o.length?o.filter((e=>e.selector)).map((e=>e.key)):[]}}))},{kind:"method",key:"render",value:function(){var e,t,i,o,n,s,d;const l=this._getServiceInfo(null===(e=this._value)||void 0===e?void 0:e.service,this.hass.services),r=(null==l?void 0:l.fields.length)&&!l.hasSelector.length||l&&Object.keys((null===(t=this._value)||void 0===t?void 0:t.data)||{}).some((e=>!l.hasSelector.includes(e))),c=r&&(null==l?void 0:l.fields.find((e=>"entity_id"===e.key))),u=Boolean(!r&&(null==l?void 0:l.fields.some((e=>Pt(e)))));return a`<ha-service-picker
        .hass=${this.hass}
        .value=${null===(i=this._value)||void 0===i?void 0:i.service}
        @value-changed=${this._serviceChanged}
      ></ha-service-picker>
      <div class="description">
        <p>${null==l?void 0:l.description}</p>
        ${this._manifest?a` <a
              href=${this._manifest.is_built_in?de(this.hass,`/integrations/${this._manifest.domain}`):this._manifest.documentation}
              title=${this.hass.localize("ui.components.service-control.integration_doc")}
              target="_blank"
              rel="noreferrer"
            >
              <ha-icon-button
                .path=${q}
                class="help-icon"
              ></ha-icon-button>
            </a>`:""}
      </div>
      ${l&&"target"in l?a`<ha-settings-row .narrow=${this.narrow}>
            ${u?a`<div slot="prefix" class="checkbox-spacer"></div>`:""}
            <span slot="heading"
              >${this.hass.localize("ui.components.service-control.target")}</span
            >
            <span slot="description"
              >${this.hass.localize("ui.components.service-control.target_description")}</span
            ><ha-selector
              .hass=${this.hass}
              .selector=${l.target?{target:l.target}:{target:{}}}
              @value-changed=${this._targetChanged}
              .value=${null===(o=this._value)||void 0===o?void 0:o.target}
            ></ha-selector
          ></ha-settings-row>`:c?a`<ha-entity-picker
            .hass=${this.hass}
            .value=${null===(n=this._value)||void 0===n||null===(s=n.data)||void 0===s?void 0:s.entity_id}
            .label=${c.description}
            @value-changed=${this._entityPicked}
            allow-custom-entity
          ></ha-entity-picker>`:""}
      ${r?a`<ha-yaml-editor
            .hass=${this.hass}
            .label=${this.hass.localize("ui.components.service-control.service_data")}
            .name=${"data"}
            .defaultValue=${null===(d=this._value)||void 0===d?void 0:d.data}
            @value-changed=${this._dataChanged}
          ></ha-yaml-editor>`:null==l?void 0:l.fields.map((e=>{var t,i,o,n;const s=Pt(e);return e.selector&&(!e.advanced||this.showAdvanced||null!==(t=this._value)&&void 0!==t&&t.data&&void 0!==this._value.data[e.key])?a`<ha-settings-row .narrow=${this.narrow}>
                  ${s?a`<ha-checkbox
                        .key=${e.key}
                        .checked=${this._checkedKeys.has(e.key)||(null===(i=this._value)||void 0===i?void 0:i.data)&&void 0!==this._value.data[e.key]}
                        @change=${this._checkboxChanged}
                        slot="prefix"
                      ></ha-checkbox>`:u?a`<div slot="prefix" class="checkbox-spacer"></div>`:""}
                  <span slot="heading">${e.name||e.key}</span>
                  <span slot="description">${null==e?void 0:e.description}</span>
                  <ha-selector
                    .disabled=${s&&!this._checkedKeys.has(e.key)&&(!(null!==(o=this._value)&&void 0!==o&&o.data)||void 0===this._value.data[e.key])}
                    .hass=${this.hass}
                    .selector=${e.selector}
                    .key=${e.key}
                    @value-changed=${this._serviceDataChanged}
                    .value=${null!==(n=this._value)&&void 0!==n&&n.data&&void 0!==this._value.data[e.key]?this._value.data[e.key]:e.default}
                  ></ha-selector>
                </ha-settings-row>`:""}))}`}},{kind:"method",key:"_checkboxChanged",value:function(e){const t=e.currentTarget.checked,i=e.currentTarget.key;let a;if(t){var n,s,d;this._checkedKeys.add(i);const e=null===(n=this._getServiceInfo(null===(d=this._value)||void 0===d?void 0:d.service,this.hass.services))||void 0===n||null===(s=n.fields.find((e=>e.key===i)))||void 0===s?void 0:s.default;var l;if(e)a={...null===(l=this._value)||void 0===l?void 0:l.data,[i]:e}}else{var r;this._checkedKeys.delete(i),a={...null===(r=this._value)||void 0===r?void 0:r.data},delete a[i]}a&&o(this,"value-changed",{value:{...this._value,data:a}}),this.requestUpdate("_checkedKeys")}},{kind:"method",key:"_serviceChanged",value:function(e){var t;e.stopPropagation(),e.detail.value!==(null===(t=this._value)||void 0===t?void 0:t.service)&&o(this,"value-changed",{value:{service:e.detail.value||""}})}},{kind:"method",key:"_entityPicked",value:function(e){var t,i,a;e.stopPropagation();const n=e.detail.value;if((null===(t=this._value)||void 0===t||null===(i=t.data)||void 0===i?void 0:i.entity_id)===n)return;let s;var d;!n&&null!==(a=this._value)&&void 0!==a&&a.data?(s={...this._value},delete s.data.entity_id):s={...this._value,data:{...null===(d=this._value)||void 0===d?void 0:d.data,entity_id:e.detail.value}};o(this,"value-changed",{value:s})}},{kind:"method",key:"_targetChanged",value:function(e){var t;e.stopPropagation();const i=e.detail.value;if((null===(t=this._value)||void 0===t?void 0:t.target)===i)return;let a;i?a={...this._value,target:e.detail.value}:(a={...this._value},delete a.target),o(this,"value-changed",{value:a})}},{kind:"method",key:"_serviceDataChanged",value:function(e){var t,i,a,n,s;e.stopPropagation();const d=e.currentTarget.key,l=e.detail.value;if((null===(t=this._value)||void 0===t||null===(i=t.data)||void 0===i?void 0:i[d])===l||(null===(a=this._value)||void 0===a||null===(n=a.data)||void 0===n||!n[d])&&(""===l||void 0===l))return;const r={...null===(s=this._value)||void 0===s?void 0:s.data,[d]:l};""!==l&&void 0!==l||delete r[d],o(this,"value-changed",{value:{...this._value,data:r}})}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&o(this,"value-changed",{value:{...this._value,data:e.detail.value}})}},{kind:"method",key:"_fetchManifest",value:async function(e){this._manifest=void 0;try{this._manifest=await se(this.hass,e)}catch(e){}}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-settings-row {
        padding: var(--service-control-padding, 0 16px);
      }
      ha-settings-row {
        --paper-time-input-justify-content: flex-end;
        --settings-row-content-width: 100%;
        border-top: var(
          --service-control-items-border-top,
          1px solid var(--divider-color)
        );
      }
      ha-service-picker,
      ha-entity-picker,
      ha-yaml-editor {
        display: block;
        margin: var(--service-control-padding, 0 16px);
      }
      ha-yaml-editor {
        padding: 16px 0;
      }
      p {
        margin: var(--service-control-padding, 0 16px);
        padding: 16px 0;
      }
      .checkbox-spacer {
        width: 32px;
      }
      ha-checkbox {
        margin-left: -16px;
      }
      .help-icon {
        color: var(--secondary-text-color);
      }
      .description {
        justify-content: space-between;
        display: flex;
        align-items: center;
        padding-right: 2px;
      }
    `}}]}}),t);export{zt as HaSelector};
