import{z as e}from"./c.027db416.js";import{E as t,L as a}from"./c.3e14cfd3.js";import{cx as r,cq as s,d$ as i,e0 as o}from"./main-ac83c92b.js";import{f as n}from"./c.9f624ee3.js";import"./c.8cbd7110.js";class l extends(t(r)){static get template(){return s`
      <style include="iron-flex iron-flex-alignment"></style>
      <style>
        /* local DOM styles go here */
        :host {
          @apply --layout-flex;
          @apply --layout-horizontal;
          @apply --layout-justified;
        }
        .in-flux#target_temperature {
          color: var(--error-color);
        }
        #target_temperature {
          @apply --layout-self-center;
          font-size: 200%;
        }
        .control-buttons {
          font-size: 200%;
          text-align: right;
        }
        ha-icon-button {
          height: 48px;
          width: 48px;
        }
      </style>

      <!-- local DOM goes here -->
      <div id="target_temperature">[[value]] [[units]]</div>
      <div class="control-buttons">
        <div>
          <ha-icon-button on-click="incrementValue">
            <ha-icon icon="hass:chevron-up"></ha-icon>
          </ha-icon-button>
        </div>
        <div>
          <ha-icon-button on-click="decrementValue">
            <ha-icon icon="hass:chevron-down"></ha-icon>
          </ha-icon-button>
        </div>
      </div>
    `}static get properties(){return{value:{type:Number,observer:"valueChanged"},units:{type:String},min:{type:Number},max:{type:Number},step:{type:Number,value:1}}}temperatureStateInFlux(e){this.$.target_temperature.classList.toggle("in-flux",e)}incrementValue(){const e=this.value+this.step;this.value<this.max&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e<=this.max?e<=this.min?this.value=this.min:this.value=e:this.value=this.max}decrementValue(){const e=this.value-this.step;this.value>this.min&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e>=this.min?this.value=e:this.value=this.min}valueChanged(){this.last_changed&&window.setTimeout((()=>{Date.now()-this.last_changed>=2e3&&(this.fire("change"),this.temperatureStateInFlux(!1),this.last_changed=null)}),2010)}}customElements.define("ha-water_heater-control",l);class c extends(a(t(r))){static get template(){return s`
      <style include="iron-flex"></style>
      <style>
        :host {
          color: var(--primary-text-color);
        }

        ha-select {
          width: 100%;
        }

        ha-water_heater-control.range-control-left,
        ha-water_heater-control.range-control-right {
          float: left;
          width: 46%;
        }
        ha-water_heater-control.range-control-left {
          margin-right: 4%;
        }
        ha-water_heater-control.range-control-right {
          margin-left: 4%;
        }

        .single-row {
          padding: 8px 0;
        }
      </style>

      <div class$="[[computeClassNames(stateObj)]]">
        <div class="container-temperature">
          <div class$="[[stateObj.attributes.operation_mode]]">
            <div hidden$="[[!supportsTemperatureControls(stateObj)]]">
              [[localize('ui.card.water_heater.target_temperature')]]
            </div>
            <template is="dom-if" if="[[supportsTemperature(stateObj)]]">
              <ha-water_heater-control
                value="[[stateObj.attributes.temperature]]"
                units="[[hass.config.unit_system.temperature]]"
                step="[[computeTemperatureStepSize(hass, stateObj)]]"
                min="[[stateObj.attributes.min_temp]]"
                max="[[stateObj.attributes.max_temp]]"
                on-change="targetTemperatureChanged"
              >
              </ha-water_heater-control>
            </template>
          </div>
        </div>

        <template is="dom-if" if="[[supportsOperationMode(stateObj)]]">
          <div class="container-operation_list">
            <div class="controls">
              <ha-select
                label="[[localize('ui.card.water_heater.operation')]]"
                value="[[stateObj.attributes.operation_mode]]"
                on-selected="handleOperationmodeChanged"
                fixedMenuPosition
                naturalMenuWidth
                on-closed="stopPropagation"
              >
                <template
                  is="dom-repeat"
                  items="[[stateObj.attributes.operation_list]]"
                >
                  <mwc-list-item value="[[item]]">
                    [[_localizeOperationMode(localize, item)]]
                  </mwc-list-item>
                </template>
              </ha-select>
            </div>
          </div>
        </template>

        <template is="dom-if" if="[[supportsAwayMode(stateObj)]]">
          <div class="container-away_mode">
            <div class="center horizontal layout single-row">
              <div class="flex">
                [[localize('ui.card.water_heater.away_mode')]]
              </div>
              <ha-switch
                checked="[[awayToggleChecked]]"
                on-change="awayToggleChanged"
              >
              </ha-switch>
            </div>
          </div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},stateObj:{type:Object,observer:"stateObjChanged"},awayToggleChecked:Boolean}}stateObjChanged(e,t){e&&this.setProperties({awayToggleChecked:"on"===e.attributes.away_mode}),t&&(this._debouncer=i.debounce(this._debouncer,o.after(500),(()=>{this.fire("iron-resize")})))}computeTemperatureStepSize(e,t){return t.attributes.target_temp_step?t.attributes.target_temp_step:-1!==e.config.unit_system.temperature.indexOf("F")?1:.5}supportsTemperatureControls(e){return this.supportsTemperature(e)}supportsTemperature(t){return e(t,1)&&"number"==typeof t.attributes.temperature}supportsOperationMode(t){return e(t,2)}supportsAwayMode(t){return e(t,4)}computeClassNames(e){const t=[n(e,{1:"has-target_temperature",2:"has-operation_mode",4:"has-away_mode"})];return t.push("more-info-water_heater"),t.join(" ")}targetTemperatureChanged(e){const t=e.target.value;t!==this.stateObj.attributes.temperature&&this.callServiceHelper("set_temperature",{temperature:t})}awayToggleChanged(e){const t="on"===this.stateObj.attributes.away_mode,a=e.target.checked;t!==a&&this.callServiceHelper("set_away_mode",{away_mode:a})}handleOperationmodeChanged(e){const t=this.stateObj.attributes.operation_mode,a=e.target.value;a&&t!==a&&this.callServiceHelper("set_operation_mode",{operation_mode:a})}stopPropagation(e){e.stopPropagation()}callServiceHelper(e,t){t.entity_id=this.stateObj.entity_id,this.hass.callService("water_heater",e,t).then((()=>{this.stateObjChanged(this.stateObj)}))}_localizeOperationMode(e,t){return e(`component.water_heater.state._.${t}`)||t}}customElements.define("more-info-water_heater",c);
