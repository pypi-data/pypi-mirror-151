import{_ as t,s as e,e as i,$ as c,ar as n,n as s}from"./main-ac83c92b.js";import{U as a}from"./c.027db416.js";t([s("more-info-counter")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return c``;const t=a.includes(this.stateObj.state);return c`
      <div class="actions">
        <mwc-button
          .action=${"increment"}
          @click=${this._handleActionClick}
          .disabled=${t}
        >
          ${this.hass.localize("ui.card.counter.actions.increment")}
        </mwc-button>
        <mwc-button
          .action=${"decrement"}
          @click=${this._handleActionClick}
          .disabled=${t}
        >
          ${this.hass.localize("ui.card.counter.actions.decrement")}
        </mwc-button>
        <mwc-button
          .action=${"reset"}
          @click=${this._handleActionClick}
          .disabled=${t}
        >
          ${this.hass.localize("ui.card.counter.actions.reset")}
        </mwc-button>
      </div>
    `}},{kind:"method",key:"_handleActionClick",value:function(t){const e=t.currentTarget.action;this.hass.callService("counter",e,{entity_id:this.stateObj.entity_id})}},{kind:"get",static:!0,key:"styles",value:function(){return n`
      .actions {
        margin: 8px 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
      }
    `}}]}}),e);
