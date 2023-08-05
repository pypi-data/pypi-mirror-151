import{_ as t,s as e,e as s,g as i,i as a,f as r,$ as n,ar as c,n as o}from"./main-ac83c92b.js";import{bp as d}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";let h=t([o("hui-starting-card")],(function(t,e){class o extends e{constructor(...e){super(...e),t(this)}}return{F:o,d:[{kind:"field",decorators:[s({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 2}},{kind:"method",key:"setConfig",value:function(t){}},{kind:"method",key:"updated",value:function(t){i(a(o.prototype),"updated",this).call(this,t),t.has("hass")&&this.hass.config&&this.hass.config.state!==d&&r(this,"config-refresh")}},{kind:"method",key:"render",value:function(){return this.hass?n`
      <div class="content">
        <ha-circular-progress active></ha-circular-progress>
        ${this.hass.localize("ui.panel.lovelace.cards.starting.description")}
      </div>
    `:n``}},{kind:"get",static:!0,key:"styles",value:function(){return c`
      :host {
        display: block;
        height: calc(100vh - var(--header-height));
      }
      ha-circular-progress {
        padding-bottom: 20px;
      }
      .content {
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }
    `}}]}}),e);export{h as HuiStartingCard};
