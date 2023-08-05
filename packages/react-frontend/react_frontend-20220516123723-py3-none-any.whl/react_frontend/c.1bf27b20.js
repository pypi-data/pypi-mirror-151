import{_ as t,s as i,e,t as a,g as o,i as s,di as n,$ as c,aq as h,ax as r,ar as l,n as d}from"./main-ac83c92b.js";import{$ as g,h as f,c as u}from"./c.027db416.js";import{aG as p,aE as m,aH as _,aB as v,aC as b,aJ as y,aK as k,aD as $}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";const w=new Set(["closed","locked","not_home","off"]);t([d("hui-picture-glance-card")],(function(t,i){class d extends i{constructor(...i){super(...i),t(this)}}return{F:d,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.484e32c7.js"),document.createElement("hui-picture-glance-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,i,e){return{type:"picture-glance",title:"Kitchen",image:"https://demo.home-assistant.io/stub_config/kitchen.png",entities:p(t,2,i,e,["sensor","binary_sensor"])}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"field",key:"_entitiesDialog",value:void 0},{kind:"field",key:"_entitiesToggle",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entities||!Array.isArray(t.entities)||!(t.image||t.camera_image||t.state_image)||t.state_image&&!t.entity)throw new Error("Invalid configuration");const i=m(t.entities);this._entitiesDialog=[],this._entitiesToggle=[],i.forEach((i=>{t.force_dialog||!g.has(f(i.entity))?this._entitiesDialog.push(i):this._entitiesToggle.push(i)})),this._config={hold_action:{action:"more-info"},...t}}},{kind:"method",key:"shouldUpdate",value:function(t){if(_(this,t))return!0;const i=t.get("hass");if(!i||i.themes!==this.hass.themes||i.locale!==this.hass.locale)return!0;if(this._entitiesDialog)for(const t of this._entitiesDialog)if(i.states[t.entity]!==this.hass.states[t.entity])return!0;if(this._entitiesToggle)for(const t of this._entitiesToggle)if(i.states[t.entity]!==this.hass.states[t.entity])return!0;return!1}},{kind:"method",key:"updated",value:function(t){if(o(s(d.prototype),"updated",this).call(this,t),!this._config||!this.hass)return;const i=t.get("hass"),e=t.get("_config");i&&e&&i.themes===this.hass.themes&&e.theme===this._config.theme||n(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?c`
      <ha-card>
        <hui-image
          class=${h({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.camera_image)})}
          @action=${this._handleAction}
          .actionHandler=${v({hasHold:b(this._config.hold_action),hasDoubleClick:b(this._config.double_tap_action)})}
          tabindex=${r(b(this._config.tap_action)?"0":void 0)}
          .config=${this._config}
          .hass=${this.hass}
          .image=${this._config.image}
          .stateImage=${this._config.state_image}
          .stateFilter=${this._config.state_filter}
          .cameraImage=${this._config.camera_image}
          .cameraView=${this._config.camera_view}
          .entity=${this._config.entity}
          .aspectRatio=${this._config.aspect_ratio}
        ></hui-image>
        <div class="box">
          ${this._config.title?c` <div class="title">${this._config.title}</div> `:""}
          <div class="row">
            ${this._entitiesDialog.map((t=>this.renderEntity(t,!0)))}
          </div>
          <div class="row">
            ${this._entitiesToggle.map((t=>this.renderEntity(t,!1)))}
          </div>
        </div>
      </ha-card>
    `:c``}},{kind:"method",key:"renderEntity",value:function(t,i){const e=this.hass.states[t.entity];return t={tap_action:{action:i?"more-info":"toggle"},hold_action:{action:"more-info"},...t},e?c`
      <div class="wrapper">
        <ha-icon-button
          @action=${this._handleAction}
          .actionHandler=${v({hasHold:b(t.hold_action),hasDoubleClick:b(t.double_tap_action)})}
          tabindex=${r(b(t.tap_action)?void 0:"-1")}
          .disabled=${!b(t.tap_action)}
          .config=${t}
          class=${h({"state-on":!w.has(e.state)})}
          title=${`${u(e)} : ${k(this.hass.localize,e,this.hass.locale)}`}
        >
          <ha-state-icon
            .icon=${t.icon}
            .state=${e}
          ></ha-state-icon>
        </ha-icon-button>

        ${!0!==this._config.show_state&&!0!==t.show_state?c`<div class="state"></div>`:c`
              <div class="state">
                ${t.attribute?c`
                      ${t.prefix}${e.attributes[t.attribute]}${t.suffix}
                    `:k(this.hass.localize,e,this.hass.locale)}
              </div>
            `}
      </div>
    `:c`
        <hui-warning-element
          .label=${y(this.hass,t.entity)}
        ></hui-warning-element>
      `}},{kind:"method",key:"_handleAction",value:function(t){const i=t.currentTarget.config;$(this,this.hass,i,t.detail.action)}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-card {
        position: relative;
        min-height: 48px;
        overflow: hidden;
        height: 100%;
        box-sizing: border-box;
      }

      hui-image.clickable {
        cursor: pointer;
      }

      .box {
        /* start paper-font-common-nowrap style */
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        /* end paper-font-common-nowrap style */

        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: var(
          --ha-picture-card-background-color,
          rgba(0, 0, 0, 0.3)
        );
        padding: 4px 8px;
        font-size: 16px;
        line-height: 40px;
        color: var(--ha-picture-card-text-color, white);
        display: flex;
        justify-content: space-between;
        flex-direction: row;
      }

      .box .title {
        font-weight: 500;
        margin-left: 8px;
      }

      ha-icon-button {
        --mdc-icon-button-size: 40px;
        --disabled-text-color: currentColor;
        color: var(--ha-picture-icon-button-color, #a9a9a9);
      }

      ha-icon-button.state-on {
        color: var(--ha-picture-icon-button-on-color, white);
      }
      hui-warning-element {
        padding: 0 8px;
      }
      .state {
        display: block;
        font-size: 12px;
        text-align: center;
        line-height: 12px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .row {
        display: flex;
        flex-direction: row;
      }
      .wrapper {
        display: flex;
        flex-direction: column;
        width: 40px;
      }
    `}}]}}),i);
