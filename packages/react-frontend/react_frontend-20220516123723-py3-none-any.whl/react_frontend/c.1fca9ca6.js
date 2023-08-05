import{_ as e,s as t,e as i,ap as a,$ as s,f as d,n as l,ar as o,g as n,i as r,t as u,cE as h,cF as c,cJ as v,cD as m,m as k,ea as f,W as p}from"./main-ac83c92b.js";import{d as b}from"./c.4e93087d.js";import"./c.3e14cfd3.js";import"./c.8eddd911.js";import"./c.c8193d47.js";import{s as y}from"./c.027db416.js";import"./c.e9aa747b.js";import"./c.8e198788.js";import"./c.25e73c3c.js";import{c as g}from"./c.5ea5eadd.js";function $(e){return Array.isArray(e)?e[0]:e}function _(e){return Array.isArray(e)?e[1]||e[0]:e}e([l("ha-form-boolean")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a("ha-checkbox",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return s`
      <mwc-formfield .label=${this.label}>
        <ha-checkbox
          .checked=${this.data}
          .disabled=${this.disabled}
          @change=${this._valueChanged}
        ></ha-checkbox>
      </mwc-formfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){d(this,"value-changed",{value:e.target.checked})}}]}}),t),e([l("ha-form-constant")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"method",key:"render",value:function(){return s`<span class="label">${this.label}</span>${this.schema.value?`: ${this.schema.value}`:""}`}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: block;
      }
      .label {
        font-weight: 500;
      }
    `}}]}}),t),e([l("ha-form-grid")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i()],key:"computeLabel",value:void 0},{kind:"field",decorators:[i()],key:"computeHelper",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){n(r(a.prototype),"firstUpdated",this).call(this,e),this.setAttribute("own-margin","")}},{kind:"method",key:"updated",value:function(e){n(r(a.prototype),"updated",this).call(this,e),e.has("schema")&&(this.schema.column_min_width?this.style.setProperty("--form-grid-min-width",this.schema.column_min_width):this.style.setProperty("--form-grid-min-width",""))}},{kind:"method",key:"render",value:function(){return s`
      ${this.schema.schema.map((e=>s`
            <ha-form
              .hass=${this.hass}
              .data=${this.data}
              .schema=${[e]}
              .disabled=${this.disabled}
              .computeLabel=${this.computeLabel}
              .computeHelper=${this.computeHelper}
            ></ha-form>
          `))}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: grid !important;
        grid-template-columns: repeat(
          var(--form-grid-column-count, auto-fit),
          minmax(var(--form-grid-min-width, 200px), 1fr)
        );
        grid-gap: 8px;
      }
      :host > ha-form {
        display: block;
        margin-bottom: 24px;
      }
    `}}]}}),t),e([l("ha-form-float")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a("ha-textfield")],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e;return s`
      <ha-textfield
        inputMode="decimal"
        .label=${this.label}
        .value=${void 0!==this.data?this.data:""}
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .autoValidate=${this.schema.required}
        .suffix=${null===(e=this.schema.description)||void 0===e?void 0:e.suffix}
        .validationMessage=${this.schema.required?"Required":void 0}
        @input=${this._valueChanged}
      ></ha-textfield>
    `}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!!this.schema.required)}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.target,i=t.value.replace(",",".");let a;if(!i.endsWith("."))if(""!==i&&(a=parseFloat(i),isNaN(a)&&(a=void 0)),this.data!==a)d(this,"value-changed",{value:a});else{const e=void 0===a?"":String(a);t.value!==e&&(t.value=e)}}},{kind:"field",static:!0,key:"styles",value:()=>o`
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    ha-textfield {
      display: block;
    }
  `}]}}),t),e([l("ha-form-integer")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a("ha-textfield ha-slider")],key:"_input",value:void 0},{kind:"field",key:"_lastValue",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e;return void 0!==this.schema.valueMin&&void 0!==this.schema.valueMax&&this.schema.valueMax-this.schema.valueMin<256?s`
        <div>
          ${this.label}
          <div class="flex">
            ${this.schema.required?"":s`
                  <ha-checkbox
                    @change=${this._handleCheckboxChange}
                    .checked=${void 0!==this.data}
                    .disabled=${this.disabled}
                  ></ha-checkbox>
                `}
            <ha-slider
              pin
              ignore-bar-touch
              .value=${this._value}
              .min=${this.schema.valueMin}
              .max=${this.schema.valueMax}
              .disabled=${this.disabled||void 0===this.data&&!this.schema.required}
              @change=${this._valueChanged}
            ></ha-slider>
          </div>
        </div>
      `:s`
      <ha-textfield
        type="number"
        inputMode="numeric"
        .label=${this.label}
        .value=${void 0!==this.data?this.data:""}
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .autoValidate=${this.schema.required}
        .suffix=${null===(e=this.schema.description)||void 0===e?void 0:e.suffix}
        .validationMessage=${this.schema.required?"Required":void 0}
        @input=${this._valueChanged}
      ></ha-textfield>
    `}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!("valueMin"in this.schema&&"valueMax"in this.schema||!this.schema.required))}},{kind:"get",key:"_value",value:function(){var e;return void 0!==this.data?this.data:this.schema.required?(null===(e=this.schema.description)||void 0===e?void 0:e.suggested_value)||this.schema.default||this.schema.valueMin||0:this.schema.valueMin||0}},{kind:"method",key:"_handleCheckboxChange",value:function(e){let t;if(e.target.checked)for(const e of[this._lastValue,null===(i=this.schema.description)||void 0===i?void 0:i.suggested_value,this.schema.default,0]){var i;if(void 0!==e){t=e;break}}else this._lastValue=this.data;d(this,"value-changed",{value:t})}},{kind:"method",key:"_valueChanged",value:function(e){const t=e.target,i=t.value;let a;if(""!==i&&(a=parseInt(String(i))),this.data!==a)d(this,"value-changed",{value:a});else{const e=void 0===a?"":String(a);t.value!==e&&(t.value=e)}}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host([own-margin]) {
        margin-bottom: 5px;
      }
      .flex {
        display: flex;
      }
      ha-slider {
        flex: 1;
      }
      ha-textfield {
        display: block;
      }
    `}}]}}),t);e([l("ha-form-multi_select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[u()],key:"_opened",value:()=>!1},{kind:"field",decorators:[a("ha-button-menu")],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){const e=Array.isArray(this.schema.options)?this.schema.options:Object.entries(this.schema.options),t=this.data||[];return e.length<6?s`<div>
        ${this.label}${e.map((e=>{const i=$(e);return s`
            <ha-formfield .label=${_(e)}>
              <ha-checkbox
                .checked=${t.includes(i)}
                .value=${i}
                .disabled=${this.disabled}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
          `}))}
      </div> `:s`
      <ha-button-menu
        .disabled=${this.disabled}
        fixed
        corner="BOTTOM_START"
        @opened=${this._handleOpen}
        @closed=${this._handleClose}
        multi
        activatable
      >
        <ha-textfield
          slot="trigger"
          .label=${this.label}
          .value=${t.map((e=>this.schema.options[e]||e)).join(", ")}
          .disabled=${this.disabled}
          tabindex="-1"
        ></ha-textfield>
        <ha-svg-icon
          slot="trigger"
          .path=${this._opened?h:c}
        ></ha-svg-icon>
        ${e.map((e=>{const i=$(e),a=t.includes(i);return s`<ha-check-list-item
            left
            .selected=${a}
            .activated=${a}
            @request-selected=${this._selectedChanged}
            .value=${i}
            .disabled=${this.disabled}
          >
            ${_(e)}
          </ha-check-list-item>`}))}
      </ha-button-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>{var e;const{formElement:t,mdcRoot:i}=(null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("ha-textfield"))||{};t&&(t.style.textOverflow="ellipsis"),i&&(i.style.cursor="pointer")}))}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",Object.keys(this.schema.options).length>=6&&!!this.schema.required)}},{kind:"method",key:"_selectedChanged",value:function(e){e.stopPropagation(),"property"!==e.detail.source&&this._handleValueChanged(e.target.value,e.detail.selected)}},{kind:"method",key:"_valueChanged",value:function(e){const{value:t,checked:i}=e.target;this._handleValueChanged(t,i)}},{kind:"method",key:"_handleValueChanged",value:function(e,t){let i;if(t)if(this.data){if(this.data.includes(e))return;i=[...this.data,e]}else i=[e];else{if(!this.data.includes(e))return;i=this.data.filter((t=>t!==e))}d(this,"value-changed",{value:i})}},{kind:"method",key:"_handleOpen",value:function(e){e.stopPropagation(),this._opened=!0,this.toggleAttribute("opened",!0)}},{kind:"method",key:"_handleClose",value:function(e){e.stopPropagation(),this._opened=!1,this.toggleAttribute("opened",!1)}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host([own-margin]) {
        margin-bottom: 5px;
      }
      ha-button-menu {
        display: block;
        cursor: pointer;
      }
      ha-formfield {
        display: block;
        padding-right: 16px;
      }
      ha-textfield {
        display: block;
        pointer-events: none;
      }
      ha-svg-icon {
        color: var(--input-dropdown-icon-color);
        position: absolute;
        right: 1em;
        top: 1em;
        cursor: pointer;
      }
      :host([opened]) ha-svg-icon {
        color: var(--primary-color);
      }
      :host([opened]) ha-button-menu {
        --mdc-text-field-idle-line-color: var(--input-hover-line-color);
        --mdc-text-field-label-ink-color: var(--primary-color);
      }
    `}}]}}),t),e([l("ha-duration-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"enableMillisecond",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"enableDay",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a("paper-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return s`
      <ha-base-time-input
        .label=${this.label}
        .helper=${this.helper}
        .required=${this.required}
        .autoValidate=${this.required}
        .disabled=${this.disabled}
        errorMessage="Required"
        enableSecond
        .enableMillisecond=${this.enableMillisecond}
        .enableDay=${this.enableDay}
        format="24"
        .days=${this._days}
        .hours=${this._hours}
        .minutes=${this._minutes}
        .seconds=${this._seconds}
        .milliseconds=${this._milliseconds}
        @value-changed=${this._durationChanged}
        noHoursLimit
        dayLabel="dd"
        hourLabel="hh"
        minLabel="mm"
        secLabel="ss"
        millisecLabel="ms"
      ></ha-base-time-input>
    `}},{kind:"get",key:"_days",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.days?Number(this.data.days):0}},{kind:"get",key:"_hours",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.hours?Number(this.data.hours):0}},{kind:"get",key:"_minutes",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.minutes?Number(this.data.minutes):0}},{kind:"get",key:"_seconds",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.seconds?Number(this.data.seconds):0}},{kind:"get",key:"_milliseconds",value:function(){var e;return null!==(e=this.data)&&void 0!==e&&e.milliseconds?Number(this.data.milliseconds):0}},{kind:"method",key:"_durationChanged",value:function(e){e.stopPropagation();const t={...e.detail.value};var i;(this.enableMillisecond||t.milliseconds?t.milliseconds>999&&(t.seconds+=Math.floor(t.milliseconds/1e3),t.milliseconds%=1e3):delete t.milliseconds,t.seconds>59&&(t.minutes+=Math.floor(t.seconds/60),t.seconds%=60),t.minutes>59&&(t.hours+=Math.floor(t.minutes/60),t.minutes%=60),this.enableDay&&t.hours>24)&&(t.days=(null!==(i=t.days)&&void 0!==i?i:0)+Math.floor(t.hours/24),t.hours%=24);d(this,"value-changed",{value:t})}}]}}),t),e([l("ha-form-positive_time_period_dict")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[a("ha-time-input",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return s`
      <ha-duration-input
        .label=${this.label}
        .required=${this.schema.required}
        .data=${this.data}
        .disabled=${this.disabled}
      ></ha-duration-input>
    `}}]}}),t),e([l("ha-chip-set")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return s`
      <div class="mdc-chip-set">
        <slot></slot>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      ${v(g)}

      slot::slotted(ha-chip) {
        margin: 4px 4px 4px 0;
      }
    `}}]}}),t),e([l("ha-selector-select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[i()],key:"value",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"required",value:()=>!0},{kind:"field",decorators:[a("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_filter",value:()=>""},{kind:"method",key:"render",value:function(){const e=this.selector.select.options.map((e=>"object"==typeof e?e:{value:e,label:e}));if(!this.selector.select.custom_value&&"list"===this._mode)return!this.selector.select.multiple||this.required?s`
          <div>
            ${this.label}
            ${e.map((e=>s`
                <mwc-formfield .label=${e.label}>
                  <ha-radio
                    .checked=${e.value===this.value}
                    .value=${e.value}
                    .disabled=${this.disabled}
                    @change=${this._valueChanged}
                  ></ha-radio>
                </mwc-formfield>
              `))}
          </div>
          ${this._renderHelper()}
        `:s`
        <div>
          ${this.label}${e.map((e=>{var t;return s`
              <ha-formfield .label=${e.label}>
                <ha-checkbox
                  .checked=${null===(t=this.value)||void 0===t?void 0:t.includes(e.value)}
                  .value=${e.value}
                  .disabled=${this.disabled}
                  @change=${this._checkboxChanged}
                ></ha-checkbox>
              </ha-formfield>
            `}))}
        </div>
        ${this._renderHelper()}
      `;if(this.selector.select.multiple){const t=this.value&&""!==this.value?this.value:[];return s`
        <ha-chip-set>
          ${null==t?void 0:t.map(((t,i)=>{var a;return s`
                <ha-chip hasTrailingIcon>
                  ${(null===(a=e.find((e=>e.value===t)))||void 0===a?void 0:a.label)||t}
                  <ha-svg-icon
                    slot="trailing-icon"
                    .path=${m}
                    .idx=${i}
                    @click=${this._removeItem}
                  ></ha-svg-icon>
                </ha-chip>
              `}))}
        </ha-chip-set>

        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${this.hass}
          .label=${this.label}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .required=${this.required&&!t.length}
          .value=${this._filter}
          .items=${e.filter((e=>{var t;return!(null!==(t=this.value)&&void 0!==t&&t.includes(e.value))}))}
          @filter-changed=${this._filterChanged}
          @value-changed=${this._comboBoxValueChanged}
        ></ha-combo-box>
      `}return this.selector.select.custom_value?(void 0===this.value||e.find((e=>e.value===this.value))||e.unshift({value:this.value,label:this.value}),s`
        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${this.hass}
          .label=${this.label}
          .helper=${this.helper}
          .disabled=${this.disabled}
          .required=${this.required}
          .items=${e}
          .value=${this.value}
          @filter-changed=${this._filterChanged}
          @value-changed=${this._comboBoxValueChanged}
        ></ha-combo-box>
      `):s`
      <ha-select
        fixedMenuPosition
        naturalMenuWidth
        .label=${this.label}
        .value=${this.value}
        .helper=${this.helper}
        .disabled=${this.disabled}
        @closed=${y}
        @selected=${this._valueChanged}
      >
        ${e.map((e=>s`
            <mwc-list-item .value=${e.value}>${e.label}</mwc-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"_renderHelper",value:function(){return this.helper?s`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""}},{kind:"get",key:"_mode",value:function(){return this.selector.select.mode||(this.selector.select.options.length<6?"list":"dropdown")}},{kind:"method",key:"_valueChanged",value:function(e){var t;e.stopPropagation();const i=(null===(t=e.detail)||void 0===t?void 0:t.value)||e.target.value;!this.disabled&&i&&d(this,"value-changed",{value:i})}},{kind:"method",key:"_checkboxChanged",value:function(e){if(e.stopPropagation(),this.disabled)return;let t;const i=e.target.value;if(e.target.checked)if(this.value){if(this.value.includes(i))return;t=[...this.value,i]}else t=[i];else{var a;if(null===(a=this.value)||void 0===a||!a.includes(i))return;t=this.value.filter((e=>e!==i))}d(this,"value-changed",{value:t})}},{kind:"method",key:"_removeItem",value:async function(e){const t=[...this.value];t.splice(e.target.idx,1),d(this,"value-changed",{value:t}),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_comboBoxValueChanged",value:function(e){var t;e.stopPropagation();const i=e.detail.value;if(this.disabled||""===i)return;if(!this.selector.select.multiple)return void d(this,"value-changed",{value:i});if(void 0!==i&&null!==(t=this.value)&&void 0!==t&&t.includes(i))return;setTimeout((()=>{this._filterChanged(),this.comboBox.setInputValue("")}),0);const a=this.value&&""!==this.value?this.value:[];d(this,"value-changed",{value:[...a,i]})}},{kind:"method",key:"_filterChanged",value:function(e){var t;this._filter=(null==e?void 0:e.detail.value)||"";const i=null===(t=this.comboBox.items)||void 0===t?void 0:t.filter((e=>{var t,i;if(this.selector.select.multiple&&null!==(t=this.value)&&void 0!==t&&t.includes(e.value))return!1;return(e.label||e.value).toLowerCase().includes(null===(i=this._filter)||void 0===i?void 0:i.toLowerCase())}));this._filter&&this.selector.select.custom_value&&(null==i||i.unshift({label:this._filter,value:this._filter})),this.comboBox.filteredItems=i}},{kind:"field",static:!0,key:"styles",value:()=>o`
    ha-select,
    mwc-formfield,
    ha-formfield {
      display: block;
    }
  `}]}}),t),e([l("ha-form-select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",key:"_selectSchema",value:()=>k((e=>({select:{options:e.map((e=>({value:e[0],label:e[1]})))}})))},{kind:"method",key:"render",value:function(){return s`
      <ha-selector-select
        .hass=${this.hass}
        .schema=${this.schema}
        .value=${this.data}
        .label=${this.label}
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .selector=${this._selectSchema(this.schema.options)}
        @value-changed=${this._valueChanged}
      ></ha-selector-select>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();let t=e.detail.value;t!==this.data&&(""===t&&(t=void 0),d(this,"value-changed",{value:t}))}}]}}),t);const x=["password","secret","token"];e([l("ha-form-string")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"data",value:void 0},{kind:"field",decorators:[i()],key:"label",value:void 0},{kind:"field",decorators:[i()],key:"helper",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[u()],key:"_unmaskedPassword",value:()=>!1},{kind:"field",decorators:[a("ha-textfield")],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){var e;const t=x.some((e=>this.schema.name.includes(e)));return s`
      <ha-textfield
        .type=${t?this._unmaskedPassword?"text":"password":this._stringType}
        .label=${this.label}
        .value=${this.data||""}
        .helper=${this.helper}
        helperPersistent
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .autoValidate=${this.schema.required}
        .suffix=${t?s`<div style="width: 24px"></div>`:null===(e=this.schema.description)||void 0===e?void 0:e.suffix}
        .validationMessage=${this.schema.required?"Required":void 0}
        @input=${this._valueChanged}
      ></ha-textfield>
      ${t?s`<ha-icon-button
            toggles
            .label=${(this._unmaskedPassword?"Hide":"Show")+" password"}
            @click=${this._toggleUnmaskedPassword}
            .path=${this._unmaskedPassword?f:p}
          ></ha-icon-button>`:""}
    `}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",!!this.schema.required)}},{kind:"method",key:"_toggleUnmaskedPassword",value:function(){this._unmaskedPassword=!this._unmaskedPassword}},{kind:"method",key:"_valueChanged",value:function(e){let t=e.target.value;this.data!==t&&(""!==t||this.schema.required||(t=void 0),d(this,"value-changed",{value:t}))}},{kind:"get",key:"_stringType",value:function(){if(this.schema.format){if(["email","url"].includes(this.schema.format))return this.schema.format;if("fqdnurl"===this.schema.format)return"url"}return"text"}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      :host {
        display: block;
        position: relative;
      }
      :host([own-margin]) {
        margin-bottom: 5px;
      }
      ha-textfield {
        display: block;
      }
      ha-icon-button {
        position: absolute;
        top: 1em;
        right: 12px;
        --mdc-icon-button-size: 24px;
        color: var(--secondary-text-color);
      }
    `}}]}}),t);const w=(e,t)=>e?t.name?e[t.name]:e:null;let C=!1;e([l("ha-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[i()],key:"error",value:void 0},{kind:"field",decorators:[i({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[i()],key:"computeError",value:void 0},{kind:"field",decorators:[i()],key:"computeLabel",value:void 0},{kind:"field",decorators:[i()],key:"computeHelper",value:void 0},{kind:"method",key:"focus",value:function(){var e;const t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector(".root");if(t)for(const e of t.children)if("HA-ALERT"!==e.tagName){e.focus();break}}},{kind:"method",key:"willUpdate",value:function(e){var t;n(r(a.prototype),"willUpdate",this).call(this,e),!C&&e.has("schema")&&null!==(t=this.schema)&&void 0!==t&&t.some((e=>"selector"in e))&&(C=!0,import("./c.958cb46c.js"))}},{kind:"method",key:"render",value:function(){return s`
      <div class="root" part="root">
        ${this.error&&this.error.base?s`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e);return s`
            ${t?s`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:""}
            ${"selector"in e?s`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .selector=${e.selector}
                  .value=${w(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${this.disabled}
                  .helper=${this._computeHelper(e)}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:b(`ha-form-${e.type}`,{schema:e,data:w(this.data,e),label:this._computeLabel(e,this.data),disabled:this.disabled,hass:this.hass,computeLabel:this.computeLabel,computeHelper:this.computeHelper,context:this._generateContext(e)})}
          `}))}
      </div>
    `}},{kind:"method",key:"_generateContext",value:function(e){if(!e.context)return;const t={};for(const[i,a]of Object.entries(e.context))t[i]=this.data[a];return t}},{kind:"method",key:"createRenderRoot",value:function(){const e=n(r(a.prototype),"createRenderRoot",this).call(this);return e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema,i=t.name?{[t.name]:e.detail.value}:e.detail.value;d(this,"value-changed",{value:{...this.data,...i}})})),e}},{kind:"method",key:"_computeLabel",value:function(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}},{kind:"method",key:"_computeHelper",value:function(e){return this.computeHelper?this.computeHelper(e):""}},{kind:"method",key:"_computeError",value:function(e,t){return this.computeError?this.computeError(e,t):e}},{kind:"get",static:!0,key:"styles",value:function(){return o`
      .root {
        margin-bottom: -24px;
        overflow: clip visible;
      }
      .root > * {
        display: block;
      }
      .root > *:not([own-margin]) {
        margin-bottom: 24px;
      }
      ha-alert[own-margin] {
        margin-bottom: 4px;
      }
    `}}]}}),t);
