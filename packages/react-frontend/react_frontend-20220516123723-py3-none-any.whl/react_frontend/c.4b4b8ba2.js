import{_ as e,s as i,e as t,t as s,g as a,i as n,$ as o,f as d,ar as r,n as l,m as h,h as c,cD as _,dT as u,dE as y,dF as m}from"./main-ac83c92b.js";import{d as p,s as g,a as v}from"./c.3e14cfd3.js";import{d as b}from"./c.4e93087d.js";import{h as f,T as k,s as $,ad as w,k as x,_ as z,ae as C,a7 as I,c as B,af as T}from"./c.027db416.js";import"./c.8cbd7110.js";import{s as E,a as S,u as A}from"./c.39da0aeb.js";import{g as D,d as F}from"./c.40d6516d.js";import{f as P}from"./c.5b2e0d05.js";import{S as j}from"./c.02ed471c.js";import{d as O}from"./c.57c0073c.js";import"./c.8eddd911.js";import{s as M}from"./c.cfa85e17.js";import"./c.4860f91b.js";e([l("ha-related-items")],(function(e,i){class l extends i{constructor(...i){super(...i),e(this)}}return{F:l,d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"itemType",value:void 0},{kind:"field",decorators:[t()],key:"itemId",value:void 0},{kind:"field",decorators:[s()],key:"_entries",value:void 0},{kind:"field",decorators:[s()],key:"_devices",value:void 0},{kind:"field",decorators:[s()],key:"_areas",value:void 0},{kind:"field",decorators:[s()],key:"_related",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[E(this.hass.connection,(e=>{this._devices=e})),S(this.hass.connection,(e=>{this._areas=e}))]}},{kind:"method",key:"firstUpdated",value:function(e){a(n(l.prototype),"firstUpdated",this).call(this,e),D(this.hass).then((e=>{this._entries=e})),this.hass.loadBackendTranslation("title")}},{kind:"method",key:"updated",value:function(e){a(n(l.prototype),"updated",this).call(this,e),(e.has("itemId")||e.has("itemType"))&&this.itemId&&this.itemType&&this._findRelated()}},{kind:"method",key:"render",value:function(){return this._related?0===Object.keys(this._related).length?o`
        ${this.hass.localize("ui.components.related-items.no_related_found")}
      `:o`
      ${this._related.config_entry&&this._entries?this._related.config_entry.map((e=>{const i=this._entries.find((i=>i.entry_id===e));return i?o`
              <h3>
                ${this.hass.localize("ui.components.related-items.integration")}:
              </h3>
              <a
                href=${`/config/integrations#config_entry=${e}`}
                @click=${this._navigateAwayClose}
              >
                ${this.hass.localize(`component.${i.domain}.title`)}:
                ${i.title}
              </a>
            `:""})):""}
      ${this._related.device&&this._devices?this._related.device.map((e=>{const i=this._devices.find((i=>i.id===e));return i?o`
              <h3>
                ${this.hass.localize("ui.components.related-items.device")}:
              </h3>
              <a
                href="/config/devices/device/${e}"
                @click=${this._navigateAwayClose}
              >
                ${i.name_by_user||i.name}
              </a>
            `:""})):""}
      ${this._related.area&&this._areas?this._related.area.map((e=>{const i=this._areas.find((i=>i.area_id===e));return i?o`
              <h3>
                ${this.hass.localize("ui.components.related-items.area")}:
              </h3>
              <a
                href="/config/areas/area/${e}"
                @click=${this._navigateAwayClose}
              >
                ${i.name}
              </a>
            `:""})):""}
      ${this._related.entity?o`
            <h3>
              ${this.hass.localize("ui.components.related-items.entity")}:
            </h3>
            <ul>
              ${this._related.entity.map((e=>{const i=this.hass.states[e];return i?o`
                  <li>
                    <button
                      @click=${this._openMoreInfo}
                      .entityId=${e}
                      class="link"
                    >
                      ${i.attributes.friendly_name||e}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.group?o`
            <h3>${this.hass.localize("ui.components.related-items.group")}:</h3>
            <ul>
              ${this._related.group.map((e=>{const i=this.hass.states[e];return i?o`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${e}
                    >
                      ${i.attributes.friendly_name||i.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.scene?o`
            <h3>${this.hass.localize("ui.components.related-items.scene")}:</h3>
            <ul>
              ${this._related.scene.map((e=>{const i=this.hass.states[e];return i?o`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${e}
                    >
                      ${i.attributes.friendly_name||i.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.automation?o`
            <h3>
              ${this.hass.localize("ui.components.related-items.automation")}:
            </h3>
            <ul>
              ${this._related.automation.map((e=>{const i=this.hass.states[e];return i?o`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${e}
                    >
                      ${i.attributes.friendly_name||i.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
      ${this._related.script?o`
            <h3>
              ${this.hass.localize("ui.components.related-items.script")}:
            </h3>
            <ul>
              ${this._related.script.map((e=>{const i=this.hass.states[e];return i?o`
                  <li>
                    <button
                      class="link"
                      @click=${this._openMoreInfo}
                      .entityId=${e}
                    >
                      ${i.attributes.friendly_name||i.entity_id}
                    </button>
                  </li>
                `:""}))}
            </ul>
          `:""}
    `:o``}},{kind:"method",key:"_navigateAwayClose",value:async function(){await new Promise((e=>setTimeout(e,0))),d(this,"close-dialog")}},{kind:"method",key:"_findRelated",value:async function(){this._related=await P(this.hass,this.itemType,this.itemId),await this.updateComplete,d(this,"iron-resize")}},{kind:"method",key:"_openMoreInfo",value:function(e){const i=e.target.entityId;d(this,"hass-more-info",{entityId:i})}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      a {
        color: var(--primary-color);
      }
      button.link {
        color: var(--primary-color);
        text-align: left;
        cursor: pointer;
        background: none;
        border-width: initial;
        border-style: none;
        border-color: initial;
        border-image: initial;
        padding: 0px;
        font: inherit;
        text-decoration: underline;
      }
      h3 {
        font-family: var(--paper-font-title_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-title_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-title_-_font-size);
        font-weight: var(--paper-font-headline-_font-weight);
        letter-spacing: var(--paper-font-title_-_letter-spacing);
        line-height: var(--paper-font-title_-_line-height);
        opacity: var(--dark-primary-opacity);
      }
    `}}]}}),j(i));const H={input_number:"entity-settings-helper-tab",input_select:"entity-settings-helper-tab",input_text:"entity-settings-helper-tab",input_boolean:"entity-settings-helper-tab",input_datetime:"entity-settings-helper-tab",counter:"entity-settings-helper-tab",timer:"entity-settings-helper-tab",input_button:"entity-settings-helper-tab"},L={"HA-Frontend-Base":`${location.protocol}//${location.host}`},U=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),q=(e,i)=>i.context.title_placeholders&&0!==Object.keys(i.context.title_placeholders).length?e(`component.${i.handler}.config.flow_title`,i.context.title_placeholders)||("name"in i.context.title_placeholders?i.context.title_placeholders.name:p(e,i.handler)):p(e,i.handler),R=(e,i)=>{var t;return e.callApi("POST","config/config_entries/options/flow",{handler:i,show_advanced_options:Boolean(null===(t=e.userData)||void 0===t?void 0:t.showAdvanced)})},W=(e,i)=>e.callApi("GET",`config/config_entries/options/flow/${i}`),K=(e,i,t)=>e.callApi("POST",`config/config_entries/options/flow/${i}`,t),N=(e,i)=>e.callApi("DELETE",`config/config_entries/options/flow/${i}`),G=()=>import("./c.0d3a7a49.js"),J=(e,i,t)=>((e,i,t)=>{d(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:G,dialogParams:{...i,flowConfig:t}})})(e,{startFlowHandler:i.entry_id,domain:i.domain,manifest:t},{loadDevicesAndAreas:!1,createFlow:async(e,t)=>{const[s]=await Promise.all([R(e,t),e.loadBackendTranslation("options",i.domain)]);return s},fetchFlow:async(e,t)=>{const[s]=await Promise.all([W(e,t),e.loadBackendTranslation("options",i.domain)]);return s},handleFlowStep:K,deleteFlow:N,renderAbortDescription(e,t){const s=e.localize(`component.${i.domain}.options.abort.${t.reason}`,t.description_placeholders);return s?o`
              <ha-markdown
                breaks
                allowsvg
                .content=${s}
              ></ha-markdown>
            `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${i.domain}.options.step.${t.step_id}.title`)||e.localize("ui.dialogs.options_flow.form.header"),renderShowFormStepDescription(e,t){const s=e.localize(`component.${i.domain}.options.step.${t.step_id}.description`,t.description_placeholders);return s?o`
              <ha-markdown
                allowsvg
                breaks
                .content=${s}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel:(e,t,s)=>e.localize(`component.${i.domain}.options.step.${t.step_id}.data.${s.name}`),renderShowFormStepFieldHelper:(e,t,s)=>e.localize(`component.${i.domain}.options.step.${t.step_id}.data_description.${s.name}`),renderShowFormStepFieldError:(e,t,s)=>e.localize(`component.${i.domain}.options.error.${s}`,t.description_placeholders),renderExternalStepHeader:(e,i)=>"",renderExternalStepDescription:(e,i)=>"",renderCreateEntryDescription:(e,i)=>o`
          <p>${e.localize("ui.dialogs.options_flow.success.description")}</p>
        `,renderShowFormProgressHeader:(e,t)=>e.localize(`component.${i.domain}.options.step.${t.step_id}.title`)||e.localize(`component.${i.domain}.title`),renderShowFormProgressDescription(e,t){const s=e.localize(`component.${i.domain}.options.progress.${t.progress_action}`,t.description_placeholders);return s?o`
              <ha-markdown
                allowsvg
                breaks
                .content=${s}
              ></ha-markdown>
            `:""},renderMenuHeader:(e,i)=>e.localize(`component.${i.handler}.option.step.${i.step_id}.title`)||e.localize(`component.${i.handler}.title`),renderMenuDescription(e,i){const t=e.localize(`component.${i.handler}.option.step.${i.step_id}.description`,i.description_placeholders);return t?o`
              <ha-markdown
                allowsvg
                breaks
                .content=${t}
              ></ha-markdown>
            `:""},renderMenuOption:(e,i,t)=>e.localize(`component.${i.handler}.options.step.${i.step_id}.menu_options.${t}`,i.description_placeholders),renderLoadingDescription:(e,t)=>e.localize(`component.${i.domain}.options.loading`)||e.localize(`ui.dialogs.options_flow.loading.${t}`,{integration:p(e.localize,i.domain)})}),Q=()=>import("./c.7d78ea6b.js"),V={cover:[["awning","blind","curtain","damper","door","garage","gate","shade","shutter","window"]],binary_sensor:[["lock"],["window","door","garage_door","opening"],["battery","battery_charging"],["cold","gas","heat"],["running","motion","moving","occupancy","presence","vibration"],["power","plug","light"],["smoke","safety","sound","problem","tamper","carbon_monoxide","moisture"]]},X={temperature:["°C","°F","K"],pressure:["hPa","Pa","kPa","bar","cbar","mbar","mmHg","inHg","psi"]},Y=["cover","fan","light","lock","siren"];e([l("entity-registry-settings")],(function(e,i){class l extends i{constructor(...i){super(...i),e(this)}}return{F:l,d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"entry",value:void 0},{kind:"field",decorators:[s()],key:"_name",value:void 0},{kind:"field",decorators:[s()],key:"_icon",value:void 0},{kind:"field",decorators:[s()],key:"_entityId",value:void 0},{kind:"field",decorators:[s()],key:"_deviceClass",value:void 0},{kind:"field",decorators:[s()],key:"_switchAs",value:()=>"switch"},{kind:"field",decorators:[s()],key:"_areaId",value:void 0},{kind:"field",decorators:[s()],key:"_disabledBy",value:void 0},{kind:"field",decorators:[s()],key:"_hiddenBy",value:void 0},{kind:"field",decorators:[s()],key:"_device",value:void 0},{kind:"field",decorators:[s()],key:"_helperConfigEntry",value:void 0},{kind:"field",decorators:[s()],key:"_unit_of_measurement",value:void 0},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s()],key:"_submitting",value:void 0},{kind:"field",key:"_origEntityId",value:void 0},{kind:"field",key:"_deviceLookup",value:void 0},{kind:"field",key:"_deviceClassOptions",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){return[E(this.hass.connection,(e=>{this._deviceLookup={};for(const i of e)this._deviceLookup[i.id]=i;this.entry.device_id&&(this._device=this._deviceLookup[this.entry.device_id])}))]}},{kind:"method",key:"firstUpdated",value:function(e){a(n(l.prototype),"firstUpdated",this).call(this,e),this.entry.config_entry_id&&D(this.hass,{type:"helper",domain:this.entry.platform}).then((e=>{this._helperConfigEntry=e.find((e=>e.entry_id===this.entry.config_entry_id))}))}},{kind:"method",key:"willUpdate",value:function(e){if(a(n(l.prototype),"willUpdate",this).call(this,e),!e.has("entry"))return;this._error=void 0,this._name=this.entry.name||"",this._icon=this.entry.icon||"",this._deviceClass=this.entry.device_class||this.entry.original_device_class,this._origEntityId=this.entry.entity_id,this._areaId=this.entry.area_id,this._entityId=this.entry.entity_id,this._disabledBy=this.entry.disabled_by,this._hiddenBy=this.entry.hidden_by,this._device=this.entry.device_id&&this._deviceLookup?this._deviceLookup[this.entry.device_id]:void 0;const i=f(this.entry.entity_id);if("sensor"===i){var t;const e=this.hass.states[this.entry.entity_id];this._unit_of_measurement=null==e||null===(t=e.attributes)||void 0===t?void 0:t.unit_of_measurement}const s=V[i];if(s){this._deviceClassOptions=[[],[]];for(const e of s)e.includes(this.entry.original_device_class)?this._deviceClassOptions[0]=e:this._deviceClassOptions[1].push(...e)}}},{kind:"method",key:"render",value:function(){var e,i,t,s,a,n;if(this.entry.entity_id!==this._origEntityId)return o``;const d=this.hass.states[this.entry.entity_id],r=f(this.entry.entity_id),l=f(this._entityId.trim())!==r;return o`
      ${d?"":o`
            <div class="container warning">
              ${this.hass.localize("ui.dialogs.entity_registry.editor.unavailable")}
              ${null!==(e=this._device)&&void 0!==e&&e.disabled_by?o`<br />${this.hass.localize("ui.dialogs.entity_registry.editor.device_disabled")}<br /><mwc-button @click=${this._openDeviceSettings}>
                      ${this.hass.localize("ui.dialogs.entity_registry.editor.open_device_settings")}
                    </mwc-button>`:""}
            </div>
          `}
      ${this._error?o`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
      <div class="form container">
        <ha-textfield
          .value=${this._name}
          .label=${this.hass.localize("ui.dialogs.entity_registry.editor.name")}
          .invalid=${l}
          .disabled=${this._submitting}
          .placeholder=${this.entry.original_name}
          @input=${this._nameChanged}
        ></ha-textfield>
        <ha-icon-picker
          .value=${this._icon}
          @value-changed=${this._iconChanged}
          .label=${this.hass.localize("ui.dialogs.entity_registry.editor.icon")}
          .placeholder=${this.entry.original_icon||(null==d?void 0:d.attributes.icon)}
          .fallbackPath=${this._icon||null!=d&&d.attributes.icon||!d?void 0:k(f(d.entity_id),d)}
          .disabled=${this._submitting}
        ></ha-icon-picker>
        ${this._deviceClassOptions?o`
              <ha-select
                .label=${this.hass.localize("ui.dialogs.entity_registry.editor.device_class")}
                .value=${this._deviceClass}
                naturalMenuWidth
                fixedMenuPosition
                @selected=${this._deviceClassChanged}
                @closed=${$}
              >
                ${this._deviceClassesSorted(r,this._deviceClassOptions[0],this.hass.localize).map((e=>o`
                    <mwc-list-item .value=${e.deviceClass}>
                      ${e.label}
                    </mwc-list-item>
                  `))}
                ${this._deviceClassOptions[0].length&&this._deviceClassOptions[1].length?o`<li divider role="separator"></li>`:""}
                ${this._deviceClassesSorted(r,this._deviceClassOptions[1],this.hass.localize).map((e=>o`
                    <mwc-list-item .value=${e.deviceClass}>
                      ${e.label}
                    </mwc-list-item>
                  `))}
              </ha-select>
            `:""}
        ${this._deviceClass&&null!=d&&d.attributes.unit_of_measurement&&null!==(i=X[this._deviceClass])&&void 0!==i&&i.includes(null==d?void 0:d.attributes.unit_of_measurement)?o`
              <ha-select
                .label=${this.hass.localize("ui.dialogs.entity_registry.editor.unit_of_measurement")}
                .value=${d.attributes.unit_of_measurement}
                naturalMenuWidth
                fixedMenuPosition
                @selected=${this._unitChanged}
                @closed=${$}
              >
                ${X[this._deviceClass].map((e=>o`
                    <mwc-list-item .value=${e}>${e}</mwc-list-item>
                  `))}
              </ha-select>
            `:""}
        ${"switch"===r?o`<ha-select
              .label=${this.hass.localize("ui.dialogs.entity_registry.editor.device_class")}
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._switchAsChanged}
              @closed=${$}
            >
              <mwc-list-item value="switch" selected>
                ${p(this.hass.localize,"switch")}</mwc-list-item
              >
              <li divider role="separator"></li>
              ${this._switchAsDomainsSorted(Y,this.hass.localize).map((e=>o`
                  <mwc-list-item .value=${e.domain}>
                    ${e.label}
                  </mwc-list-item>
                `))}
            </ha-select>`:""}
        <ha-textfield
          error-message="Domain needs to stay the same"
          .value=${this._entityId}
          .label=${this.hass.localize("ui.dialogs.entity_registry.editor.entity_id")}
          .invalid=${l}
          .disabled=${this._submitting}
          @input=${this._entityIdChanged}
        ></ha-textfield>
        ${this.entry.device_id?"":o`<ha-area-picker
              .hass=${this.hass}
              .value=${this._areaId}
              @value-changed=${this._areaPicked}
            ></ha-area-picker>`}
        ${this._helperConfigEntry?o`
              <div class="row">
                <mwc-button
                  @click=${this._showOptionsFlow}
                  .disabled=${this._submitting}
                >
                  ${this.hass.localize("ui.dialogs.entity_registry.editor.configure_state")}
                </mwc-button>
              </div>
            `:""}

        <ha-expansion-panel
          .header=${this.hass.localize("ui.dialogs.entity_registry.editor.advanced")}
          outlined
        >
          <div class="label">
            ${this.hass.localize("ui.dialogs.entity_registry.editor.entity_status")}:
          </div>
          <div class="secondary">
            ${this._disabledBy&&"user"!==this._disabledBy&&"integration"!==this._disabledBy?this.hass.localize("ui.dialogs.entity_registry.editor.enabled_cause","cause",this.hass.localize(`config_entry.disabled_by.${this._disabledBy}`)):""}
          </div>
          <div class="row">
            <mwc-formfield
              .label=${this.hass.localize("ui.dialogs.entity_registry.editor.enabled_label")}
            >
              <ha-radio
                name="hiddendisabled"
                value="enabled"
                .checked=${!this._hiddenBy&&!this._disabledBy}
                .disabled=${this._hiddenBy&&"user"!==this._hiddenBy||(null===(t=this._device)||void 0===t?void 0:t.disabled_by)||this._disabledBy&&"user"!==this._disabledBy&&"integration"!==this._disabledBy}
                @change=${this._viewStatusChanged}
              ></ha-radio>
            </mwc-formfield>
            <mwc-formfield
              .label=${this.hass.localize("ui.dialogs.entity_registry.editor.hidden_label")}
            >
              <ha-radio
                name="hiddendisabled"
                value="hidden"
                .checked=${null!==this._hiddenBy}
                .disabled=${this._hiddenBy&&"user"!==this._hiddenBy||Boolean(null===(s=this._device)||void 0===s?void 0:s.disabled_by)||this._disabledBy&&"user"!==this._disabledBy&&"integration"!==this._disabledBy}
                @change=${this._viewStatusChanged}
              ></ha-radio>
            </mwc-formfield>
            <mwc-formfield
              .label=${this.hass.localize("ui.dialogs.entity_registry.editor.disabled_label")}
            >
              <ha-radio
                name="hiddendisabled"
                value="disabled"
                .checked=${null!==this._disabledBy}
                .disabled=${this._hiddenBy&&"user"!==this._hiddenBy||Boolean(null===(a=this._device)||void 0===a?void 0:a.disabled_by)||this._disabledBy&&"user"!==this._disabledBy&&"integration"!==this._disabledBy}
                @change=${this._viewStatusChanged}
              ></ha-radio>
            </mwc-formfield>
          </div>

          ${null!==this._disabledBy?o`
                <div class="secondary">
                  ${this.hass.localize("ui.dialogs.entity_registry.editor.enabled_description")}
                </div>
              `:null!==this._hiddenBy?o`
                <div class="secondary">
                  ${this.hass.localize("ui.dialogs.entity_registry.editor.hidden_description")}
                </div>
              `:""}
          ${this.entry.device_id?o`
                <div class="label">
                  ${this.hass.localize("ui.dialogs.entity_registry.editor.change_area")}:
                </div>
                <ha-area-picker
                  .hass=${this.hass}
                  .value=${this._areaId}
                  .placeholder=${null===(n=this._device)||void 0===n?void 0:n.area_id}
                  .label=${this.hass.localize("ui.dialogs.entity_registry.editor.area")}
                  @value-changed=${this._areaPicked}
                ></ha-area-picker>
                <div class="secondary">
                  ${this.hass.localize("ui.dialogs.entity_registry.editor.area_note")}
                  ${this._device?o`
                        <button class="link" @click=${this._openDeviceSettings}>
                          ${this.hass.localize("ui.dialogs.entity_registry.editor.change_device_area")}
                        </button>
                      `:""}
                </div>
              `:""}
        </ha-expansion-panel>
      </div>
      <div class="buttons">
        <mwc-button
          class="warning"
          @click=${this._confirmDeleteEntry}
          .disabled=${this._submitting||!this._helperConfigEntry&&!(null!=d&&d.attributes.restored)}
        >
          ${this.hass.localize("ui.dialogs.entity_registry.editor.delete")}
        </mwc-button>
        <mwc-button
          @click=${this._updateEntry}
          .disabled=${l||this._submitting}
        >
          ${this.hass.localize("ui.dialogs.entity_registry.editor.update")}
        </mwc-button>
      </div>
    `}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_iconChanged",value:function(e){this._error=void 0,this._icon=e.detail.value}},{kind:"method",key:"_entityIdChanged",value:function(e){this._error=void 0,this._entityId=e.target.value}},{kind:"method",key:"_deviceClassChanged",value:function(e){this._error=void 0,this._deviceClass=e.target.value}},{kind:"method",key:"_unitChanged",value:function(e){this._error=void 0,this._unit_of_measurement=e.target.value}},{kind:"method",key:"_switchAsChanged",value:function(e){""!==e.target.value&&(this._switchAs=e.target.value)}},{kind:"method",key:"_areaPicked",value:function(e){this._error=void 0,this._areaId=e.detail.value}},{kind:"method",key:"_viewStatusChanged",value:function(e){switch(e.target.value){case"enabled":this._disabledBy=null,this._hiddenBy=null;break;case"disabled":this._disabledBy="user",this._hiddenBy=null;break;case"hidden":this._hiddenBy="user",this._disabledBy=null}}},{kind:"method",key:"_openDeviceSettings",value:function(){var e,i;e=this,i={device:this._device,updateEntry:async e=>{await A(this.hass,this._device.id,e)}},d(e,"show-dialog",{dialogTag:"dialog-device-registry-detail",dialogImport:Q,dialogParams:i})}},{kind:"method",key:"_updateEntry",value:async function(){var e;this._submitting=!0;const i=this.getRootNode().host,t={name:this._name.trim()||null,icon:this._icon.trim()||null,area_id:this._areaId||null,device_class:this._deviceClass||null,new_entity_id:this._entityId.trim()},s=this.hass.states[this.entry.entity_id],a=f(this.entry.entity_id);this.entry.disabled_by===this._disabledBy||null!==this._disabledBy&&"user"!==this._disabledBy||(t.disabled_by=this._disabledBy),this.entry.hidden_by===this._hiddenBy||null!==this._hiddenBy&&"user"!==this._hiddenBy||(t.hidden_by=this._hiddenBy),"sensor"===a&&(null==s||null===(e=s.attributes)||void 0===e?void 0:e.unit_of_measurement)!==this._unit_of_measurement&&(t.options_domain="sensor",t.options={unit_of_measurement:this._unit_of_measurement});try{const e=await w(this.hass,this._origEntityId,t);e.require_restart&&x(this,{text:this.hass.localize("ui.dialogs.entity_registry.editor.enabled_restart_confirm")}),e.reload_delay&&x(this,{text:this.hass.localize("ui.dialogs.entity_registry.editor.enabled_delay_confirm","delay",e.reload_delay)}),d(this,"close-dialog")}catch(e){this._error=e.message||"Unknown error"}finally{this._submitting=!1}if("switch"!==this._switchAs){var n;if(!await z(this,{text:this.hass.localize("ui.dialogs.entity_registry.editor.switch_as_x_confirm","domain",this._switchAs)}))return;const e=await(o=this.hass,r="switch_as_x",o.callApi("POST","config/config_entries/flow",{handler:r,show_advanced_options:Boolean(null===(l=o.userData)||void 0===l?void 0:l.showAdvanced)},L)),t=await((e,i,t)=>e.callApi("POST",`config/config_entries/flow/${i}`,t,L))(this.hass,e.flow_id,{entity_id:this._entityId.trim(),target_domain:this._switchAs});if(null===(n=t.result)||void 0===n||!n.entry_id)return;const s=await this.hass.connection.subscribeEvents((()=>{s(),C(this.hass.connection).then((e=>{const s=e.find((e=>e.config_entry_id===t.result.entry_id));s&&g(i,{entity_id:s.entity_id})}))}),"entity_registry_updated")}var o,r,l}},{kind:"method",key:"_confirmDeleteEntry",value:async function(){if(await z(this,{text:this.hass.localize("ui.dialogs.entity_registry.editor.confirm_delete")})){this._submitting=!0;try{this._helperConfigEntry?await F(this.hass,this._helperConfigEntry.entry_id):await I(this.hass,this._origEntityId),d(this,"close-dialog")}finally{this._submitting=!1}}}},{kind:"method",key:"_showOptionsFlow",value:async function(){J(this,this._helperConfigEntry,null)}},{kind:"field",key:"_switchAsDomainsSorted",value:()=>h(((e,i)=>e.map((e=>({domain:e,label:p(i,e)}))).sort(((e,i)=>M(e.label,i.label)))))},{kind:"field",key:"_deviceClassesSorted",value:()=>h(((e,i,t)=>i.map((i=>({deviceClass:i,label:t(`ui.dialogs.entity_registry.editor.device_classes.${e}.${i}`)}))).sort(((e,i)=>M(e.label,i.label)))))},{kind:"get",static:!0,key:"styles",value:function(){return[c,r`
        :host {
          display: block;
        }
        .container {
          padding: 20px 24px;
        }
        .form {
          margin-bottom: 53px;
        }
        .buttons {
          position: absolute;
          bottom: 0;
          width: 100%;
          box-sizing: border-box;
          border-top: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
          display: flex;
          justify-content: space-between;
          padding: 8px;
          padding-bottom: max(env(safe-area-inset-bottom), 8px);
          background-color: var(--mdc-theme-surface, #fff);
        }
        ha-select {
          width: 100%;
          margin: 8px 0;
        }
        ha-switch {
          margin-right: 16px;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
        ha-area-picker {
          margin: 8px 0;
          display: block;
        }
        .row {
          margin: 8px 0;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .label {
          margin-top: 16px;
        }
        .secondary {
          margin: 8px 0;
          width: 340px;
        }
        li[divider] {
          border-bottom-color: var(--divider-color);
        }
      `]}}]}}),j(i));let Z=e([l("dialog-entity-editor")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_params",value:void 0},{kind:"field",decorators:[s()],key:"_entry",value:void 0},{kind:"field",decorators:[s()],key:"_curTab",value:()=>"tab-settings"},{kind:"field",decorators:[s()],key:"_extraTabs",value:()=>({})},{kind:"field",decorators:[s()],key:"_settingsElementTag",value:void 0},{kind:"field",key:"_curTabIndex",value:()=>0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._entry=void 0,this._settingsElementTag=void 0,this._extraTabs={},this._getEntityReg()}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,d(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params||void 0===this._entry)return o``;const e=this._params.entity_id,i=this._entry,t=this.hass.states[e];return o`
      <ha-dialog
        open
        .heading=${t?B(t):(null==i?void 0:i.name)||e}
        hideActions
        @closed=${this.closeDialog}
        @close-dialog=${this.closeDialog}
      >
        <div slot="heading">
          <ha-header-bar>
            <ha-icon-button
              slot="navigationIcon"
              .label=${this.hass.localize("ui.dialogs.entity_registry.dismiss")}
              .path=${_}
              dialogAction="cancel"
            ></ha-icon-button>
            <span slot="title">
              ${t?B(t):(null==i?void 0:i.name)||e}
            </span>
            ${t?o`
                  <ha-icon-button
                    slot="actionItems"
                    .label=${this.hass.localize("ui.dialogs.entity_registry.control")}
                    .path=${u}
                    @click=${this._openMoreInfo}
                  ></ha-icon-button>
                `:""}
          </ha-header-bar>
          <mwc-tab-bar
            .activeIndex=${this._curTabIndex}
            @MDCTabBar:activated=${this._handleTabActivated}
            @MDCTab:interacted=${this._handleTabInteracted}
          >
            <mwc-tab
              id="tab-settings"
              .label=${this.hass.localize("ui.dialogs.entity_registry.settings")}
              dialogInitialFocus
            >
            </mwc-tab>
            ${Object.entries(this._extraTabs).map((([e,i])=>o`
                <mwc-tab
                  id=${e}
                  .label=${this.hass.localize(i.translationKey)||e}
                >
                </mwc-tab>
              `))}
            <mwc-tab
              id="tab-related"
              .label=${this.hass.localize("ui.dialogs.entity_registry.related")}
            >
            </mwc-tab>
          </mwc-tab-bar>
        </div>
        <div class="wrapper">${v(this._renderTab())}</div>
      </ha-dialog>
    `}},{kind:"method",key:"_renderTab",value:function(){switch(this._curTab){case"tab-settings":return this._entry?this._settingsElementTag?o`
              ${b(this._settingsElementTag,{hass:this.hass,entry:this._entry,entityId:this._params.entity_id})}
            `:o``:o`
          <div class="content">
            ${this.hass.localize("ui.dialogs.entity_registry.no_unique_id","entity_id",this._params.entity_id,"faq_link",o`<a
                href=${O(this.hass,"/faq/unique_id")}
                target="_blank"
                rel="noreferrer"
                >${this.hass.localize("ui.dialogs.entity_registry.faq")}</a
              >`)}
          </div>
        `;case"tab-related":return o`
          <ha-related-items
            class="content"
            .hass=${this.hass}
            .itemId=${this._params.entity_id}
            itemType="entity"
          ></ha-related-items>
        `;default:return o``}}},{kind:"method",key:"_getEntityReg",value:async function(){try{this._entry=await T(this.hass,this._params.entity_id),this._loadPlatformSettingTabs()}catch{this._entry=null}}},{kind:"method",key:"_handleTabActivated",value:function(e){this._curTabIndex=e.detail.index}},{kind:"method",key:"_handleTabInteracted",value:function(e){this._curTab=e.detail.tabId}},{kind:"method",key:"_loadPlatformSettingTabs",value:async function(){if(!this._entry)return;if(!Object.keys(H).includes(this._entry.platform))return void(this._settingsElementTag="entity-registry-settings");const e=H[this._entry.platform];await import(`./editor-tabs/settings/${e}`),this._settingsElementTag=e}},{kind:"method",key:"_openMoreInfo",value:function(){y(),d(this,"hass-more-info",{entityId:this._params.entity_id}),this.closeDialog()}},{kind:"get",static:!0,key:"styles",value:function(){return[m,r`
        ha-header-bar {
          --mdc-theme-on-primary: var(--primary-text-color);
          --mdc-theme-primary: var(--mdc-theme-surface);
          flex-shrink: 0;
        }

        mwc-tab-bar {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }

        ha-dialog {
          --dialog-content-position: static;
          --dialog-content-padding: 0;
          --dialog-z-index: 6;
        }

        @media all and (min-width: 451px) and (min-height: 501px) {
          .wrapper {
            min-width: 400px;
          }
        }

        .content {
          display: block;
          padding: 20px 24px;
        }

        /* overrule the ha-style-dialog max-height on small screens */
        @media all and (max-width: 450px), all and (max-height: 500px) {
          ha-header-bar {
            --mdc-theme-primary: var(--app-header-background-color);
            --mdc-theme-on-primary: var(--app-header-text-color, white);
          }
        }

        mwc-button.warning {
          --mdc-theme-primary: var(--error-color);
        }

        :host([rtl]) app-toolbar {
          direction: rtl;
          text-align: right;
        }
      `]}}]}}),i);var ee=Object.freeze({__proto__:null,DialogEntityEditor:Z});export{ee as d,U as f,q as l};
