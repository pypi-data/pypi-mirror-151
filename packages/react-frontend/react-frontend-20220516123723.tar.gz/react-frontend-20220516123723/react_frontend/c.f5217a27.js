import{_ as a,s as t,e,t as i,ap as o,g as n,i as r,di as s,$ as l,aq as c,f as d,ar as h,n as m}from"./main-ac83c92b.js";import{at as u,x as p}from"./c.027db416.js";import{aG as f,aJ as g}from"./c.3e14cfd3.js";import"./c.5ea5eadd.js";import{F as y,c as _}from"./c.af439a08.js";import"./c.8cbd7110.js";const v=["1","2","3","4","5","6","7","8","9","","0","clear"];a([m("hui-alarm-panel-card")],(function(a,t){class m extends t{constructor(...t){super(...t),a(this)}}return{F:m,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.4ecf8f0b.js"),document.createElement("hui-alarm-panel-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(a,t,e){return{type:"alarm-panel",states:["arm_home","arm_away"],entity:f(a,1,t,e,["alarm_control_panel"])[0]||""}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"field",decorators:[o("#alarmCode")],key:"_input",value:void 0},{kind:"method",key:"getCardSize",value:async function(){if(!this._config||!this.hass)return 9;const a=this.hass.states[this._config.entity];return a&&a.attributes.code_format===y?9:4}},{kind:"method",key:"setConfig",value:function(a){if(!a||!a.entity||"alarm_control_panel"!==a.entity.split(".")[0])throw new Error("Invalid configuration");this._config={states:["arm_away","arm_home"],...a}}},{kind:"method",key:"updated",value:function(a){if(n(r(m.prototype),"updated",this).call(this,a),!this._config||!this.hass)return;const t=a.get("hass"),e=a.get("_config");t&&e&&t.themes===this.hass.themes&&e.theme===this._config.theme||s(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"shouldUpdate",value:function(a){if(a.has("_config"))return!0;const t=a.get("hass");return!t||t.themes!==this.hass.themes||t.locale!==this.hass.locale||t.states[this._config.entity]!==this.hass.states[this._config.entity]}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return l``;const a=this.hass.states[this._config.entity];if(!a)return l`
        <hui-warning>
          ${g(this.hass,this._config.entity)}
        </hui-warning>
      `;const t=this._stateDisplay(a.state);return l`
      <ha-card>
        <h1 class="card-header">
          ${this._config.name||a.attributes.friendly_name||t}
          <ha-chip
            hasIcon
            class=${c({[a.state]:!0})}
            @click=${this._handleMoreInfo}
          >
            <ha-svg-icon slot="icon" .path=${u(a.state)}>
            </ha-svg-icon>
            ${t}
          </ha-chip>
        </h1>
        <div id="armActions" class="actions">
          ${("disarmed"===a.state?this._config.states:["disarm"]).map((a=>l`
              <mwc-button
                .action=${a}
                @click=${this._handleActionClick}
                outlined
              >
                ${this._actionDisplay(a)}
              </mwc-button>
            `))}
        </div>
        ${a.attributes.code_format?l`
              <ha-textfield
                id="alarmCode"
                .label=${this.hass.localize("ui.card.alarm_control_panel.code")}
                type="password"
                .inputmode=${a.attributes.code_format===y?"numeric":"text"}
              ></ha-textfield>
            `:l``}
        ${a.attributes.code_format!==y?l``:l`
              <div id="keypad">
                ${v.map((a=>""===a?l` <mwc-button disabled></mwc-button> `:l`
                        <mwc-button
                          .value=${a}
                          @click=${this._handlePadClick}
                          outlined
                          class=${c({numberkey:"clear"!==a})}
                        >
                          ${"clear"===a?this.hass.localize("ui.card.alarm_control_panel.clear_code"):a}
                        </mwc-button>
                      `))}
              </div>
            `}
      </ha-card>
    `}},{kind:"method",key:"_actionDisplay",value:function(a){return this.hass.localize(`ui.card.alarm_control_panel.${a}`)}},{kind:"method",key:"_stateDisplay",value:function(a){return a===p?this.hass.localize("state.default.unavailable"):this.hass.localize(`component.alarm_control_panel.state._.${a}`)||a}},{kind:"method",key:"_handlePadClick",value:function(a){const t=a.currentTarget.value;this._input.value="clear"===t?"":this._input.value+t}},{kind:"method",key:"_handleActionClick",value:function(a){const t=this._input;_(this.hass,this._config.entity,a.currentTarget.action,(null==t?void 0:t.value)||void 0),t&&(t.value="")}},{kind:"method",key:"_handleMoreInfo",value:function(){d(this,"hass-more-info",{entityId:this._config.entity})}},{kind:"get",static:!0,key:"styles",value:function(){return h`
      ha-card {
        padding-bottom: 16px;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
        --alarm-color-disarmed: var(--label-badge-green);
        --alarm-color-pending: var(--label-badge-yellow);
        --alarm-color-triggered: var(--label-badge-red);
        --alarm-color-armed: var(--label-badge-red);
        --alarm-color-autoarm: rgba(0, 153, 255, 0.1);
        --alarm-state-color: var(--alarm-color-armed);
      }

      ha-chip {
        --ha-chip-background-color: var(--alarm-state-color);
        --primary-text-color: var(--text-primary-color);
        line-height: initial;
      }

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
      }

      .unavailable {
        --alarm-state-color: var(--state-unavailable-color);
      }

      .disarmed {
        --alarm-state-color: var(--alarm-color-disarmed);
      }

      .triggered {
        --alarm-state-color: var(--alarm-color-triggered);
        animation: pulse 1s infinite;
      }

      .arming {
        --alarm-state-color: var(--alarm-color-pending);
        animation: pulse 1s infinite;
      }

      .pending {
        --alarm-state-color: var(--alarm-color-pending);
        animation: pulse 1s infinite;
      }

      @keyframes pulse {
        0% {
          opacity: 1;
        }
        50% {
          opacity: 0;
        }
        100% {
          opacity: 1;
        }
      }

      ha-textfield {
        display: block;
        margin: 8px;
        max-width: 150px;
        text-align: center;
      }

      .state {
        margin-left: 16px;
        position: relative;
        bottom: 16px;
        color: var(--alarm-state-color);
        animation: none;
      }

      #keypad {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin: auto;
        width: 100%;
        max-width: 300px;
      }

      #keypad mwc-button {
        padding: 8px;
        width: 30%;
        box-sizing: border-box;
      }

      .actions {
        margin: 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
      }

      .actions mwc-button {
        margin: 0 4px 4px;
      }

      mwc-button#disarm {
        color: var(--error-color);
      }

      mwc-button.numberkey {
        --mdc-typography-button-font-size: var(--keypad-font-size, 0.875rem);
      }
    `}}]}}),t);
