import{_ as t,s as e,e as i,$ as s,ar as r,n as a}from"./main-ac83c92b.js";import"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";t([a("more-info-script")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[i()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){return this.hass&&this.stateObj?s`
      <hr />
      <div class="flex">
        <div>
          ${this.hass.localize("ui.dialogs.more_info_control.script.last_triggered")}:
        </div>
        ${this.stateObj.attributes.last_triggered?s`
              <ha-relative-time
                .hass=${this.hass}
                .datetime=${this.stateObj.attributes.last_triggered}
                capitalize
              ></ha-relative-time>
            `:this.hass.localize("ui.components.relative_time.never")}
      </div>
    `:s``}},{kind:"get",static:!0,key:"styles",value:function(){return r`
      .flex {
        display: flex;
        justify-content: space-between;
      }
      hr {
        border-color: var(--divider-color);
        border-bottom: none;
        margin: 16px 0;
      }
    `}}]}}),e);
