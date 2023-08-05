import{_ as e,s as i,e as t,$ as a,eb as o,ar as l,n,m as s,f as c}from"./main-ac83c92b.js";import{s as r}from"./c.027db416.js";import"./c.958cb46c.js";e([n("ha-help-tooltip")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"position",value:()=>"top"},{kind:"method",key:"render",value:function(){return a`
      <ha-svg-icon .path=${o}></ha-svg-icon>
      <paper-tooltip
        offset="4"
        .position=${this.position}
        .fitToVisibleBounds=${!0}
        >${this.label}</paper-tooltip
      >
    `}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-svg-icon {
        --mdc-icon-size: var(--ha-help-tooltip-size, 14px);
        color: var(--ha-help-tooltip-color, var(--disabled-text-color));
      }
    `}}]}}),i),e([n("hui-action-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t()],key:"config",value:void 0},{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"actions",value:void 0},{kind:"field",decorators:[t()],key:"tooltipText",value:void 0},{kind:"field",decorators:[t()],key:"hass",value:void 0},{kind:"get",key:"_navigation_path",value:function(){const e=this.config;return(null==e?void 0:e.navigation_path)||""}},{kind:"get",key:"_url_path",value:function(){const e=this.config;return(null==e?void 0:e.url_path)||""}},{kind:"get",key:"_service",value:function(){const e=this.config;return(null==e?void 0:e.service)||""}},{kind:"field",key:"_serviceAction",value(){return s((e=>({service:this._service,data:e.service_data,target:e.target})))}},{kind:"method",key:"render",value:function(){var e,i,t,o,l,n;return this.hass&&this.actions?a`
      <div class="dropdown">
        <ha-select
          .label=${this.label}
          .configValue=${"action"}
          @selected=${this._actionPicked}
          .value=${null!==(e=null===(i=this.config)||void 0===i?void 0:i.action)&&void 0!==e?e:"default"}
          @closed=${r}
          fixedMenuPosition
          naturalMenuWidt
        >
          <mwc-list-item value="default">
            ${this.hass.localize("ui.panel.lovelace.editor.action-editor.actions.default_action")}
          </mwc-list-item>
          ${this.actions.map((e=>a`
              <mwc-list-item .value=${e}>
                ${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${e}`)}
              </mwc-list-item>
            `))}
        </ha-select>
        ${this.tooltipText?a`
              <ha-help-tooltip .label=${this.tooltipText}></ha-help-tooltip>
            `:""}
      </div>
      ${"navigate"===(null===(t=this.config)||void 0===t?void 0:t.action)?a`
            <ha-textfield
              label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.navigation_path")}
              .value=${this._navigation_path}
              .configValue=${"navigation_path"}
              @input=${this._valueChanged}
            ></ha-textfield>
          `:""}
      ${"url"===(null===(o=this.config)||void 0===o?void 0:o.action)?a`
            <ha-textfield
              .label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.url_path")}
              .value=${this._url_path}
              .configValue=${"url_path"}
              @input=${this._valueChanged}
            ></ha-textfield>
          `:""}
      ${"call-service"===(null===(l=this.config)||void 0===l?void 0:l.action)?a`
            <ha-service-control
              .hass=${this.hass}
              .value=${this._serviceAction(this.config)}
              .showAdvanced=${null===(n=this.hass.userData)||void 0===n?void 0:n.showAdvanced}
              narrow
              @value-changed=${this._serviceValueChanged}
            ></ha-service-control>
          `:""}
    `:a``}},{kind:"method",key:"_actionPicked",value:function(e){var i;if(e.stopPropagation(),!this.hass)return;const t=e.target.value;if((null===(i=this.config)||void 0===i?void 0:i.action)===t)return;if("default"===t)return void c(this,"value-changed",{value:void 0});let a;switch(t){case"url":a={url_path:this._url_path};break;case"call-service":a={service:this._service};break;case"navigate":a={navigation_path:this._navigation_path}}c(this,"value-changed",{value:{action:t,...a}})}},{kind:"method",key:"_valueChanged",value:function(e){if(e.stopPropagation(),!this.hass)return;const i=e.target,t=e.target.value;this[`_${i.configValue}`]!==t&&i.configValue&&c(this,"value-changed",{value:{...this.config,[i.configValue]:t}})}},{kind:"method",key:"_serviceValueChanged",value:function(e){e.stopPropagation(),c(this,"value-changed",{value:{...this.config,service:e.detail.value.service||"",service_data:e.detail.value.data||{},target:e.detail.value.target||{}}})}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      .dropdown {
        position: relative;
      }
      ha-help-tooltip {
        position: absolute;
        right: 40px;
        top: 16px;
      }
      ha-select,
      ha-textfield {
        width: 100%;
      }
      ha-textfield {
        margin-top: 8px;
      }
      ha-service-control {
        --service-control-padding: 0;
      }
    `}}]}}),i);
