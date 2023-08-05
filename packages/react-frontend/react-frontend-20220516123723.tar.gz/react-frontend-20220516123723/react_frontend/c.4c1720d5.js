import{z as e}from"./c.027db416.js";import{L as t,E as i}from"./c.3e14cfd3.js";import{cx as a,cq as s}from"./main-ac83c92b.js";import{a as r}from"./c.c7eb9fb9.js";import"./c.5756eeee.js";import"./c.8cbd7110.js";class n extends(t(i(a))){static get template(){return s`
      <style include="iron-flex"></style>
      <style>
        .container-preset_modes,
        .container-direction,
        .container-percentage,
        .container-oscillating {
          display: none;
        }

        .has-percentage .container-percentage,
        .has-preset_modes .container-preset_modes,
        .has-direction .container-direction,
        .has-oscillating .container-oscillating {
          display: block;
          margin-top: 8px;
        }

        ha-select {
          width: 100%;
        }
      </style>

      <div class$="[[computeClassNames(stateObj)]]">
        <div class="container-percentage">
          <ha-labeled-slider
            caption="[[localize('ui.card.fan.speed')]]"
            min="0"
            max="100"
            step="[[computePercentageStepSize(stateObj)]]"
            value="{{percentageSliderValue}}"
            on-change="percentageChanged"
            pin=""
            extra=""
          ></ha-labeled-slider>
        </div>

        <div class="container-preset_modes">
          <ha-select
            label="[[localize('ui.card.fan.preset_mode')]]"
            value="[[stateObj.attributes.preset_mode]]"
            on-selected="presetModeChanged"
            fixedMenuPosition
            naturalMenuWidth
            on-closed="stopPropagation"
          >
            <template
              is="dom-repeat"
              items="[[stateObj.attributes.preset_modes]]"
            >
              <mwc-list-item value="[[item]]">[[item]]</mwc-list-item>
            </template>
          </ha-select>
        </div>

        <div class="container-oscillating">
          <div class="center horizontal layout single-row">
            <div class="flex">[[localize('ui.card.fan.oscillate')]]</div>
            <ha-switch
              checked="[[oscillationToggleChecked]]"
              on-change="oscillationToggleChanged"
            >
            </ha-switch>
          </div>
        </div>

        <div class="container-direction">
          <div class="direction">
            <div>[[localize('ui.card.fan.direction')]]</div>
            <ha-icon-button
              on-click="onDirectionReverse"
              title="[[localize('ui.card.fan.reverse')]]"
              disabled="[[computeIsRotatingReverse(stateObj)]]"
            >
              <ha-icon icon="hass:rotate-left"></ha-icon>
            </ha-icon-button>
            <ha-icon-button
              on-click="onDirectionForward"
              title="[[localize('ui.card.fan.forward')]]"
              disabled="[[computeIsRotatingForward(stateObj)]]"
            >
              <ha-icon icon="hass:rotate-right"></ha-icon>
            </ha-icon-button>
          </div>
        </div>
      </div>

      <ha-attributes
        hass="[[hass]]"
        state-obj="[[stateObj]]"
        extra-filters="percentage_step,speed,preset_mode,preset_modes,speed_list,percentage,oscillating,direction"
      ></ha-attributes>
    `}static get properties(){return{hass:{type:Object},stateObj:{type:Object,observer:"stateObjChanged"},oscillationToggleChecked:{type:Boolean},percentageSliderValue:{type:Number}}}stateObjChanged(e,t){e&&this.setProperties({oscillationToggleChecked:e.attributes.oscillating,percentageSliderValue:e.attributes.percentage}),t&&setTimeout((()=>{this.fire("iron-resize")}),500)}computePercentageStepSize(e){return e.attributes.percentage_step?e.attributes.percentage_step:1}computeClassNames(t){return"more-info-fan "+(e(t,1)?"has-percentage ":"")+(t.attributes.preset_modes&&t.attributes.preset_modes.length?"has-preset_modes ":"")+r(t,["oscillating","direction"])}presetModeChanged(e){const t=this.stateObj.attributes.preset_mode,i=e.target.value;i&&t!==i&&this.hass.callService("fan","set_preset_mode",{entity_id:this.stateObj.entity_id,preset_mode:i})}stopPropagation(e){e.stopPropagation()}percentageChanged(e){const t=parseInt(this.stateObj.attributes.percentage,10),i=e.target.value;isNaN(i)||t===i||this.hass.callService("fan","set_percentage",{entity_id:this.stateObj.entity_id,percentage:i})}oscillationToggleChanged(e){const t=this.stateObj.attributes.oscillating,i=e.target.checked;t!==i&&this.hass.callService("fan","oscillate",{entity_id:this.stateObj.entity_id,oscillating:i})}onDirectionReverse(){this.hass.callService("fan","set_direction",{entity_id:this.stateObj.entity_id,direction:"reverse"})}onDirectionForward(){this.hass.callService("fan","set_direction",{entity_id:this.stateObj.entity_id,direction:"forward"})}computeIsRotatingReverse(e){return"reverse"===e.attributes.direction}computeIsRotatingForward(e){return"forward"===e.attributes.direction}}customElements.define("more-info-fan",n);
