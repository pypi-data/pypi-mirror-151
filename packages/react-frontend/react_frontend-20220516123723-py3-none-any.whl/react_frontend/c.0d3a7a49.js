import{ar as e,_ as t,s as i,e as s,$ as a,f as o,n,g as r,i as l,t as d,eI as h,dl as c,dk as p,cp as f,cq as u,m,aA as g,d as v,eb as _,cD as y,dF as k}from"./main-ac83c92b.js";import{k as w,i as b,b as $}from"./c.027db416.js";import"./c.8cbd7110.js";import{c as x,u as C,s as F,a as z}from"./c.39da0aeb.js";import{l as D,f as P}from"./c.4b4b8ba2.js";import{aq as S,ap as j,d as E,af as I}from"./c.3e14cfd3.js";import{d as A}from"./c.57c0073c.js";import"./c.4860f91b.js";import"./c.1fca9ca6.js";import"./c.f731f3b4.js";import"./c.0225555d.js";import{b as H}from"./c.3eb3ee48.js";import{F as M}from"./c.f5888e17.js";import"./c.0660f3f3.js";import{c as U}from"./c.cfa85e17.js";import{g as R}from"./c.40d6516d.js";import"./c.4e93087d.js";import"./c.5b2e0d05.js";import"./c.02ed471c.js";import"./c.8eddd911.js";import"./c.0e001851.js";import"./c.c8193d47.js";import"./c.47fa9be3.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import"./c.5ea5eadd.js";import"./c.d2605417.js";const T=e`
  h2 {
    margin: 24px 38px 0 0;
    padding: 0 24px;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    font-family: var(
      --mdc-typography-headline6-font-family,
      var(--mdc-typography-font-family, Roboto, sans-serif)
    );
    font-size: var(--mdc-typography-headline6-font-size, 1.25rem);
    line-height: var(--mdc-typography-headline6-line-height, 2rem);
    font-weight: var(--mdc-typography-headline6-font-weight, 500);
    letter-spacing: var(--mdc-typography-headline6-letter-spacing, 0.0125em);
    text-decoration: var(--mdc-typography-headline6-text-decoration, inherit);
    text-transform: var(--mdc-typography-headline6-text-transform, inherit);
    box-sizing: border-box;
  }

  .content {
    margin-top: 20px;
    padding: 0 24px;
  }

  .buttons {
    position: relative;
    padding: 8px 16px 8px 24px;
    margin: 8px 0 0;
    color: var(--primary-color);
    display: flex;
    justify-content: flex-end;
  }

  ha-markdown {
    overflow-wrap: break-word;
  }
  ha-markdown a {
    color: var(--primary-color);
  }
  ha-markdown img:first-child:last-child {
    display: block;
    margin: 0 auto;
  }
