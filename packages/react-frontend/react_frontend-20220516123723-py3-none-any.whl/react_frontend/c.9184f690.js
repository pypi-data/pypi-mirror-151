import{_ as e,s as t,e as a,t as s,$ as i,aq as n,g as o,i as c,ar as r,n as d}from"./main-ac83c92b.js";const l="http://192.168.1.234:8123",h=!1,u="A078F6B0",g="urn:x-cast:com.nabucasa.hast",f=(e,t)=>e.sendMessage({type:"connect",refreshToken:t.data.refresh_token,clientId:t.data.clientId,hassUrl:t.data.hassUrl});e([d("hui-cast-row")],(function(e,t){class d extends t{constructor(...t){super(...t),e(this)}}return{F:d,d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[s()],key:"_config",value:void 0},{kind:"field",decorators:[s()],key:"_castManager",value:void 0},{kind:"field",decorators:[s()],key:"_noHTTPS",value:()=>!1},{kind:"method",key:"setConfig",value:function(e){if(!e||void 0===e.view||null===e.view)throw new Error("View required");this._config={icon:"hass:television",name:"Home Assistant Cast",...e}}},{kind:"method",key:"shouldUpdate",value:function(e){return!(1===e.size&&e.has("hass"))}},{kind:"method",key:"render",value:function(){if(!this._config)return i``;const e=this._castManager&&this._castManager.status&&this._config.view===this._castManager.status.lovelacePath&&this._config.dashboard===this._castManager.status.urlPath;return i`
      <ha-icon .icon=${this._config.icon}></ha-icon>
      <div class="flex">
        <div class="name">${this._config.name}</div>
        ${this._noHTTPS?i` Cast requires HTTPS `:void 0===this._castManager?i``:null===this._castManager?i` Cast API unavailable `:"NO_DEVICES_AVAILABLE"===this._castManager.castState?i` No devices found `:i`
              <div class="controls">
                <google-cast-launcher></google-cast-launcher>
                <mwc-button
                  @click=${this._sendLovelace}
                  class=${n({inactive:!e})}
                  .unelevated=${e}
                  .disabled=${!this._castManager.status}
                >
                  SHOW
                </mwc-button>
              </div>
            `}
      </div>
    `}},{kind:"method",key:"firstUpdated",value:function(e){o(c(d.prototype),"firstUpdated",this).call(this,e),"http:"===location.protocol&&"localhost"!==location.hostname&&(this._noHTTPS=!0),import("./c.fcef4205.js").then((({getCastManager:e})=>e(this.hass.auth).then((e=>{this._castManager=e,e.addEventListener("connection-changed",(()=>{this.requestUpdate()})),e.addEventListener("state-changed",(()=>{this.requestUpdate()}))}),(()=>{this._castManager=null}))))}},{kind:"method",key:"updated",value:function(e){o(c(d.prototype),"updated",this).call(this,e),this._config&&this._config.hide_if_unavailable&&(this.style.display=this._castManager&&"NO_DEVICES_AVAILABLE"!==this._castManager.castState?"":"none")}},{kind:"method",key:"_sendLovelace",value:async function(){var e,t,a;await((e,t)=>{if(!e.castConnectedToOurHass)return new Promise((a=>{const s=e.addEventListener("connection-changed",(()=>{e.castConnectedToOurHass&&(s(),a())}));f(e,t)}))})(this._castManager,this.hass.auth),e=this._castManager,t=this._config.view,a=this._config.dashboard,e.sendMessage({type:"show_lovelace_view",viewPath:t,urlPath:a||null})}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      :host {
        display: flex;
        align-items: center;
      }
      ha-icon {
        padding: 8px;
        color: var(--paper-item-icon-color);
      }
      .flex {
        flex: 1;
        margin-left: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .controls {
        display: flex;
        align-items: center;
      }
      google-cast-launcher {
        margin-right: 0.57em;
        cursor: pointer;
        display: inline-block;
        height: 24px;
        width: 24px;
      }
      .inactive {
        padding: 0 4px;
      }
    `}}]}}),t);var v=Object.freeze({__proto__:null});export{u as C,h as a,l as b,g as c,f as d,v as h};
