import{_ as i,s as t,e as a,t as e,$ as n,aq as s,ax as o,ar as c,n as r}from"./main-ac83c92b.js";import{aH as l,aJ as h,aS as d,aB as f,aC as u,aK as g,Q as p,T as _,aT as m,aD as v,aU as x}from"./c.3e14cfd3.js";import{c as y,U as k}from"./c.027db416.js";import"./c.8cbd7110.js";i([r("hui-weather-entity-row")],(function(i,t){return{F:class extends t{constructor(...t){super(...t),i(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(i){if(null==i||!i.entity)throw new Error("Entity must be specified");this._config=i}},{kind:"method",key:"shouldUpdate",value:function(i){return l(this,i)}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return n``;const i=this.hass.states[this._config.entity];if(!i)return n`
        <hui-warning>
          ${h(this.hass,this._config.entity)}
        </hui-warning>
      `;const t=!(this._config.tap_action&&"none"!==this._config.tap_action.action),a=d(i.state,this);return n`
      <div
        class="icon-image ${s({pointer:t})}"
        @action=${this._handleAction}
        .actionHandler=${f({hasHold:u(this._config.hold_action),hasDoubleClick:u(this._config.double_tap_action)})}
        tabindex=${o(t?"0":void 0)}
      >
        ${a||n`
          <ha-state-icon
            class="weather-icon"
            .state=${i}
          ></ha-state-icon>
        `}
      </div>
      <div
        class="info ${s({pointer:t})}"
        @action=${this._handleAction}
        .actionHandler=${f({hasHold:u(this._config.hold_action),hasDoubleClick:u(this._config.double_tap_action)})}
      >
        ${this._config.name||y(i)}
      </div>
      <div
        class="attributes ${s({pointer:t})}"
        @action=${this._handleAction}
        .actionHandler=${f({hasHold:u(this._config.hold_action),hasDoubleClick:u(this._config.double_tap_action)})}
      >
        <div>
          ${k.includes(i.state)?g(this.hass.localize,i,this.hass.locale):n`
                ${p(i.attributes.temperature,this.hass.locale)}
                ${_(this.hass,"temperature")}
              `}
        </div>
        <div class="secondary">
          ${m(this.hass,i)}
        </div>
      </div>
    `}},{kind:"method",key:"_handleAction",value:function(i){v(this,this.hass,this._config,i.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return[x,c`
        :host {
          display: flex;
          align-items: center;
          flex-direction: row;
        }

        .info {
          margin-left: 16px;
          flex: 1 0 60px;
        }

        .info,
        .info > * {
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .icon-image {
          display: flex;
          align-items: center;
          min-width: 40px;
        }

        .icon-image > * {
          flex: 0 0 40px;
          height: 40px;
        }

        .icon-image:focus {
          outline: none;
          background-color: var(--divider-color);
          border-radius: 50%;
        }

        .weather-icon {
          --mdc-icon-size: 40px;
        }

        :host([rtl]) .flex {
          margin-left: 0;
          margin-right: 16px;
        }

        .pointer {
          cursor: pointer;
        }

        .attributes {
          display: flex;
          flex-direction: column;
          justify-content: center;
          text-align: right;
          margin-left: 8px;
        }

        .secondary {
          color: var(--secondary-text-color);
        }
      `]}}]}}),t);
