import{_ as t,s as e,e as o,t as i,$ as r,aA as a,ar as n,n as s}from"./main-ac83c92b.js";import{bh as c}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";let l=t([s("hui-iframe-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.4c4d23e2.js"),document.createElement("hui-iframe-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"iframe",url:"https://www.home-assistant.io",aspect_ratio:"50%"}}},{kind:"field",decorators:[o({type:Boolean,reflect:!0})],key:"isPanel",value:()=>!1},{kind:"field",decorators:[o()],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){if(!this._config)return 5;return 1+(this._config.aspect_ratio?Number(this._config.aspect_ratio.replace("%","")):50)/25}},{kind:"method",key:"setConfig",value:function(t){if(!t.url)throw new Error("URL required");this._config=t}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return r``;let t="";if(!this.isPanel&&this._config.aspect_ratio){const e=c(this._config.aspect_ratio);e&&e.w>0&&e.h>0&&(t=`${(100*e.h/e.w).toFixed(2)}%`)}else this.isPanel||(t="50%");const e=new URL(this._config.url,location.toString()).protocol;return"https:"===location.protocol&&"https:"!==e?r`
        <ha-alert alert-type="error">
          ${this.hass.localize("ui.panel.lovelace.cards.iframe.error_secure_context",{target_protocol:e,context_protocol:location.protocol})}
        </ha-alert>
      `:r`
      <ha-card .header=${this._config.title}>
        <div
          id="root"
          style=${a({"padding-top":t})}
        >
          <iframe
            src=${this._config.url}
            sandbox="allow-forms allow-modals allow-popups allow-pointer-lock allow-same-origin allow-scripts"
            allowfullscreen="true"
          ></iframe>
        </div>
      </ha-card>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      :host([ispanel]) ha-card {
        width: 100%;
        height: 100%;
      }

      ha-card {
        overflow: hidden;
      }

      #root {
        width: 100%;
        position: relative;
      }

      :host([ispanel]) #root {
        height: 100%;
      }

      iframe {
        position: absolute;
        border: none;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
      }
    `}}]}}),e);export{l as HuiIframeCard};
