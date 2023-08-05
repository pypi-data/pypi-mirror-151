import{_ as e,s as i,e as a,t as s,f as t,$ as d,h as l,dF as r,ar as o,n}from"./main-ac83c92b.js";import"./c.4860f91b.js";import"./c.8cbd7110.js";import"./c.027db416.js";import{c}from"./c.39da0aeb.js";import"./c.02ed471c.js";import"./c.0e001851.js";import"./c.cfa85e17.js";e([n("dialog-device-registry-detail")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_nameByUser",value:void 0},{kind:"field",decorators:[s()],key:"_error",value:void 0},{kind:"field",decorators:[s()],key:"_params",value:void 0},{kind:"field",decorators:[a()],key:"_areaId",value:void 0},{kind:"field",decorators:[s()],key:"_disabledBy",value:void 0},{kind:"field",decorators:[s()],key:"_submitting",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._error=void 0,this._nameByUser=this._params.device.name_by_user||"",this._areaId=this._params.device.area_id,this._disabledBy=this._params.device.disabled_by,await this.updateComplete}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,t(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return d``;const e=this._params.device;return d`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${c(e,this.hass)}
      >
        <div>
          ${this._error?d`<ha-alert alert-type="error">${this._error}</ha-alert> `:""}
          <div class="form">
            <ha-textfield
              .value=${this._nameByUser}
              @input=${this._nameChanged}
              .label=${this.hass.localize("ui.panel.config.devices.name")}
              .placeholder=${e.name||""}
              .disabled=${this._submitting}
              dialogInitialFocus
            ></ha-textfield>
            <ha-area-picker
              .hass=${this.hass}
              .value=${this._areaId}
              @value-changed=${this._areaPicked}
            ></ha-area-picker>
            <div class="row">
              <ha-switch
                .checked=${!this._disabledBy}
                @change=${this._disabledByChanged}
              >
              </ha-switch>
              <div>
                <div>
                  ${this.hass.localize("ui.panel.config.devices.enabled_label","type",this.hass.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`))}
                </div>
                <div class="secondary">
                  ${this._disabledBy&&"user"!==this._disabledBy?this.hass.localize("ui.panel.config.devices.enabled_cause","type",this.hass.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`),"cause",this.hass.localize(`config_entry.disabled_by.${this._disabledBy}`)):""}
                  ${this.hass.localize("ui.panel.config.devices.enabled_description")}
                </div>
              </div>
            </div>
          </div>
        </div>
        <mwc-button
          slot="secondaryAction"
          @click=${this.closeDialog}
          .disabled=${this._submitting}
        >
          ${this.hass.localize("ui.common.cancel")}
        </mwc-button>
        <mwc-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${this._submitting}
        >
          ${this.hass.localize("ui.panel.config.devices.update")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._nameByUser=e.target.value}},{kind:"method",key:"_areaPicked",value:function(e){this._areaId=e.detail.value}},{kind:"method",key:"_disabledByChanged",value:function(e){this._disabledBy=e.target.checked?null:"user"}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0;try{await this._params.updateEntry({name_by_user:this._nameByUser.trim()||null,area_id:this._areaId||null,disabled_by:this._disabledBy||null}),this.closeDialog()}catch(e){this._error=e.message||this.hass.localize("ui.panel.config.devices.unknown_error")}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[l,r,o`
        .form {
          padding-bottom: 24px;
        }
        mwc-button.warning {
          margin-right: auto;
        }
        ha-textfield {
          display: block;
          margin-bottom: 16px;
        }
        ha-switch {
          margin-right: 16px;
        }
        .row {
          margin-top: 8px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
      `]}}]}}),i);
