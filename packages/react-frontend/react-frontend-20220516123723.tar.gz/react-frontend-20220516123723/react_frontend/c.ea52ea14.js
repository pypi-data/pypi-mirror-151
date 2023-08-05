import{_ as t,s as i,e,g as a,i as o,di as n,$ as s,ax as c,aq as h,ar as d,n as r}from"./main-ac83c92b.js";import{aB as u,aC as l,aD as f}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";let g=t([r("hui-picture-card")],(function(t,i){class r extends i{constructor(...i){super(...i),t(this)}}return{F:r,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await import("./c.5311fc3b.js"),document.createElement("hui-picture-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"picture",image:"https://demo.home-assistant.io/stub_config/t-shirt-promo.png",tap_action:{action:"none"},hold_action:{action:"none"}}}},{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 5}},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.image)throw new Error("Image required");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return 1!==t.size||!t.has("hass")||!t.get("hass")}},{kind:"method",key:"updated",value:function(t){if(a(o(r.prototype),"updated",this).call(this,t),!this._config||!this.hass)return;const i=t.get("hass"),e=t.get("_config");i&&e&&i.themes===this.hass.themes&&e.theme===this._config.theme||n(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?s`
      <ha-card
        @action=${this._handleAction}
        .actionHandler=${u({hasHold:l(this._config.hold_action),hasDoubleClick:l(this._config.double_tap_action)})}
        tabindex=${c(l(this._config.tap_action)?"0":void 0)}
        class=${h({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.double_tap_action)})}
      >
        <img src=${this.hass.hassUrl(this._config.image)} />
      </ha-card>
    `:s``}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      ha-card {
        overflow: hidden;
        height: 100%;
      }

      ha-card.clickable {
        cursor: pointer;
      }

      img {
        display: block;
        width: 100%;
      }
    `}},{kind:"method",key:"_handleAction",value:function(t){f(this,this.hass,this._config,t.detail.action)}}]}}),i);export{g as HuiPictureCard};