`;t([n("step-flow-abort")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){return a`
      <h2>
        ${this.hass.localize("ui.panel.config.integrations.config_flow.aborted")}
      </h2>
      <div class="content">
        ${this.flowConfig.renderAbortDescription(this.hass,this.step)}
      </div>
      <div class="buttons">
        <mwc-button @click=${this._flowDone}
          >${this.hass.localize("ui.panel.config.integrations.config_flow.close")}</mwc-button
        >
      </div>
    `}},{kind:"method",key:"_flowDone",value:function(){o(this,"flow-update",{step:void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return T}}]}}),i),t([n("step-flow-create-entry")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"devices",value:void 0},{kind:"method",key:"render",value:function(){var e;const t=this.hass.localize;return a`
      <h2>Success!</h2>
      <div class="content">
        ${this.flowConfig.renderCreateEntryDescription(this.hass,this.step)}
        ${"not_loaded"===(null===(e=this.step.result)||void 0===e?void 0:e.state)?a`<span class="error"
              >${t("ui.panel.config.integrations.config_flow.not_loaded")}</span
            >`:""}
        ${0===this.devices.length?"":a`
              <p>We found the following devices:</p>
              <div class="devices">
                ${this.devices.map((e=>a`
                      <div class="device">
                        <div>
                          <b>${x(e,this.hass)}</b><br />
                          ${e.model} (${e.manufacturer})
                        </div>
                        <ha-area-picker
                          .hass=${this.hass}
                          .device=${e.id}
                          @value-changed=${this._areaPicked}
                        ></ha-area-picker>
                      </div>
                    `))}
              </div>
            `}
      </div>
      <div class="buttons">
        <mwc-button @click=${this._flowDone}
          >${t("ui.panel.config.integrations.config_flow.finish")}</mwc-button
        >
      </div>
    `}},{kind:"method",key:"_flowDone",value:function(){o(this,"flow-update",{step:void 0})}},{kind:"method",key:"_areaPicked",value:async function(e){const t=e.currentTarget,i=t.device,s=e.detail.value;try{await C(this.hass,i,{area_id:s})}catch(e){w(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_area","error",e.message)}),t.value=null}}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        .devices {
          display: flex;
          flex-wrap: wrap;
          margin: -4px;
          max-height: 600px;
          overflow-y: auto;
        }
        .device {
          border: 1px solid var(--divider-color);
          padding: 5px;
          border-radius: 4px;
          margin: 4px;
          display: inline-block;
          width: 250px;
        }
        .buttons > *:last-child {
          margin-left: auto;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .device {
            width: 100%;
          }
        }
        .error {
          color: var(--error-color);
        }
      `]}}]}}),i),t([n("step-flow-external")],(function(t,i){class o extends i{constructor(...e){super(...e),t(this)}}return{F:o,d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.hass.localize;return a`
      <h2>${this.flowConfig.renderExternalStepHeader(this.hass,this.step)}</h2>
      <div class="content">
        ${this.flowConfig.renderExternalStepDescription(this.hass,this.step)}
        <div class="open-button">
          <a href=${this.step.url} target="_blank" rel="noreferrer">
            <mwc-button raised>
              ${e("ui.panel.config.integrations.config_flow.external_step.open_site")}
            </mwc-button>
          </a>
        </div>
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){r(l(o.prototype),"firstUpdated",this).call(this,e),window.open(this.step.url)}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        .open-button {
          text-align: center;
          padding: 24px 0;
        }
        .open-button a {
          text-decoration: none;
        }
      `]}}]}}),i);t([n("step-flow-form")],(function(t,i){class n extends i{constructor(...e){super(...e),t(this)}}return{F:n,d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"_loading",value:()=>!1},{kind:"field",decorators:[d()],key:"_stepData",value:void 0},{kind:"field",decorators:[d()],key:"_errorMsg",value:void 0},{kind:"method",key:"render",value:function(){const e=this.step,t=this._stepDataProcessed;return a`
      <h2>${this.flowConfig.renderShowFormStepHeader(this.hass,this.step)}</h2>
      <div class="content">
        ${this.flowConfig.renderShowFormStepDescription(this.hass,this.step)}
        ${this._errorMsg?a`<ha-alert alert-type="error">${this._errorMsg}</ha-alert>`:""}
        <ha-form
          .hass=${this.hass}
          .data=${t}
          .disabled=${this._loading}
          @value-changed=${this._stepDataChanged}
          .schema=${e.data_schema}
          .error=${e.errors}
          .computeLabel=${this._labelCallback}
          .computeHelper=${this._helperCallback}
          .computeError=${this._errorCallback}
        ></ha-form>
      </div>
      <div class="buttons">
        ${this._loading?a`
              <div class="submit-spinner">
                <ha-circular-progress active></ha-circular-progress>
              </div>
            `:a`
              <div>
                <mwc-button @click=${this._submitStep}>
                  ${this.hass.localize("ui.panel.config.integrations.config_flow."+(!1===this.step.last_step?"next":"submit"))}
                </mwc-button>
              </div>
            `}
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){r(l(n.prototype),"firstUpdated",this).call(this,e),setTimeout((()=>this.shadowRoot.querySelector("ha-form").focus()),0),this.addEventListener("keypress",(e=>{13===e.keyCode&&this._submitStep()}))}},{kind:"get",key:"_stepDataProcessed",value:function(){return void 0!==this._stepData||(this._stepData=(e=>{const t={};return e.forEach((e=>{var i;if(null!==(i=e.description)&&void 0!==i&&i.suggested_value)t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if(e.required)if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type)e.options.length&&(t[e.name]=e.options[0][0]);else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("selector"in e){const i=e.selector;if("device"in i)t[e.name]=i.device.multiple?[]:"";else if("entity"in i)t[e.name]=i.entity.multiple?[]:"";else if("area"in i)t[e.name]=i.area.multiple?[]:"";else if("boolean"in i)t[e.name]=!1;else if("text"in i||"addon"in i||"attribute"in i||"icon"in i||"theme"in i)t[e.name]="";else if("number"in i){var s;t[e.name]=null!==(s=i.number.min)&&void 0!==s?s:0}else if("select"in i)i.select.options.length&&(t[e.name]=i.select.options[0][0]);else if("duration"in i)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in i)t[e.name]="00:00:00";else if("date"in i||"datetime"in i){const i=(new Date).toISOString().slice(0,10);t[e.name]=`${i} 00:00:00`}else if("color_rgb"in i)t[e.name]=[0,0,0];else if("color_temp"in i){var a;t[e.name]=null!==(a=i.color_temp.min_mireds)&&void 0!==a?a:153}else{if(!("action"in i||"media"in i||"target"in i))throw new Error("Selector not supported in initial form data");t[e.name]={}}}})),t})(this.step.data_schema)),this._stepData}},{kind:"method",key:"_submitStep",value:async function(){const e=this._stepData||{};if(!(void 0===e?void 0===this.step.data_schema.find((e=>e.required)):e&&this.step.data_schema.every((t=>!t.required||!["",void 0].includes(e[t.name])))))return void(this._errorMsg=this.hass.localize("ui.panel.config.integrations.config_flow.not_all_required_fields"));this._loading=!0,this._errorMsg=void 0;const t=this.step.flow_id,i={};Object.keys(e).forEach((t=>{const s=e[t];[void 0,""].includes(s)||(i[t]=s)}));try{const e=await this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,i);if(!this.step||t!==this.step.flow_id)return;o(this,"flow-update",{step:e})}catch(e){this._errorMsg=e&&e.body&&e.body.message||"Unknown error occurred"}finally{this._loading=!1}}},{kind:"method",key:"_stepDataChanged",value:function(e){this._stepData=e.detail.value}},{kind:"field",key:"_labelCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldLabel(this.hass,this.step,e)}},{kind:"field",key:"_helperCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldHelper(this.hass,this.step,e)}},{kind:"field",key:"_errorCallback",value(){return e=>this.flowConfig.renderShowFormStepFieldError(this.hass,this.step,e)}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        .error {
          color: red;
        }

        .submit-spinner {
          margin-right: 16px;
        }

        ha-alert,
        ha-form {
          margin-top: 24px;
          display: block;
        }
        h2 {
          word-break: break-word;
          padding-right: 72px;
        }
      `]}}]}}),i),t([n("step-flow-loading")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"loadingReason",value:void 0},{kind:"field",decorators:[s()],key:"handler",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){const e=this.flowConfig.renderLoadingDescription(this.hass,this.loadingReason,this.handler,this.step);return a`
      <div class="init-spinner">
        ${e?a`<div>${e}</div>`:""}
        <ha-circular-progress active></ha-circular-progress>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      .init-spinner {
        padding: 50px 100px;
        text-align: center;
      }
      ha-circular-progress {
        margin-top: 16px;
      }
    `}}]}}),i);customElements.define("ha-icon-next",class extends h{connectedCallback(){super.connectedCallback(),setTimeout((()=>{this.path="ltr"===window.getComputedStyle(this).direction?c:p}),100)}}),t([n("step-flow-menu")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){let e,t;if(Array.isArray(this.step.menu_options)){e=this.step.menu_options,t={};for(const i of e)t[i]=this.flowConfig.renderMenuOption(this.hass,this.step,i)}else e=Object.keys(this.step.menu_options),t=this.step.menu_options;const i=this.flowConfig.renderMenuDescription(this.hass,this.step);return a`
      <h2>${this.flowConfig.renderMenuHeader(this.hass,this.step)}</h2>
      ${i?a`<div class="content">${i}</div>`:""}
      <div class="options">
        ${e.map((e=>a`
            <mwc-list-item hasMeta .step=${e} @click=${this._handleStep}>
              <span>${t[e]}</span>
              <ha-icon-next slot="meta"></ha-icon-next>
            </mwc-list-item>
          `))}
      </div>
    `}},{kind:"method",key:"_handleStep",value:function(e){o(this,"flow-update",{stepPromise:this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,{next_step_id:e.currentTarget.step})})}},{kind:"field",static:!0,key:"styles",value:()=>[T,e`
      .options {
        margin-top: 20px;
        margin-bottom: 8px;
      }
      .content {
        padding-bottom: 16px;
        border-bottom: 1px solid var(--divider-color);
      }
      .content + .options {
        margin-top: 8px;
      }
      mwc-list-item {
        --mdc-list-side-padding: 24px;
      }
    `]}]}}),i);const q=document.createElement("template");q.setAttribute("style","display: none;"),q.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(q.content);const L=[S,j,{hostAttributes:{role:"option",tabindex:"0"}}];f({_template:u`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[L]}),f({_template:u`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[L]}),t([n("step-flow-pick-flow")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"flowsInProgress",value:void 0},{kind:"field",decorators:[s()],key:"handler",value:void 0},{kind:"method",key:"render",value:function(){return a`
      <h2>
        ${this.hass.localize("ui.panel.config.integrations.config_flow.pick_flow_step.title")}
      </h2>

      <div>
        ${this.flowsInProgress.map((e=>{var t;return a` <paper-icon-item
            @click=${this._flowInProgressPicked}
            .flow=${e}
          >
            <img
              slot="item-icon"
              loading="lazy"
              src=${H({domain:e.handler,type:"icon",useFallback:!0,darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode})}
              referrerpolicy="no-referrer"
            />

            <paper-item-body>
              ${D(this.hass.localize,e)}
            </paper-item-body>
            <ha-icon-next></ha-icon-next>
          </paper-icon-item>`}))}
        <paper-item @click=${this._startNewFlowPicked} .handler=${this.handler}>
          <paper-item-body>
            ${this.hass.localize("ui.panel.config.integrations.config_flow.pick_flow_step.new_flow","integration",E(this.hass.localize,this.handler))}
          </paper-item-body>
          <ha-icon-next></ha-icon-next>
        </paper-item>
      </div>
    `}},{kind:"method",key:"_startNewFlowPicked",value:function(e){this._startFlow(e.currentTarget.handler)}},{kind:"method",key:"_startFlow",value:function(e){o(this,"flow-update",{stepPromise:this.flowConfig.createFlow(this.hass,e)})}},{kind:"method",key:"_flowInProgressPicked",value:function(e){const t=e.currentTarget.flow;o(this,"flow-update",{stepPromise:this.flowConfig.fetchFlow(this.hass,t.flow_id)})}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        img {
          width: 40px;
          height: 40px;
        }
        ha-icon-next {
          margin-right: 8px;
        }
        div {
          overflow: auto;
          max-height: 600px;
          margin: 16px 0;
        }
        h2 {
          padding-right: 66px;
        }
        @media all and (max-height: 900px) {
          div {
            max-height: calc(100vh - 134px);
          }
        }
        paper-icon-item,
        paper-item {
          cursor: pointer;
          margin-bottom: 4px;
        }
      `]}}]}}),i);const O=()=>import("./c.1a5d98d0.js");t([n("step-flow-pick-handler")],(function(t,i){class n extends i{constructor(...e){super(...e),t(this)}}return{F:n,d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"handlers",value:void 0},{kind:"field",decorators:[s()],key:"initialFilter",value:void 0},{kind:"field",decorators:[d()],key:"_filter",value:void 0},{kind:"field",key:"_width",value:void 0},{kind:"field",key:"_height",value:void 0},{kind:"field",key:"_filterHandlers",value(){return m(((e,t,i)=>{const s=e.integrations.map((e=>({name:E(this.hass.localize,e),slug:e})));if(t){const i={keys:["name","slug"],isCaseSensitive:!1,minMatchCharLength:2,threshold:.2},a=e.helpers.map((e=>({name:E(this.hass.localize,e),slug:e,is_helper:!0})));return[new M(s,i).search(t).map((e=>e.item)),new M(a,i).search(t).map((e=>e.item))]}return[s.sort(((e,t)=>U(e.name,t.name))),[]]}))}},{kind:"method",key:"render",value:function(){const[e,t]=this._getHandlers(),i=["zha","zwave_js"].filter((e=>b(this.hass,e))).map((e=>({name:this.hass.localize(`ui.panel.config.integrations.add_${e}_device`),slug:e,is_add:!0}))).sort(((e,t)=>U(e.name,t.name)));return a`
      <h2>${this.hass.localize("ui.panel.config.integrations.new")}</h2>
      <search-input
        .hass=${this.hass}
        autofocus
        .filter=${this._filter}
        @value-changed=${this._filterChanged}
        .label=${this.hass.localize("ui.panel.config.integrations.search")}
        @keypress=${this._maybeSubmit}
      ></search-input>
      <mwc-list
        style=${g({width:`${this._width}px`,height:`${this._height}px`})}
      >
        ${i.length?a`
              ${i.map((e=>this._renderRow(e)))}
              <li divider padded class="divider" role="separator"></li>
            `:""}
        ${e.length?e.map((e=>this._renderRow(e))):a`
              <p>
                ${this.hass.localize("ui.panel.config.integrations.note_about_integrations")}<br />
                ${this.hass.localize("ui.panel.config.integrations.note_about_website_reference")}<a
                  href=${A(this.hass,"/integrations/"+(this._filter?`#search/${this._filter}`:""))}
                  target="_blank"
                  rel="noreferrer"
                  >${this.hass.localize("ui.panel.config.integrations.home_assistant_website")}</a
                >.
              </p>
            `}
        ${t.length?a`
              <li divider padded class="divider" role="separator"></li>
              ${t.map((e=>this._renderRow(e)))}
            `:""}
      </mwc-list>
    `}},{kind:"method",key:"_renderRow",value:function(e){var t;return a`
      <mwc-list-item
        graphic="medium"
        .hasMeta=${!e.is_add}
        .handler=${e}
        @click=${this._handlerPicked}
      >
        <img
          slot="graphic"
          loading="lazy"
          src=${H({domain:e.slug,type:"icon",useFallback:!0,darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode})}
          referrerpolicy="no-referrer"
        />
        <span>${e.name} ${e.is_helper?" (helper)":""}</span>
        ${e.is_add?"":a`<ha-icon-next slot="meta"></ha-icon-next>`}
      </mwc-list-item>
    `}},{kind:"method",key:"willUpdate",value:function(e){if(r(l(n.prototype),"willUpdate",this).call(this,e),void 0===this._filter&&void 0!==this.initialFilter&&(this._filter=this.initialFilter),void 0!==this.initialFilter&&""===this._filter)this.initialFilter=void 0,this._filter="",this._width=void 0,this._height=void 0;else if(this.hasUpdated&&e.has("_filter")&&(!this._width||!this._height)){const e=this.shadowRoot.querySelector("mwc-list").getBoundingClientRect();this._width=e.width,this._height=e.height}}},{kind:"method",key:"firstUpdated",value:function(e){r(l(n.prototype),"firstUpdated",this).call(this,e),setTimeout((()=>this.shadowRoot.querySelector("search-input").focus()),0)}},{kind:"method",key:"_getHandlers",value:function(){return this._filterHandlers(this.handlers,this._filter,this.hass.localize)}},{kind:"method",key:"_filterChanged",value:async function(e){this._filter=e.detail.value}},{kind:"method",key:"_handlerPicked",value:async function(e){const t=e.currentTarget.handler;if(t.is_add){if("zwave_js"===t.slug){const e=await R(this.hass,{domain:"zwave_js"});if(!e.length)return;i=this,s={entry_id:e[0].entry_id},o(i,"show-dialog",{dialogTag:"dialog-zwave_js-add-node",dialogImport:O,dialogParams:s})}else"zha"===t.slug&&v("/config/zha/add");o(this,"flow-update")}else{var i,s;if(t.is_helper)return v(`/config/helpers/add?domain=${t.slug}`),void o(this,"flow-update");o(this,"handler-picked",{handler:t.slug})}}},{kind:"method",key:"_maybeSubmit",value:function(e){if("Enter"!==e.key)return;const t=this._getHandlers();t.length>0&&o(this,"handler-picked",{handler:t[0][0].slug})}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        img {
          width: 40px;
          height: 40px;
        }
        search-input {
          display: block;
          margin: 16px 16px 0;
        }
        ha-icon-next {
          margin-right: 8px;
        }
        mwc-list {
          overflow: auto;
          max-height: 600px;
        }
        .divider {
          border-bottom-color: var(--divider-color);
        }
        h2 {
          padding-right: 66px;
        }
        @media all and (max-height: 900px) {
          mwc-list {
            max-height: calc(100vh - 134px);
          }
        }
        p {
          text-align: center;
          padding: 16px;
          margin: 0;
        }
        p > a {
          color: var(--primary-color);
        }
      `]}}]}}),i),t([n("step-flow-progress")],(function(t,i){return{F:class extends i{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[s({attribute:!1})],key:"flowConfig",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s({attribute:!1})],key:"step",value:void 0},{kind:"method",key:"render",value:function(){return a`
      <h2>
        ${this.flowConfig.renderShowFormProgressHeader(this.hass,this.step)}
      </h2>
      <div class="content">
        <ha-circular-progress active></ha-circular-progress>
        ${this.flowConfig.renderShowFormProgressDescription(this.hass,this.step)}
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[T,e`
        .content {
          padding: 50px 100px;
          text-align: center;
        }
        ha-circular-progress {
          margin-bottom: 16px;
        }
      `]}}]}}),i);let N=0;t([n("dialog-data-entry-flow")],(function(t,i){class s extends i{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[d()],key:"_params",value:void 0},{kind:"field",decorators:[d()],key:"_loading",value:void 0},{kind:"field",key:"_instance",value:()=>N},{kind:"field",decorators:[d()],key:"_step",value:void 0},{kind:"field",decorators:[d()],key:"_devices",value:void 0},{kind:"field",decorators:[d()],key:"_areas",value:void 0},{kind:"field",decorators:[d()],key:"_handlers",value:void 0},{kind:"field",decorators:[d()],key:"_handler",value:void 0},{kind:"field",decorators:[d()],key:"_flowsInProgress",value:void 0},{kind:"field",key:"_unsubAreas",value:void 0},{kind:"field",key:"_unsubDevices",value:void 0},{kind:"field",key:"_unsubDataEntryFlowProgressed",value:void 0},{kind:"method",key:"showDialog",value:async function(e){if(this._params=e,this._instance=N++,e.startFlowHandler)this._checkFlowsInProgress(e.startFlowHandler);else{if(e.continueFlowId){this._loading="loading_flow";const t=this._instance;let i;try{i=await e.flowConfig.fetchFlow(this.hass,e.continueFlowId)}catch(e){this.closeDialog();let t=e.message||e.body||"Unknown error";return"string"!=typeof t&&(t=JSON.stringify(t)),void w(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${t}`})}if(t!==this._instance)return;return this._processStep(i),void(this._loading=void 0)}if(!e.flowConfig.getFlowHandlers)throw new Error("No getFlowHandlers defined in flow config");if(this._step=null,void 0===this._handlers){this._loading="loading_handlers";try{this._handlers=await e.flowConfig.getFlowHandlers(this.hass)}finally{this._loading=void 0}}}}},{kind:"method",key:"closeDialog",value:function(){if(!this._params)return;const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));var t;(!this._step||e||this._params.continueFlowId||this._params.flowConfig.deleteFlow(this.hass,this._step.flow_id),this._step&&this._params.dialogClosedCallback)&&this._params.dialogClosedCallback({flowFinished:e,entryId:"result"in this._step?null===(t=this._step.result)||void 0===t?void 0:t.entry_id:void 0});this._loading=void 0,this._step=void 0,this._params=void 0,this._devices=void 0,this._flowsInProgress=void 0,this._handler=void 0,this._unsubAreas&&(this._unsubAreas(),this._unsubAreas=void 0),this._unsubDevices&&(this._unsubDevices(),this._unsubDevices=void 0),this._unsubDataEntryFlowProgressed&&(this._unsubDataEntryFlowProgressed.then((e=>{e()})),this._unsubDataEntryFlowProgressed=void 0),o(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var e,t,i,s,o;return this._params?a`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        hideActions
      >
        <div>
          ${this._loading||null===this._step&&void 0===this._handlers&&void 0===this._handler?a`
                <step-flow-loading
                  .flowConfig=${this._params.flowConfig}
                  .hass=${this.hass}
                  .loadingReason=${this._loading||"loading_handlers"}
                  .handler=${this._handler}
                  .step=${this._step}
                ></step-flow-loading>
              `:void 0===this._step?"":a`
                <div class="dialog-actions">
                  ${["form","menu","external","progress","data_entry_flow_progressed"].includes(null===(e=this._step)||void 0===e?void 0:e.type)&&null!==(t=this._params.manifest)&&void 0!==t&&t.is_built_in||null!==(i=this._params.manifest)&&void 0!==i&&i.documentation?a`
                        <a
                          href=${this._params.manifest.is_built_in?A(this.hass,`/integrations/${this._params.manifest.domain}`):null===(s=this._params)||void 0===s||null===(o=s.manifest)||void 0===o?void 0:o.documentation}
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          <ha-icon-button
                            .label=${this.hass.localize("ui.common.help")}
                            .path=${_}
                            ?rtl=${$(this.hass)}
                          >
                          </ha-icon-button
                        ></a>
                      `:""}
                  <ha-icon-button
                    .label=${this.hass.localize("ui.panel.config.integrations.config_flow.dismiss")}
                    .path=${y}
                    dialogAction="close"
                    ?rtl=${$(this.hass)}
                  ></ha-icon-button>
                </div>
                ${null===this._step?this._handler?a`<step-flow-pick-flow
                        .flowConfig=${this._params.flowConfig}
                        .hass=${this.hass}
                        .handler=${this._handler}
                        .flowsInProgress=${this._flowsInProgress}
                      ></step-flow-pick-flow>`:a`
                        <step-flow-pick-handler
                          .hass=${this.hass}
                          .handlers=${this._handlers}
                          .initialFilter=${this._params.searchQuery}
                          @handler-picked=${this._handlerPicked}
                        ></step-flow-pick-handler>
                      `:"form"===this._step.type?a`
                      <step-flow-form
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                      ></step-flow-form>
                    `:"external"===this._step.type?a`
                      <step-flow-external
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                      ></step-flow-external>
                    `:"abort"===this._step.type?a`
                      <step-flow-abort
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                      ></step-flow-abort>
                    `:"progress"===this._step.type?a`
                      <step-flow-progress
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                      ></step-flow-progress>
                    `:"menu"===this._step.type?a`
                      <step-flow-menu
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                      ></step-flow-menu>
                    `:void 0===this._devices||void 0===this._areas?a`
                      <step-flow-loading
                        .flowConfig=${this._params.flowConfig}
                        .hass=${this.hass}
                        loadingReason="loading_devices_areas"
                      ></step-flow-loading>
                    `:a`
                      <step-flow-create-entry
                        .flowConfig=${this._params.flowConfig}
                        .step=${this._step}
                        .hass=${this.hass}
                        .devices=${this._devices}
                        .areas=${this._areas}
                      ></step-flow-create-entry>
                    `}
              `}
        </div>
      </ha-dialog>
    `:a``}},{kind:"method",key:"firstUpdated",value:function(e){r(l(s.prototype),"firstUpdated",this).call(this,e),this.addEventListener("flow-update",(e=>{const{step:t,stepPromise:i}=e.detail;this._processStep(t||i)}))}},{kind:"method",key:"willUpdate",value:function(e){r(l(s.prototype),"willUpdate",this).call(this,e),e.has("_step")&&this._step&&(["external","progress"].includes(this._step.type)&&this._subscribeDataEntryFlowProgressed(),"create_entry"===this._step.type&&(this._step.result&&this._params.flowConfig.loadDevicesAndAreas?(this._fetchDevices(this._step.result.entry_id),this._fetchAreas()):(this._devices=[],this._areas=[])))}},{kind:"method",key:"_fetchDevices",value:async function(e){this._unsubDevices=F(this.hass.connection,(t=>{this._devices=t.filter((t=>t.config_entries.includes(e)))}))}},{kind:"method",key:"_fetchAreas",value:async function(){this._unsubAreas=z(this.hass.connection,(e=>{this._areas=e}))}},{kind:"method",key:"_checkFlowsInProgress",value:async function(e){this._loading="loading_handlers",this._handler=e;const t=(await P(this.hass.connection)).filter((t=>t.handler===e));if(t.length)this._step=null,this._flowsInProgress=t;else{let t;this._loading="loading_flow";try{t=await this._params.flowConfig.createFlow(this.hass,e)}catch(e){var i;this.closeDialog();const t=404===(null==e?void 0:e.status_code)?this.hass.localize("ui.panel.config.integrations.config_flow.no_config_flow"):`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${(null==e||null===(i=e.body)||void 0===i?void 0:i.message)||(null==e?void 0:e.message)}`;return void w(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:t})}finally{this._handler=void 0}if(this._processStep(t),void 0===this._params.manifest)try{var s;this._params.manifest=await I(this.hass,(null===(s=this._params)||void 0===s?void 0:s.domain)||t.handler)}catch(e){this._params.manifest=null}}this._loading=void 0}},{kind:"method",key:"_handlerPicked",value:function(e){this._checkFlowsInProgress(e.detail.handler)}},{kind:"method",key:"_processStep",value:async function(e){if(e instanceof Promise){this._loading="loading_step";try{this._step=await e}catch(e){var t;return this.closeDialog(),void w(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:null==e||null===(t=e.body)||void 0===t?void 0:t.message})}finally{this._loading=void 0}}else void 0!==e?(this._step=void 0,await this.updateComplete,this._step=e):this.closeDialog()}},{kind:"method",key:"_subscribeDataEntryFlowProgressed",value:function(){var e,t;this._unsubDataEntryFlowProgressed||(this._unsubDataEntryFlowProgressed=(e=this.hass.connection,t=async e=>{var t,i;e.data.flow_id===(null===(t=this._step)||void 0===t?void 0:t.flow_id)&&this._processStep(this._params.flowConfig.fetchFlow(this.hass,null===(i=this._step)||void 0===i?void 0:i.flow_id))},e.subscribeEvents(t,"data_entry_flow_progressed")))}},{kind:"get",static:!0,key:"styles",value:function(){return[k,e`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        .dialog-actions {
          padding: 16px;
          position: absolute;
          top: 0;
          right: 0;
        }
        .dialog-actions[rtl] {
          right: auto;
          left: 0;
        }
        .dialog-actions > * {
          color: var(--secondary-text-color);
        }
      `]}}]}}),i);
