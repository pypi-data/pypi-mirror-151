import{_ as t,s as i,e,$ as s,ar as a,n as r}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import{t as o}from"./c.8786ad90.js";import{U as n}from"./c.027db416.js";import"./c.8cbd7110.js";t([r("more-info-automation")],(function(t,i){return{F:class extends i{constructor(...i){super(...i),t(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e({attribute:!1})],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){return this.hass&&this.stateObj?s`
      <hr />
      <div class="flex">
        <div>${this.hass.localize("ui.card.automation.last_triggered")}:</div>
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${this.stateObj.attributes.last_triggered}
          capitalize
        ></ha-relative-time>
      </div>

      <div class="actions">
        <mwc-button
          @click=${this._runActions}
          .disabled=${n.includes(this.stateObj.state)}
        >
          ${this.hass.localize("ui.card.automation.trigger")}
        </mwc-button>
      </div>
    `:s``}},{kind:"method",key:"_runActions",value:function(){o(this.hass,this.stateObj.entity_id)}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      .flex {
        display: flex;
        justify-content: space-between;
      }
      .actions {
        margin: 8px 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
      }
      hr {
        border-color: var(--divider-color);
        border-bottom: none;
        margin: 16px 0;
      }
    `}}]}}),i);
