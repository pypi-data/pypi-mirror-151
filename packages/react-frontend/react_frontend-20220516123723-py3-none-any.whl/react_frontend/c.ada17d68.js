import{_ as t,s as e,e as a,$ as i,ar as n,n as s}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";let c=t([s("hui-empty-state-card")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[a({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 2}},{kind:"method",key:"setConfig",value:function(t){}},{kind:"method",key:"render",value:function(){return this.hass?i`
      <ha-card
        .header=${this.hass.localize("ui.panel.lovelace.cards.empty_state.title")}
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.lovelace.cards.empty_state.no_devices")}
        </div>
        <div class="card-actions">
          <a href="/config/integrations">
            <mwc-button>
              ${this.hass.localize("ui.panel.lovelace.cards.empty_state.go_to_integrations_page")}
            </mwc-button>
          </a>
        </div>
      </ha-card>
    `:i``}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      .content {
        margin-top: -1em;
        padding: 16px;
      }

      .card-actions a {
        text-decoration: none;
      }

      mwc-button {
        margin-left: -8px;
      }
    `}}]}}),e);export{c as HuiEmptyStateCard};
