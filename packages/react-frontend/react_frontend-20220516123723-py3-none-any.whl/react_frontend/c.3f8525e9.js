import{_ as s,s as i,e,$ as t,ar as a,n as r}from"./main-ac83c92b.js";import{P as o,Q as n}from"./c.3e14cfd3.js";import"./c.027db416.js";import"./c.8cbd7110.js";s([r("more-info-sun")],(function(s,i){return{F:class extends i{constructor(...i){super(...i),s(this)}},d:[{kind:"field",decorators:[e({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[e()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass||!this.stateObj)return t``;const s=new Date(this.stateObj.attributes.next_rising),i=new Date(this.stateObj.attributes.next_setting);return t`
      <hr />
      ${(s>i?["set","ris"]:["ris","set"]).map((e=>t`
          <div class="row">
            <div class="key">
              <span
                >${"ris"===e?this.hass.localize("ui.dialogs.more_info_control.sun.rising"):this.hass.localize("ui.dialogs.more_info_control.sun.setting")}</span
              >
              <ha-relative-time
                .hass=${this.hass}
                .datetime=${"ris"===e?s:i}
              ></ha-relative-time>
            </div>
            <div class="value">
              ${o("ris"===e?s:i,this.hass.locale)}
            </div>
          </div>
        `))}
      <div class="row">
        <div class="key">
          ${this.hass.localize("ui.dialogs.more_info_control.sun.elevation")}
        </div>
        <div class="value">
          ${n(this.stateObj.attributes.elevation,this.hass.locale)}
        </div>
      </div>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a`
      .row {
        margin: 0;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
      ha-relative-time {
        display: inline-block;
        white-space: nowrap;
      }
      hr {
        border-color: var(--divider-color);
        border-bottom: none;
        margin: 16px 0;
      }
    `}}]}}),i);
