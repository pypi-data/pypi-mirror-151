import{_ as t,s as i,e,t as a,g as s,i as o,di as n,$ as c,ax as h,ar as r,n as d}from"./main-ac83c92b.js";import{h as g,c as f}from"./c.027db416.js";import{aG as u,aH as l,aJ as m,aK as _,aB as p,aC as y,aD as v}from"./c.3e14cfd3.js";import"./c.8cbd7110.js";t([d("hui-picture-entity-card")],(function(t,i){class d extends i{constructor(...i){super(...i),t(this)}}return{F:d,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.8f85e0e0.js"),document.createElement("hui-picture-entity-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,i,e){return{type:"picture-entity",entity:u(t,1,i,e,["light","switch"])[0]||"",image:"https://demo.home-assistant.io/stub_config/bedroom.png"}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[a()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.entity)throw new Error("Entity must be specified");if("camera"!==g(t.entity)&&!t.image&&!t.state_image&&!t.camera_image)throw new Error("No image source configured");this._config={show_name:!0,show_state:!0,...t}}},{kind:"method",key:"shouldUpdate",value:function(t){return l(this,t)}},{kind:"method",key:"updated",value:function(t){if(s(o(d.prototype),"updated",this).call(this,t),!this._config||!this.hass)return;const i=t.get("hass"),e=t.get("_config");i&&e&&i.themes===this.hass.themes&&e.theme===this._config.theme||n(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return c``;const t=this.hass.states[this._config.entity];if(!t)return c`
        <hui-warning>
          ${m(this.hass,this._config.entity)}
        </hui-warning>
      `;const i=this._config.name||f(t),e=_(this.hass.localize,t,this.hass.locale);let a="";return this._config.show_name&&this._config.show_state?a=c`
        <div class="footer both">
          <div>${i}</div>
          <div>${e}</div>
        </div>
      `:this._config.show_name?a=c`<div class="footer single">${i}</div>`:this._config.show_state&&(a=c`<div class="footer single">${e}</div>`),c`
      <ha-card>
        <hui-image
          .hass=${this.hass}
          .image=${this._config.image}
          .stateImage=${this._config.state_image}
          .stateFilter=${this._config.state_filter}
          .cameraImage=${"camera"===g(this._config.entity)?this._config.entity:this._config.camera_image}
          .cameraView=${this._config.camera_view}
          .entity=${this._config.entity}
          .aspectRatio=${this._config.aspect_ratio}
          @action=${this._handleAction}
          .actionHandler=${p({hasHold:y(this._config.hold_action),hasDoubleClick:y(this._config.double_tap_action)})}
          tabindex=${h(y(this._config.tap_action)||this._config.entity?"0":void 0)}
        ></hui-image>
        ${a}
      </ha-card>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      ha-card {
        min-height: 75px;
        overflow: hidden;
        position: relative;
        height: 100%;
        box-sizing: border-box;
      }

      hui-image {
        cursor: pointer;
      }

      .footer {
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
        padding: 16px;
        font-size: 16px;
        line-height: 16px;
        color: var(--ha-picture-card-text-color, white);
      }

      .both {
        display: flex;
        justify-content: space-between;
      }

      .single {
        text-align: center;
      }
    `}},{kind:"method",key:"_handleAction",value:function(t){v(this,this.hass,this._config,t.detail.action)}}]}}),i);
